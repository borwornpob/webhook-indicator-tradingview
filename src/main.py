from fastapi import FastAPI
from typing import List, Union
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime, timezone
from starlette.responses import Response
from starlette.requests import Request

app = FastAPI()

listAlerts = []
news_data = []  # Global variable to store news data
log = ["This is a test log"]

class Alert(BaseModel):
    Symbol: str
    Direction: str
    Code: str

class NewsItem(BaseModel):
    title: str
    country: str
    date: str
    impact: str
    forecast: str
    previous: str

@app.get("/")
def read_root():
    return {"message": "up and running"}

@app.post("/log", response_class=Response)
async def read_log(request: Request):
    body = await request.body()
    log[0] = body.decode()
    return body

@app.post("/reversal", response_class=Response)
async def reversal(request: Request):
    body = await request.body()
    alerts = body.decode().split(" ")
    symbol = alerts[0]
    direction = alerts[1]
    if direction == "bearish":
        direction = "Sell"
    elif direction == "bullish":
        direction = "Buy"

    alert = {
        "Symbol": symbol,
        "Direction": direction,
        "Code": "reversal"
    }

    listAlerts.append(alert)
    print(f"Alert added: {alert}")
    return body

@app.get("/log")
def read_log():
    return {"log": log[0]}

@app.post("/webhooks")
def processing_webhooks(data: Alert):
    listAlerts.append({
        "Symbol": data.Symbol,
        "Direction": data.Direction,
        "Code": data.Code
    })
    print(listAlerts)
    return {"message": "Webhook processed"}

@app.get("/webhooks")
def get_all_webhooks():
    return listAlerts

@app.get("/mtindicator")
def returnsignal(symbol: str, code: str) -> Union[dict, None]:
    matching_alerts = [alert for alert in listAlerts if alert["Symbol"] == symbol and alert["Code"] == code]
    if matching_alerts:
        alert = matching_alerts[0]
        listAlerts.remove(alert)
        return alert
    else:
        return None

def check_news_time():
    current_time = datetime.now(timezone.utc)
    
    for news in news_data:
        news_time = datetime.fromisoformat(news.date)
        if news_time <= current_time:
            alert = {
                "Symbol": news.country,
                "Direction": "news",
                "Code": "news"
            }
            listAlerts.append(alert)
            news_data.remove(news)
            print(f"Alert added: {alert}")

def processing_news():
    forex_factory_api = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    response = requests.get(forex_factory_api)
    data = response.json()
    global news_data
    news_data = [NewsItem(**item) for item in data if item["impact"] == "High"]  # Filter news items with impact "High"
    print("News data updated")

# Create a background scheduler
scheduler = BackgroundScheduler()

# Add the processing_news function to the scheduler
scheduler.add_job(processing_news, 'cron', day_of_week='mon', hour=0, minute=1)

# Add the check_news_time function to the scheduler
scheduler.add_job(check_news_time, 'interval', seconds=1)

# Start the scheduler
scheduler.start()

@app.on_event("startup")
def startup_event():
    processing_news()
    print("Application startup")

@app.on_event("shutdown")
def shutdown_event():
    # Shutdown the scheduler when the application is stopping
    scheduler.shutdown()