from fastapi import FastAPI
from typing import List, Union
from pydantic import BaseModel

app = FastAPI()

# Assuming listAlerts is defined somewhere in your code
listAlerts = []

class Alert(BaseModel):
    Symbol: str
    Direction: str
    Code: str

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
    # Filter listAlerts to only include items with the matching symbol
    matching_alerts = [alert for alert in listAlerts if alert["Symbol"] == symbol and alert["Code"] == code]
    if matching_alerts:
        alert = matching_alerts[0]
        listAlerts.remove(alert)  # Remove the alert from listAlerts
        return alert
    else:
        return None  # Return None if no matching alert is found