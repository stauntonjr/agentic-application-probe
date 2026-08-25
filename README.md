# Agentic Application Probe

A deliberately small greenfield application created from
`stauntonjr/agentic-project-template` commit `dd1f5d0`.

`csv-summary` reads one local UTF-8 CSV file and prints deterministic JSON containing its row
count, ordered column names, and missing-value count for each column. It uses only Python's
standard library at runtime.

```bash
python3 src/agentic_application_probe/cli.py examples.csv
```

The command rejects an empty or invalid header, duplicate columns, extra row fields, missing files,
and invalid UTF-8 with a concise error and no traceback. Network access, dialect inference,
streaming-scale files, cleaning, visualization, and deployment are outside this proof.

Run the focused tests with:

```bash
uv run --with pytest==8.4.1 python -m pytest -q tests/test_application_probe.py
```

Run the repository check with:

```bash
make smoke
```
