#!/bin/sh

export $(cat ../.env | xargs) && uvicorn main:app --host 0.0.0.0 --port 8090 --reload
