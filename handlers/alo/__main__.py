from telegram import Update

def alo(update: Update, context):
    update.message.reply_text('📞 Alo, я на связи')