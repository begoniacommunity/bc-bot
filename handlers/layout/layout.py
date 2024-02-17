from aiogram import html
from aiogram.types import Message

invert = {
    # English to Russian
    "q": "й", "w": "ц", "e": "у", "r": "к", "t": "е", "y": "н", "u": "г",
    "i": "ш", "o": "щ", "p": "з", "[": "х", "]": "ъ", "a": "ф", "s": "ы",
    "d": "в", "f": "а", "g": "п", "h": "р", "j": "о", "k": "л", "l": "д",
    ";": "ж", "'": "э", "|": "/", "z": "я", "x": "ч", "c": "с", "v": "м",
    "b": "и", "n": "т", "m": "ь", ",": "б", ".": "ю", "/": ".",
    "@": "\"", "#": "№", "$": ";", "^": ":", "&": "?",

    # Russian to English
    "й": "q", "ц": "w", "у": "e", "к": "r", "е": "t", "н": "y", "г": "u",
    "ш": "i", "щ": "o", "з": "p", "х": "[", "ъ": "]", "ф": "a", "ы": "s",
    "в": "d", "а": "f", "п": "g", "р": "h", "о": "j", "л": "k", "д": "l",
    "ж": ";", "э": "'", "/": "|", "я": "z", "ч": "x", "с": "c", "м": "v",
    "и": "b", "т": "n", "ь": "m", "б": ",", "ю": ".", ".": "/",
    "\"": "@", "№": "#", ";": "$", ":": "^", "?": "&",
}


async def invert_layout(message: str) -> None:
    result = ""
    for character in message:
        try:
            result += invert[character.lower()]
        except KeyError:
            result += character

    return result


async def layout_command(message: Message) -> None:
    if not message.reply_to_message:
        await message.reply(
            html.bold('🚫 Необходимо ответить на целевое сообщение.'))
        return

    if not message.reply_to_message.text:
        if not message.reply_to_message.caption:
            await message.reply(
                html.bold('🚫 Целевое сообщение не содержит текста.'))
            return
        else:
            msg = message.reply_to_message.caption
    else:
        msg = message.reply_to_message.text

    processed_msg = await invert_layout(msg)
    await message.reply(
        html.italic(html.quote("🗣️ " + processed_msg)))
