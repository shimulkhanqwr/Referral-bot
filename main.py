import os
from telegram.ext import Updater, CommandHandler

# Your Telegram API token
API_TOKEN = os.getenv("7732391797:AAE2588vDmx0umob1fObZaKtYDA6H_UIwbg")

# Initialize the updater with your API token
updater = Updater(token=API_TOKEN)

# Define a simple start command
def start(update, context):
    update.message.reply_text("Hello, I'm your bot!")

# Add the command handler to the dispatcher
updater.dispatcher.add_handler(CommandHandler('start', start))

# Start the bot
updater.start_polling()
updater.idle()
