import time
import requests
import hashlib
import hmac
import os
from pyrogram import Client, filters
from flask import Flask, redirect

# Telegram Bot Credentials
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "7732391797:AAE2588vDmx0umob1fObZaKtYDA6H_UIwbg"

# Binance Referral Link
BINANCE_REF_LINK = "https://www.binance.com/en/activity/referral-entry?ref=538997774"
BYBIT_REF_LINK = "https://partner.bybit.com/b/81493"

# Flask App for Redirecting Users
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Bot is Running & Auto Viral!"

@app.route('/binance')
def binance_redirect():
    return redirect(https://www.binance.info/join?ref=538997774)

@app.route('/bybit')
def bybit_redirect():
    return redirect(https://partner.bybit.com/b/81493)

# Start Flask App in Background
def start_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# Telegram Auto Viral Bot
bot = Client("referral_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Auto-Message New Users with Referral Links
@bot.on_message(filters.private & filters.command("start"))
def start(client, message):
    user_id = message.from_user.id
    username = message.from_user.username

    welcome_msg = f"""👋 Hey {username or "there"}!  
💸 Get free crypto & trading rewards!  
🔥 **Join Binance**: [Click Here](https://www.binance.info/join?ref=538997774)  
🚀 **Join Bybit**: [Click Here](https://partner.bybit.com/b/81493)  
Share this with your friends & earn more!"""
    
    message.reply_text(welcome_msg, disable_web_page_preview=True)

# Auto Viral - Forward Messages to Groups & Channels
@bot.on_message(filters.private & filters.text)
def auto_forward(client, message):
    viral_groups = [-1001234567890, -1009876543210]  # Add your Telegram group IDs
    for group in viral_groups:
        try:
            client.forward_messages(chat_id=group, from_chat_id=message.chat.id, message_ids=message.id)
        except Exception as e:
            print(f"Error forwarding: {e}")

# Background Function to Start Flask
import threading
flask_thread = threading.Thread(target=start_flask)
flask_thread.start()

# Run Bot
bot.run()
