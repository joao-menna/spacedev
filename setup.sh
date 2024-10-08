#!/bin/sh

echo "---COPYING .env---"
if [ -f "./.env" ]; then
    echo ".env already exists... skipping"
else
    echo "Copying .env"
    cp .env.example .env
fi
