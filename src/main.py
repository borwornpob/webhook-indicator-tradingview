from fastapi import FastAPI
from typing import List, Union
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime, timezone

app = FastAPI()

listAlerts = []
news_data = []  # Global variable to store news data

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

@app.get("/news", response_model=NewsItem)
def get_news():
    current_time = datetime.now(timezone.utc)
    closest_news = None
    min_time_diff = float('inf')
    
    for news in news_data:
        news_time = datetime.fromisoformat(news.date)
        time_diff = abs((current_time - news_time).total_seconds())
        if time_diff < min_time_diff:
            min_time_diff = time_diff
            closest_news = news
    
    return closest_news

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
scheduler.add_job(processing_news, 'interval', minutes=30)

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