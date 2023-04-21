import re, requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, BaseFilter

from handlers import *
from keepalive import *
from secrets import TELEGRAM_TOKEN

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'delete':
        query.message.delete()

class UserAndChannelFilter(BaseFilter):
    def __call__(self, update: Update):
        if update.message is None:
            return False

        chat = update.message.chat
        user_id = str(update.message.from_user.id)

        if chat.type == 'private' and user_id != '1010949968':
            return False

        if chat.type != 'private' and chat.username != 'begoniacommunity':
            return False

        return True

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("alo", alo))
    dp.add_handler(CommandHandler("cum", cum))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & UserAndChannelFilter(), convert_currency), group=0)
    dp.add_handler(CallbackQueryHandler(handle_callback))

    updater.start_polling()
    web.run_app(app)
    updater.idle()

if __name__ == '__main__':
    main()