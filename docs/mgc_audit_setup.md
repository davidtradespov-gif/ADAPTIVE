# MGC Audit Setup

## Runtime

Use the bundled Codex Python runtime with the project-local package directory:

- Python: `C:\Users\smile\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`
- Local package dir: `.python_packages`

`pyarrow` is installed in `.python_packages` so parquet inspection can run without relying on machine-global Python.

## Audit Command

Run:

```powershell
$env:PYTHONPATH = ".python_packages"
& 'C:\Users\smile\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\scripts\audit_mgc_dataset.py
```

## Outputs

- `reports/mgc_data_audit.json`
- `reports/mgc_data_audit.md`
