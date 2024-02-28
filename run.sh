#!/bin/bash
docker-compose up -d
poetry run gunicorn -w 1 -k uvicorn.workers.UvicornWorker --bind [::]:$PORT src.main:app --timeout 300