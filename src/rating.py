import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

bad = "bad"
ok = "ok"
good = "good"

replies = {
    bad: "Obrigada pelo feedback! Sinto muito que a transcrição não foi satisfatória 😣",
    ok: "Muito obrigada pelo feedback! 😊",
    good: "Muito obrigada pelo feedback! 😊"
}

def get_reply_markup():
    keyboard = [[
        InlineKeyboardButton("💩", callback_data=bad),
        InlineKeyboardButton("🤔", callback_data=ok),
        InlineKeyboardButton("👌", callback_data=good)
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def handle_rating_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_reply_markup(reply_markup=None) # hide keyboard after click

    # query.edit_message_text(text=replies[query.data])
    # substitui a transcrição enviada!

    chat_id = update.callback_query.message.chat.id
    context.bot.send_message(chat_id, text=replies[query.data])
