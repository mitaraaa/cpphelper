import json
from emoji import emojize
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Select language
def select_language():
	markup = InlineKeyboardMarkup()
	select_language_ru = InlineKeyboardButton(emojize("RU :russia:", use_aliases=True), callback_data="button_ru")
	select_language_en = InlineKeyboardButton(emojize("EN :uk:", use_aliases=True), callback_data="button_en")
	markup.add(select_language_ru, select_language_en)
	return markup

def menu(menu):
	markup = InlineKeyboardMarkup()
	markup.add(InlineKeyboardButton(menu["basics"], callback_data="button_menu_basics"))
	markup.add(InlineKeyboardButton(menu["functions"], callback_data="button_menu_functions"))
	markup.add(InlineKeyboardButton(menu["pointers"], callback_data="button_menu_pointers"))
	markup.add(InlineKeyboardButton(menu["object_oriented_lang"], callback_data="button_menu_object_oriented_lang"))
	markup.add(InlineKeyboardButton(menu["exceptions"], callback_data="button_menu_exceptions"))
	markup.add(InlineKeyboardButton(menu["containers"], callback_data="button_menu_containers"))
	markup.add(InlineKeyboardButton(menu["streams"], callback_data="button_menu_streams"))
	markup.add(InlineKeyboardButton(menu["patterns"], callback_data="button_menu_patterns"))
	return markup

def navigation(locale):
	markup = InlineKeyboardMarkup(row_width=3)
	markup.row(
		InlineKeyboardButton(emojize(locale["prev_page"], use_aliases=True), callback_data="button_navigation_prev_page"),
		InlineKeyboardButton(emojize(locale["to_menu"], use_aliases=True), callback_data="button_navigation_to_menu"), 
		InlineKeyboardButton(emojize(locale["next_page"], use_aliases=True), callback_data="button_navigation_next_page")
		)
	return markup