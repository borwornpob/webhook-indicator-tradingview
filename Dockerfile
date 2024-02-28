FROM python:3.12-slim

WORKDIR /

COPY . /app/

RUN pip install -r /app/requirements.txt

EXPOSE 8000

CMD uvicorn app.src.main:app --host $UVICORN_HOST --port $UVICORN_PORT 