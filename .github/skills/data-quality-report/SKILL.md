# Data Quality Report Skill

Generate a batch QA report from files in `data/`.

## Usage

```bash
python -m src.batch_qa
```

### Optional station filter

Use `--station` to process only files for a specific station:

```bash
python -m src.batch_qa --station A
```

When `--station` is omitted, all files in `data/` are processed (existing behavior).

## Output

- Report path: `reports/batch-result.json`
- Schema: `schemas/batch_result.schema.json`
