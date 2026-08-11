import json
from pathlib import Path

from src.batch_qa import generate_batch_report


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file)


def test_generate_batch_report_processes_all_files_without_station_filter(tmp_path: Path):
    data_dir = tmp_path / "data"
    report_path = tmp_path / "reports" / "batch-result.json"

    _write_json(data_dir / "station-A-001.json", {"ok": True})
    _write_json(data_dir / "station-B-002.json", {"ok": True})

    report = generate_batch_report(data_dir=data_dir, report_path=report_path)

    assert report["station_filter"] is None
    assert report["processed_count"] == 2
    assert report["passed_count"] == 2
    assert report["failed_count"] == 0
    assert {item["file"] for item in report["results"]} == {
        "station-A-001.json",
        "station-B-002.json",
    }


def test_generate_batch_report_filters_by_station(tmp_path: Path):
    data_dir = tmp_path / "data"
    report_path = tmp_path / "reports" / "batch-result.json"

    _write_json(data_dir / "station-A-001.json", {"ok": True})
    _write_json(data_dir / "station-A-002.json", {"ok": True})
    _write_json(data_dir / "station-B-001.json", {"ok": True})

    report = generate_batch_report(data_dir=data_dir, report_path=report_path, station="A")

    assert report["station_filter"] == "A"
    assert report["processed_count"] == 2
    assert report["passed_count"] == 2
    assert report["failed_count"] == 0
    assert {item["file"] for item in report["results"]} == {
        "station-A-001.json",
        "station-A-002.json",
    }
