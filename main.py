import os
import redis
import logging

import rich
from rich.logging import RichHandler

from emoji import emojize
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import MessageNotModified

import localization as lang
from keyboards import *
from utils import *

# Connects to Redis database
db = redis.from_url(os.environ.get("REDIS_URL"))

# Creates bot and dispatcher instances
bot = Bot(os.environ["TOKEN"])
dp = Dispatcher(bot)

# Logging
FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
log = logging.getLogger("rich")

# Navigation handler
@dp.callback_query_handler(cb_nav.filter(name="navigation_prev_page"))
@dp.callback_query_handler(cb_nav.filter(name="navigation_next_page"))
async def process_navigation(callback_query: types.CallbackQuery, callback_data: dict):
	try:
		page = int(callback_data["current_page"]) + 1 if callback_data["name"] == "navigation_next_page" else int(callback_data["current_page"]) - 1
		article = parse_path(callback_data["article"])[f"page_{page}"]
		await edit_message_nav(bot, parse_article(article), callback_query, callback_data["article"], page)
	except KeyError:
		text = locale.navigation["err_last"] if page > int(callback_data["current_page"]) else locale.navigation["err_first"]
		await bot.answer_callback_query(callback_query_id=callback_query.id, text=text)

# "To menu" button handler
@dp.callback_query_handler(lambda c: c.data == "navigation_to_menu")
async def process_navigation_to_menu(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	await edit_message(bot, emojize(locale.menu["name"]), callback_query, locale.menu)

# Language selector handler
@dp.callback_query_handler(lambda c: c.data == "lang_en")
@dp.callback_query_handler(lambda c: c.data == "lang_ru")
async def process_language(callback_query: types.CallbackQuery):
	language = "ru" if callback_query == "lang_ru" else "en"
	db.set(callback_query.from_user.id, language)
	locale.set_lang(language)

	await bot.edit_message_text(
			text=("Выбран язык: Русский" if language == "ru" else "Picked language: English"), 
			message_id=callback_query.message.message_id, 
			chat_id=callback_query.from_user.id
			)
	await bot.send_message(callback_query.from_user.id, emojize(locale.menu["name"], use_aliases=True), reply_markup=menu(locale.menu))

# Handles all callbacks except navigation
@dp.callback_query_handler(lambda c: True)
async def process_callback_button(callback_query: types.CallbackQuery):
	query_text = callback_query.data
	if query_text.startswith("menu"):
		if query_text == "menu_basics":
			await edit_message(bot, "".join(locale.basics["name"] + '\n' + locale.basics["overview"]), callback_query, locale.basics)
	else:
		for attr in get_attrs():
			if query_text.startswith(attr):
				qt = query_text.split('_')
				qt.pop(0)
				qt = '_'.join(qt)
				for article in getattr(locale, attr).keys():
					if article == qt:
						await edit_message_nav(bot, parse_article(getattr(locale, attr)[article]["page_1"]), callback_query, attr + '.' + article, 1)
	await bot.answer_callback_query(callback_query.id)

# Skip NotModified exception
@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    return True

# On /start message
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
	await bot.send_message(
		message.from_user.id,
		emojize("Select language / Выберите язык :earth_asia:", use_aliases=True), 
		reply_markup=select_language()
		)

# TODO Add /search command
# TODO Add /pattern command
# TODO Fill localization files

# Starts bot
if __name__ == "__main__":
	executor.start_polling(dp)