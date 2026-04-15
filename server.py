from flask import Flask, jsonify
import yfinance as yf
import pandas as pd
from datetime import datetime

app = Flask(__name__)

pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "EURJPY=X"]

def signal_logic(symbol):
    data = yf.download(symbol, interval="5m", period="1d")

    data["ema20"] = data["Close"].ewm(span=20).mean()
    data["ema50"] = data["Close"].ewm(span=50).mean()

    last = data.iloc[-1]
    entry_time = datetime.now().strftime("%H:%M")

    if last["ema20"] > last["ema50"]:
        return "CALL ⬆️", entry_time
    else:
        return "PUT ⬇️", entry_time

@app.route("/signals")
def signals():
    results = []

    for p in pairs:
        signal, entry = signal_logic(p)

        results.append({
            "pair": p.replace("=X",""),
            "signal": signal,
            "entry_time": entry,
            "expiry": "3 MIN"
        })

    return jsonify({
        "status": "ACTIVE",
        "signals": results
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)