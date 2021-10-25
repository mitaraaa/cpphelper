from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

def create_callback(name, key):
	callback = "".join("button_" + name + "_" + key)
	return callback

# Select language
def select_language():
	markup = InlineKeyboardMarkup()
	select_language_ru = InlineKeyboardButton(emojize("RU :Russia:", use_aliases=True), callback_data="button_ru")
	select_language_en = InlineKeyboardButton(emojize("EN :United_Kingdom:", use_aliases=True), callback_data="button_en")
	markup.add(select_language_ru, select_language_en)
	return markup

# Main menu
def menu(menu):
	markup = InlineKeyboardMarkup()
	for key in menu.keys():
		if key == "name": continue
		markup.add(InlineKeyboardButton(menu[key], callback_data=create_callback("menu", key)))
	return markup

# Generates keyboard from json
def generate_keyboard(locale):
	markup = InlineKeyboardMarkup()
	for key in locale.keys():
		if key == "id" or key == "name" or key == "overview": continue
		markup.add(InlineKeyboardButton(locale[key]["name"], callback_data=create_callback(locale["id"], key)))
	return markup

# Navigation in articles
def navigation(locale):
	markup = InlineKeyboardMarkup(row_width=3)
	markup.row(
		InlineKeyboardButton(emojize(locale["prev_page"], use_aliases=True), callback_data="button_navigation_prev_page"),
		InlineKeyboardButton(emojize(locale["to_menu"], use_aliases=True), callback_data="button_navigation_to_menu"), 
		InlineKeyboardButton(emojize(locale["next_page"], use_aliases=True), callback_data="button_navigation_next_page")
		)
	return markup