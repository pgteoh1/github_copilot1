import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def _extract_station_from_filename(file_name: str) -> str | None:
    stem = Path(file_name).stem.lower()
    tokens = [token for token in re.split(r"[^a-z0-9]+", stem) if token]
    for index, token in enumerate(tokens):
        if token == "station" and index + 1 < len(tokens):
            return tokens[index + 1].upper()
    return None


def _matches_station_filter(file_name: str, station: str) -> bool:
    station_token = station.strip().lower()
    if not station_token:
        return False

    extracted_station = _extract_station_from_filename(file_name)
    return bool(extracted_station and extracted_station.lower() == station_token)


def discover_files(data_dir: Path, station: str | None = None) -> list[Path]:
    files = sorted(path for path in data_dir.glob("*.json") if path.is_file())
    if not station:
        return files

    return [path for path in files if _matches_station_filter(path.name, station)]


def generate_batch_report(
    data_dir: Path = Path("data"),
    report_path: Path = Path("reports/batch-result.json"),
    station: str | None = None,
) -> dict:
    selected_files = discover_files(data_dir=data_dir, station=station)
    results = []

    for file_path in selected_files:
        station_name = _extract_station_from_filename(file_path.name)
        try:
            with file_path.open("r", encoding="utf-8") as file:
                json.load(file)

            results.append(
                {
                    "file": file_path.name,
                    "station": station_name,
                    "verdict": "pass",
                    "errors": [],
                }
            )
        except (OSError, json.JSONDecodeError) as error:
            results.append(
                {
                    "file": file_path.name,
                    "station": station_name,
                    "verdict": "fail",
                    "errors": [str(error)],
                }
            )

    passed_count = sum(1 for result in results if result["verdict"] == "pass")
    failed_count = len(results) - passed_count

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "station_filter": station,
        "processed_count": len(results),
        "passed_count": passed_count,
        "failed_count": failed_count,
        "results": results,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)
        file.write("\n")

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a batch QA result report.")
    parser.add_argument(
        "--station",
        dest="station",
        help="Optional station filter (for example: --station A).",
    )
    parser.add_argument(
        "--data-dir",
        dest="data_dir",
        default="data",
        help="Directory containing input station JSON files.",
    )
    parser.add_argument(
        "--report-path",
        dest="report_path",
        default="reports/batch-result.json",
        help="Output path for the batch result report JSON.",
    )
    args = parser.parse_args()

    generate_batch_report(
        data_dir=Path(args.data_dir),
        report_path=Path(args.report_path),
        station=args.station,
    )


if __name__ == "__main__":
    main()
