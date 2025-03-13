import time
import requests
import hmac
import hashlib
import json
from flask import Flask
import threading

app = Flask(__name__)

# Binance API credentials
BINANCE_API_KEY = "fhgNtIlE1TWSRorrHMKZxJjJl5HhTUBTFAllau9D0uwLEAvaqnInCRsd1BK6fHbF"
BINANCE_SECRET_KEY = "YOUR_BINANCE_SECRET"

# Bybit API 
BYBIT_API_KEY = "KpDvhKwd4oXxppihbZuzdZno6dkdwDl4k2gM"
BYBIT_SECRET_KEY = "KpDvhKwd4oXxppihbZuzdZno6dkdwDl4k2gM"

# Telegram Bot Token & Chat ID (for notifications)
TELEGRAM_BOT_TOKEN = "7732391797:AAE2588vDmx0umob1fObZaKtYDA6H_UIwbg"
TELEGRAM_CHAT_ID = "7070160570"

# Function to send Telegram notifications
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

# Function to check Binance referrals
def get_binance_referrals():
    url = "https://api.binance.com/sapi/v1/refer/rewards/refer-spot-summary"
    timestamp = int(time.time() * 1000)
    params = f"timestamp={timestamp}"
    signature = hmac.new(BINANCE_SECRET_KEY.encode(), params.encode(), hashlib.sha256).hexdigest()
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    response = requests.get(f"{url}?{params}&signature={signature}", headers=headers)
    data = response.json()
    
    if "totalCommission" in data:
        earnings = data["totalCommission"]
        send_telegram_message(f"💰 Binance Referral Earnings: {earnings} USDT")

# Function to check Bybit referrals
def get_bybit_referrals():
    url = "https://api.bybit.com/v2/private/affiliate/referral"
    timestamp = str(int(time.time() * 1000))
    params = f"api_key={BYBIT_API_KEY}&timestamp={timestamp}"
    signature = hmac.new(BYBIT_SECRET_KEY.encode(), params.encode(), hashlib.sha256).hexdigest()

    response = requests.get(f"{url}?{params}&sign={signature}")
    data = response.json()

    if "result" in data:
        earnings = data["result"]["referral_commission"]
        send_telegram_message(f"💰 Bybit Referral Earnings: {earnings} USDT")

# Function to run the bot in the background
def run_bot():
    while True:
        try:
            get_binance_referrals()
            get_bybit_referrals()
        except Exception as e:
            send_telegram_message(f"⚠️ Error: {str(e)}")
        
        time.sleep(3600)  # Check every hour

# Starting the background task for the referral checks
@app.route('/')
def home():
    return "Flask App is Running and Collecting Referrals!"

if __name__ == '__main__':
    # Start the bot in a background thread
    threading.Thread(target=run_bot, daemon=True).start()

    # Start the Flask app
    app.run(host='0.0.0.0', port=5000)
