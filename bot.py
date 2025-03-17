from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
BINANCE_REFERRAL_LINK = "https://www.binance.com/en/register?ref=your_referral_code"

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Sign Up on Binance", url=BINANCE_REFERRAL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Hey! Want to trade crypto? Sign up below!", reply_markup=reply_markup)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
