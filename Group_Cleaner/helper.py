from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json

keyboards = {
    "start_he": InlineKeyboardMarkup([
        [InlineKeyboardButton("לערוץ עדכוני רובוטים 🍕", url='t.me/m100achuzBots')],
        [InlineKeyboardButton('English 🇺🇸', callback_data='start_en')]]),

    "start_en": InlineKeyboardMarkup([
        [InlineKeyboardButton("Bot updates channel 🎂", url='t.me/m100achuzBots')],
        [InlineKeyboardButton('עברית 🇮🇱', callback_data='start_he')]]),

    "help_he": InlineKeyboardMarkup([[
        InlineKeyboardButton('English 🇺🇸', callback_data='help_en')]]),

    "help_en": InlineKeyboardMarkup([[
        InlineKeyboardButton('עברית 🇮🇱', callback_data='help_he')]]),
}


def json_load(file: str) -> json:
    """" func for read and load json file's """
    return json.load(open(file, 'r', encoding='UTF-8'))


def json_dump(var: object, file: str) -> bool:
    """ func for dump json object's to json file's """
    with open(file, 'w', encoding='UTF-8') as file_write:
        json.dump(var, file_write, indent=4)
