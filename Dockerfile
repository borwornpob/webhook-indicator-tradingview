FROM python:3.12-slim

WORKDIR /app

COPY ./src /app
COPY ./requirements.txt /app

RUN pip install -r /app/requirements.txt

CMD gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b [::]:5001 main:app --timeout 300