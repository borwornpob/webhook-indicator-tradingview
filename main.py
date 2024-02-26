from fastapi import FastAPI
from typing import List, Union

app = FastAPI()

# Assuming listAlerts is defined somewhere in your code
listAlerts = []

@app.get("/")
def read_root():
    return {"message": "up and running"}

@app.post("/webhooks")
def processing_webhooks(symbol: str, direction: str):
    listAlerts.append({
        "Symbol": symbol,
        "Direction": direction
    })
    print(listAlerts)
    return {"message": "Webhook processed"}

@app.get("/mtindicator")
def returnsignal(symbol: str) -> Union[dict, None]:
    # Filter listAlerts to only include items with the matching symbol
    matching_alerts = [alert for alert in listAlerts if alert["Symbol"] == symbol]
    if matching_alerts:
        alert = matching_alerts[0]
        listAlerts.remove(alert)  # Remove the alert from listAlerts
        return alert
    else:
        return None  # Return None if no matching alert is found