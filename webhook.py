import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

@app.route("/github-webhook", methods=["POST"])
def github_webhook():
    data = request.json

    if "pusher" in data:  # Push event
        repo_name = data["repository"]["full
