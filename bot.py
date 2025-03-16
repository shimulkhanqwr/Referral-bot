import time
import requests
import hmac
import hashlib
import json
from flask import Flask
import threading

app = Flask(__name__)

# Binance API credentials (DO NOT share public keys in code!)
BINANCE_API_KEY = "YOUR_BINANCE_API_KEY"
BINANCE_SECRET_KEY = "YOUR_BINANCE_SECRET"

# Bybit API credentials
BYBIT_API_KEY = "YOUR_BYBIT_API_KEY"
BYBIT_SECRET_KEY = "YOUR_BYBIT_SECRET"

# Telegram Bot Token & Chat ID
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

# Telegram Notification Function
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Telegram Error: {response.text}")
    except Exception as e:
        print(f"Telegram Send Failed: {e}")

# Binance Referral Checker
def get_binance_referrals():
    try:
        url = "https://api.binance.com/sapi/v1/refer/rewards/refer-spot-summary"
        timestamp = int(time.time() * 1000)
        params = f"timestamp={timestamp}"
        signature = hmac.new(BINANCE_SECRET_KEY.encode(), params.encode(), hashlib.sha256).hexdigest()
        headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

        response = requests.get(f"{url}?{params}&signature={signature}", headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                if "totalCommission" in data:
                    earnings = data["totalCommission"]
                    send_telegram_message(f"💰 Binance Referral Earnings: {earnings} USDT")
                else:
                    print("Binance: No earnings data found.")
            except json.JSONDecodeError:
                print("Binance JSON Parse Error:", response.text)
        else:
            print("Binance API Error:", response.text)
    except Exception as e:
        print(f"Binance Error: {e}")
        send_telegram_message(f"⚠️ Binance Error: {e}")

# Bybit Referral Checker
def get_bybit_referrals():
    try:
        url = "https://api.bybit.com/v2/private/affiliate/referral"
        timestamp = str(int(time.time() * 1000))
        params_dict = {
            "api_key": BYBIT_API_KEY,
            "timestamp": timestamp
        }
        sorted_params = "&".join([f"{k}={params_dict[k]}" for k in sorted(params_dict)])
        signature = hmac.new(BYBIT_SECRET_KEY.encode(), sorted_params.encode(), hashlib.sha256).hexdigest()

        full_url = f"{url}?{sorted_params}&sign={signature}"
        response = requests.get(full_url)
        if response.status_code == 200:
            try:
                data = response.json()
                if "result" in data and "referral_commission" in data["result"]:
                    earnings = data["result"]["referral_commission"]
                    send_telegram_message(f"💰 Bybit Referral Earnings: {earnings} USDT")
                else:
                    print("Bybit: No earnings data found.")
            except json.JSONDecodeError:
                print("Bybit JSON Parse Error:", response.text)
        else:
            print("Bybit API Error:", response.text)
    except Exception as e:
        print(f"Bybit Error: {e}")
        send_telegram_message(f"⚠️ Bybit Error: {e}")

# Background Bot Runner
def run_bot():
    while True:
        try:
            print("Checking referrals...")
            get_binance_referrals()
            get_bybit_referrals()
        except Exception as e:
            print(f"Bot Error: {e}")
            send_telegram_message(f"⚠️ Bot Error: {e}")
        time.sleep(3600)  # 1 hour interval

@app.route('/')
def home():
    return "Referral Tracker Bot is Running!"

if __name__ == '__main__':
    # Start background bot
    threading.Thread(target=run_bot, daemon=True).start()
    # Run Flask app
    app.run(host='0.0.0.0', port=5000)
