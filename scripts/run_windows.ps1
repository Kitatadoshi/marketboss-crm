$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
$env:PYTHONPATH='.'
python scripts\seed_demo.py
python -m uvicorn src.interfaces.http.app:app --host 127.0.0.1 --port 8080 --reload
