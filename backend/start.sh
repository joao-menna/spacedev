#!/bin/sh

if [ -f "./.venv" ]; then
    source ./.venv/bin/activate
else
    python -m venv ./.venv
fi

export $(cat ../.env | xargs) && uvicorn main:app --host 0.0.0.0 --port 8090 $1
