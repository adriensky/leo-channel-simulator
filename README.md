# LEO Channel Simulator API

FastAPI backend for the LEO Channel Simulator.

## Features
- Mock hardware mode for local development
- FastAPI endpoints
- Swagger docs
- Clean hardware abstraction layer for future Raspberry Pi deployment

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```
## Docs
- Swagger UI : http://127.0.0.1:8000/docs
- ReDoc : http://127.0.0.1:8000/redoc

## Run the API

```bash
uvicorn app.main:app --reload
```

## Test API
```bash
python scripts/test_api.py
```

