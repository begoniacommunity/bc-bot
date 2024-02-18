import time
import pickle
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger
from main import botID
from .markov import avg_transition_prob

english_to_cyrillic = {
    "q": "й", "w": "ц", "e": "у", "r": "к", "t": "е", "y": "н", "u": "г", "i": "ш", "o": "щ", "p": "з", "[": "х",
    "]": "ъ", "a": "ф", "s": "ы", "d": "в", "f": "а", "g": "п", "h": "р", "j": "о", "k": "л", "l": "д", ";": "ж",
    "'": "э", "z": "я", "x": "ч", "c": "с", "v": "м", "b": "и", "n": "т", "m": "ь", ",": "б", ".": "ю", "/": ".",
    " ": " "
}
allowed_detector_letters = [key for key in english_to_cyrillic.keys()]

logger.debug("Loading model...")
start = time.perf_counter()
try:
    with open('static/gib_model.pki', 'rb') as model_file:
        model_data = pickle.load(model_file)
except FileNotFoundError:
    logger.error("Model file not found.")
    logger.info("Please run model_trainer.py (located at ./handlers/cyrillic/markov) to generate the model file")
    logger.info("Model file should be at static/gib_model.pki")
    exit(1)
model_mat = model_data['mat']
threshold = model_data['thresh']
end = time.perf_counter()
logger.debug(f"Model loaded in {end - start} seconds")
del start, end


def gibberish_detector(text: str) -> bool:
    """Detects if a text is gibberish
    Returns false if text is valid, true if text is gibberish"""
    return avg_transition_prob(text, model_mat) < threshold


async def cyrillic_processor(message: Message, being_called_from_autodetect: bool = False):
    """Converts Latin characters to cyrillic characters."""
    if not message.reply_to_message and not being_called_from_autodetect:
        await message.reply("Используйте эту команду ответом на целевые сообщения")
        return

    if not being_called_from_autodetect:
        target_message = message.reply_to_message
        if target_message.from_user.id == botID:
            await message.reply("Ты совсем ебобо?")
            return
    else:
        target_message = message

    result = "Перевод: "
    errored = False
    for character in target_message.text:
        try:
            result += english_to_cyrillic[character.lower()]
        except KeyError:
            result += character
            errored = True

    if errored:
        result.replace("Перевод: ", "Частичный перевод: ")

    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Удалить", callback_data='delete')],
        ]
    )
    await target_message.reply(result, reply_markup=reply_markup)


async def wrong_layout_detector(message: Message):
    """Detects if a message is likely to have been typed with a wrong layout"""
    for letter in message.text:
        if letter.lower() not in allowed_detector_letters:
            return
    if gibberish_detector(message.text):
        await cyrillic_processor(message, True)
