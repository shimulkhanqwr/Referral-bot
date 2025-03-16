import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Dispatcher
from telegram.ext import MessageHandler, Filters
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)

# Replace with your Binance referral link or user ID
BINANCE_REFERRAL_CODE = "YOUR_BINANCE_REFERRAL_CODE"

# Create a referral link
def get_binance_referral_link():
    return f"https://www.binance.com/en/register?ref={BINANCE_REFERRAL_CODE}"

# Command to start the bot
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(f"Welcome {user.first_name},\nLet's get started with your referral journey!")
    referral_link = get_binance_referral_link()
    update.message.reply_text(f"Here is your referral link: {referral_link}\nShare it with your friends to start earning rewards!")

# Command to show hidden tricks
def hidden_tricks(update: Update, context: CallbackContext):
    tricks = """
    1. Use a Binance Referral Link to get bonus rewards.
    2. Take advantage of Binance Earn to grow your crypto without trading.
    3. Participate in Binance Launchpad to get early access to new tokens.
    4. Binance offers reduced trading fees if you use their token (BNB).
    """
    update.message.reply_text(f"Here are some hidden tricks for you:\n{tricks}")

# Command to track referrals (dummy)
def track_referrals(update: Update, context: CallbackContext):
    update.message.reply_text("Your referrals are being tracked. Keep sharing your link!")

# Create Telegram bot with Flask
def create_updater():
    # Replace with your Telegram bot token
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('tricks', hidden_tricks))
    dispatcher.add_handler(CommandHandler('track', track_referrals))

    return updater

# Flask route to handle webhook requests from Telegram
@app.route('/hook', methods=['POST'])
def webhook():
    if request.method == "POST":
        json_str = request.get_data().decode("UTF-8")
        update = Update.de_json(json_str, bot)
        dispatcher.process_update(update)
        return 'OK', 200

# Flask route to test the server
@app.route('/')
def home():
    return "Telegram Bot is running!"

# Set up the webhook to handle incoming requests
def set_webhook():
    webhook_url = os.getenv('WEBHOOK_URL')  # Set this environment variable
    bot.set_webhook(url=webhook_url + '/hook')

if __name__ == '__main__':
    bot = create_updater().bot
    dispatcher = Dispatcher(bot, None)
    set_webhook()

    # Run Flask app with the Telegram webhook
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app)
    run_simple('0.0.0.0', 5000, app)
