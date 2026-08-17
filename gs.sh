#!/bin/bash

set -e  # stop on error

echo "🚀 Starting FastAPI..."

cd /home/rf-team/leo-channel-simulator

source venv/bin/activate

exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000
