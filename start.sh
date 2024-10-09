#!/bin/sh

sudo docker compose up frontend -d && ./backend/start.sh
