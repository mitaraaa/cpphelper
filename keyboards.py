from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from emoji import emojize


# Creates callback
def _get_callback_name(name, key):
	callback = "".join(name + "_" + key)
	return callback

# Select language
def select_language():
	markup = InlineKeyboardMarkup()
	select_language_ru = InlineKeyboardButton(emojize("RU :Russia:", use_aliases=True), callback_data="lang_ru")
	select_language_en = InlineKeyboardButton(emojize("EN :United_Kingdom:", use_aliases=True), callback_data="lang_en")
	markup.add(select_language_ru, select_language_en)
	return markup

# Main menu
def menu(menu):
	markup = InlineKeyboardMarkup()
	for key in menu.keys():
		if key == "name": continue
		markup.add(InlineKeyboardButton(menu[key], callback_data=_get_callback_name("menu", key)))
	return markup

# Generates keyboard from json
def generate_keyboard(locale):
	markup = InlineKeyboardMarkup()
	for key in locale.keys():
		if key == "id" or key == "name" or key == "overview": continue
		markup.add(InlineKeyboardButton(locale[key]["name"], callback_data=_get_callback_name(locale["id"], key)))
	return markup

# Custom callback
cb_nav = CallbackData("nav", "name", "article", "current_page", sep="#")

# Navigation in articles
def navigation(navigation, article, current_page):
	markup = InlineKeyboardMarkup(row_width=3)
	markup.row(
		InlineKeyboardButton(emojize(navigation["prev_page"], use_aliases=True), callback_data=cb_nav.new(name="navigation_prev_page", article=article, current_page=current_page)),
		InlineKeyboardButton(emojize(navigation["to_menu"], use_aliases=True), callback_data="navigation_to_menu"), 
		InlineKeyboardButton(emojize(navigation["next_page"], use_aliases=True), callback_data=cb_nav.new(name="navigation_next_page", article=article, current_page=current_page))
		)
	return markup