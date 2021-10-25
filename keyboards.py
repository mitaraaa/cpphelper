from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

def create_callback(locales):
	pass

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
	markup.add(InlineKeyboardButton(menu["basics"], callback_data="button_menu_basics"))
	markup.add(InlineKeyboardButton(menu["functions"], callback_data="button_menu_functions"))
	markup.add(InlineKeyboardButton(menu["pointers"], callback_data="button_menu_pointers"))
	markup.add(InlineKeyboardButton(menu["object_oriented_lang"], callback_data="button_menu_object_oriented_lang"))
	markup.add(InlineKeyboardButton(menu["exceptions"], callback_data="button_menu_exceptions"))
	markup.add(InlineKeyboardButton(menu["containers"], callback_data="button_menu_containers"))
	markup.add(InlineKeyboardButton(menu["streams"], callback_data="button_menu_streams"))
	markup.add(InlineKeyboardButton(menu["patterns"], callback_data="button_menu_patterns"))
	return markup

def basics(basics):
	markup = InlineKeyboardMarkup()
	markup.add(InlineKeyboardButton(basics["variables"]["name"], callback_data="button_basics_variables"))
	markup.add(InlineKeyboardButton(basics["data_types"]["name"], callback_data="button_basics_data_types"))
	markup.add(InlineKeyboardButton(basics["static_typization"]["name"], callback_data="button_basics_static_typization"))
	markup.add(InlineKeyboardButton(basics["constants"]["name"], callback_data="button_basics_constants"))
	markup.add(InlineKeyboardButton(basics["arithmetical_operations"]["name"], callback_data="button_basics_arithmetical_operations"))
	markup.add(InlineKeyboardButton(basics["console_io"]["name"], callback_data="button_basics_console_io"))
	markup.add(InlineKeyboardButton(basics["conditional_constructions"]["name"], callback_data="button_basics_conditional_constructions"))
	markup.add(InlineKeyboardButton(basics["bit_operations"]["name"], callback_data="button_basics_bit_operations"))
	markup.add(InlineKeyboardButton(basics["logical_operations"]["name"], callback_data="button_basics_logical_operations"))
	markup.add(InlineKeyboardButton(basics["loops"]["name"], callback_data="button_basics_loops"))
	markup.add(InlineKeyboardButton(basics["links"]["name"], callback_data="button_basics_links"))
	markup.add(InlineKeyboardButton(basics["arrays"]["name"], callback_data="button_basics_arrays"))
	markup.add(InlineKeyboardButton(basics["strings"]["name"], callback_data="button_basics_strings"))
	markup.add(InlineKeyboardButton(basics["namespaces"]["name"], callback_data="button_basics_namespaces"))
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