import requests
import time
import hmac
import hashlib
from flask import Flask
import os

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if no PORT is set
    app.run(host='0.0.0.0', port=port)

# Binance API credentials
BINANCE_API_KEY = "fhgNtIlE1TWSRorrHMKZxJjJl5HhTUBTFAllau9D0uwLEAvaqnInCRsd1BK6fHbF"
BINANCE_SECRET_KEY = "YOUR_BINANCE_SECRET"

# Bybit API credentials
BYBIT_API_KEY = "KpDvhKwd4oXxppihbZuzdZno6dkdwDl4k2gM"
BYBIT_SECRET_KEY = "KpDvhKwd4oXxppihbZuzdZno6dkdwDl4k2gM"

# Telegram Bot Token & Chat ID for notifications
TELEGRAM_BOT_TOKEN = "7732391797:AAE2588vDmx0umob1fObZaKtYDA6H_UIwbg"
TELEGRAM_CHAT_ID = "7070160570"

# Function to send Telegram notifications
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Check for successful request
        print(f"Message sent to Telegram: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")

# Function to check Binance referrals
def get_binance_referrals():
    url = "https://api.binance.com/sapi/v1/refer/rewards/refer-spot-summary"
    timestamp = int(time.time() * 1000)
    params = f"timestamp={timestamp}"
    signature = hmac.new(BINANCE_SECRET_KEY.encode(), params.encode(), hashlib.sha256).hexdigest()
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    try:
        response = requests.get(f"{url}?{params}&signature={signature}", headers=headers)
        response.raise_for_status()
        data = response.json()

        if "totalCommission" in data:
            earnings = data["totalCommission"]
            send_telegram_message(f"💰 Binance Referral Earnings: {earnings} USDT")
        else:
            print("No referral data available for Binance.")
    except requests.exceptions.RequestException as e:
        send_telegram_message(f"⚠️ Binance API Error: {e}")
        print(f"Error with Binance API: {e}")

# Function to check Bybit referrals
def get_bybit_referrals():
    url = "https://api.bybit.com/v2/private/affiliate/referral"
    timestamp = str(int(time.time() * 1000))
    params = f"api_key={BYBIT_API_KEY}&timestamp={timestamp}"
    signature = hmac.new(BYBIT_SECRET_KEY.encode(), params.encode(), hashlib.sha256).hexdigest()

    try:
        response = requests.get(f"{url}?{params}&sign={signature}")
        response.raise_for_status()
        data = response.json()

        if "result" in data:
            earnings = data["result"]["referral_commission"]
            send_telegram_message(f"💰 Bybit Referral Earnings: {earnings} USDT")
        else:
            print("No referral data available for Bybit.")
    except requests.exceptions.RequestException as e:
        send_telegram_message(f"⚠️ Bybit API Error: {e}")
        print(f"Error with Bybit API: {e}")

# Main function to run the bot
def run_bot():
    while True:
        try:
            get_binance_referrals()
            get_bybit_referrals()
        except Exception as e:
            send_telegram_message(f"⚠️ General Error: {str(e)}")
            print(f"Unexpected error: {e}")
        
        time.sleep(3600)  # Check every hour

# Start the bot
if __name__ == '__main__':
    # Start Flask app and referral check in separate threads
    from threading import Thread

    def start_flask():
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

    # Start Flask in a separate thread
    flask_thread = Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start referral checking in the main thread
    run_bot()
