FROM python:3.12-slim

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn src.main:app --host $UVICORN_HOST --port $UVICORN_PORT 