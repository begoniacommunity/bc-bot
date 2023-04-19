import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from .currency_emojis import *
from .get_rates import *
from .main_currencies import *
from .preprocess_message import *
from .triggers import *

def convert_currency(update: Update, context: CallbackContext):
    if update.message is None:
        return
    message = preprocess_message(update.message.text.lower())
    response = ''
    processed_amounts = set()

    # Sort triggers by the number of words in descending order
    sorted_triggers = sorted(triggers.items(), key=lambda x: -len(x[0]))

    # Find all matches of triggers in the message
    matches = []
    for trigger_words, currency_code in sorted_triggers:
        trigger_regex = r'\s*'.join([re.escape(word) for word in trigger_words])
        for match in re.finditer(trigger_regex, message):
            start_index = match.start()
            end_index = match.end()
            amount = None

            # Check if there is a number before the trigger
            if start_index > 0:
                pre_match = message[:start_index].rstrip()
                pre_match_number = re.search(r'(\d[\d\s]*[.,])?\d+\s*$', pre_match)
                if pre_match_number:
                    amount = float(pre_match_number.group().replace(',', '.'))
                    start_index = pre_match_number.start()

            # Check if there is a number after the trigger
            if amount is None and end_index < len(message):
                post_match = message[end_index:].lstrip()
                post_match_number = re.search(r'^\s*(\d[\d\s]*[.,])?\d+', post_match)
                if post_match_number:
                    amount = float(post_match_number.group().replace(',', '.'))
                    end_index += post_match_number.end()

            # If a number was found before or after the trigger
            if amount is not None:
                matches.append((currency_code, amount, start_index, end_index))

    # Sort matches by their start index in ascending order
    matches.sort(key=lambda x: x[2])

    # Process matches
    for currency_code, amount, start_index, end_index in matches:
        if (currency_code, amount) not in processed_amounts:
            processed_amounts.add((currency_code, amount))
            rates = get_rates(currency_code)
            if rates is not None:
                response += f'{currency_emojis.get(currency_code, "")}{amount:.2f} {currency_code}:\n\n'
                for currency in main_currencies:
                    if currency != currency_code:
                        rate = rates[currency]
                        response += f'{currency_emojis.get(currency, "")}{rate * amount:.2f} {currency}\n'
                response += '—————\n'

    # Send response
    if response:
        response = response.replace('.', ',')
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Удалить", callback_data='delete')]])
        update.message.reply_text(response.strip().rstrip('—————').strip(), reply_markup=reply_markup)
    else:
        return False