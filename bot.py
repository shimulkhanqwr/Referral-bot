import os
import logging
from flask import Flask, request, render_template
from telegram import Update, Bot, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, Dispatcher

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)

# Binance referral code
BINANCE_REFERRAL_CODE = "538997774"
BINANCE_REFERRAL_LINK = f"https://www.binance.com/en/register?ref={BINANCE_REFERRAL_CODE}"

# Get environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TELEGRAM_BOT_TOKEN or not WEBAPP_URL or not WEBHOOK_URL:
    logger.error("Missing environment variables. Set TELEGRAM_BOT_TOKEN, WEBAPP_URL, WEBHOOK_URL.")
    exit(1)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# Telegram Command: /start
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Launch Mini App", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"Hey {user.first_name}, open the Mini App below and earn crypto tips!", reply_markup=reply_markup)

# Register command handler
dispatcher.add_handler(CommandHandler("start", start))

# Telegram webhook route
@app.route('/hook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

# Mini App route
@app.route('/')
def mini_app():
    # HTML auto-redirects to Binance referral link after 2 seconds
    return render_template('index.html', referral_link=BINANCE_REFERRAL_LINK)

# Set Telegram webhook
@app.before_first_request
def set_webhook():
    bot.set_webhook(url=f"{WEBHOOK_URL}/hook")
    logger.info(f"Webhook set to {WEBHOOK_URL}/hook")

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
