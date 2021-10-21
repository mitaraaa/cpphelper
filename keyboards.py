import json
from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton

# Select language
def select_language():
	select_language_ru = InlineKeyboardButton("RU 🌐", callback_data="button_ru")
	select_language_en = InlineKeyboardButton("EN 🌐", callback_data="button_en")
	return InlineKeyboardMarkup().add(select_language_ru).row(select_language_en)

def menu(locale):
	markup = InlineKeyboardMarkup()
	markup.add(InlineKeyboardButton(locale["basics"], callback_data="button_menu_basics"))
	markup.add(InlineKeyboardButton(locale["functions"], callback_data="button_menu_functions"))
	markup.add(InlineKeyboardButton(locale["pointers"], callback_data="button_menu_pointers"))
	markup.add(InlineKeyboardButton(locale["object_oriented_lang"], callback_data="button_menu_object_oriented_lang"))
	markup.add(InlineKeyboardButton(locale["exceptions"], callback_data="button_menu_exceptions"))
	markup.add(InlineKeyboardButton(locale["containers"], callback_data="button_menu_containers"))
	markup.add(InlineKeyboardButton(locale["streams"], callback_data="button_menu_streams"))
	markup.add(InlineKeyboardButton(locale["patterns"], callback_data="button_menu_patterns"))
	return markup