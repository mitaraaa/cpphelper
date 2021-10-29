import os
import pickle
from jsonpath_ng import jsonpath, parse

from emoji import emojize

from aiogram.utils.callback_data import CallbackData
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import localization as lang
import keyboards
from utils import parse_article, read_pickle

bot = Bot(os.environ["TOKEN"])
dp = Dispatcher(bot, storage=MemoryStorage())

cb = CallbackData("nav", "name", "article", "current_page", sep="#")
menu = {}
navigation = {}
basics = {}

def parse_path(path):
	path = path.split('.')
	if path[0] == "basics": 
		dct = basics
	else:
		raise KeyError
	path.pop(0)
	for p in path:
		dct = dct[p]
	return dct

def set_lang(selected_language):
	global menu, navigation, basics
	menu = lang.RU_MENU if selected_language == "ru" else lang.EN_MENU
	navigation = lang.RU_NAV if selected_language == "ru" else lang.EN_NAV
	basics = lang.RU_BASICS if selected_language == "ru" else lang.EN_BASICS

async def edit_message(text, callback_query, keyboard):
	if keyboard == menu:
		kb = keyboards.menu(menu)
	else:
		kb = keyboards.generate_keyboard(keyboard)
	
	await bot.edit_message_text(
		text=text, 
		parse_mode="markdown", 
		message_id=callback_query.message.message_id, 
		chat_id=callback_query.from_user.id, 
		reply_markup=kb
	)

async def edit_message_nav(text, callback_query, article, current_page):
	kb = keyboards.navigation(navigation, article, current_page)
	await bot.edit_message_text(
		text=text, 
		parse_mode="markdown", 
		message_id=callback_query.message.message_id, 
		chat_id=callback_query.from_user.id, 
		reply_markup=kb
	)


@dp.callback_query_handler(cb.filter(name="navigation_prev_page"))
@dp.callback_query_handler(cb.filter(name="navigation_next_page"))
async def process_navigation(callback_query: types.CallbackQuery, callback_data: dict):
	try:
		page = int(callback_data["current_page"]) + 1 if callback_data["name"] == "navigation_next_page" else int(callback_data["current_page"]) - 1
		print(parse_path(callback_data["article"]))
		article = parse_path(callback_data["article"])[f"page_{page}"]
		await edit_message_nav(parse_article(article), callback_query, callback_data["article"], page)
	except KeyError:
		text = navigation["err_last"] if page > int(callback_data["current_page"]) else navigation["err_first"]
		await bot.answer_callback_query(callback_query_id=callback_query.id, text=text)


@dp.callback_query_handler(cb.filter(name="navigation_to_menu"))
async def process_navigation_to_menu(callback_query: types.CallbackQuery):
	bot.answer_callback_query()
	await edit_message(emojize(menu["name"]), callback_query, menu)


@dp.callback_query_handler(lambda c: c.data == "lang_en")
@dp.callback_query_handler(lambda c: c.data == "lang_ru")
async def process_language(callback_query: types.CallbackQuery):
	user_data = read_pickle()
	with open("locales.pickle", "wb") as file:
		user_data[callback_query.from_user.id] = "ru" if callback_query.data == "lang_ru" else "en"
		set_lang(user_data[callback_query.from_user.id])
		pickle.dump(user_data, file)
	await bot.edit_message_text(
			text=("Выбран язык: Русский" if callback_query.data == "lang_ru" else "Picked language: English"), 
			message_id=callback_query.message.message_id, 
			chat_id=callback_query.from_user.id
			)
	await bot.send_message(callback_query.from_user.id, emojize(menu["name"], use_aliases=True), reply_markup=keyboards.menu(menu))


@dp.callback_query_handler(lambda c: True)
async def process_callback_button(callback_query: types.CallbackQuery):
	query_text = callback_query.data
	if query_text.startswith("menu"):
		if query_text == "menu_basics":
			await edit_message("".join(basics["name"] + '\n' + basics["overview"]), callback_query, basics)

	if query_text.startswith("basics"):
		if query_text == "basics_data_types":
			await edit_message_nav(parse_article(basics["data_types"]["page_1"]), callback_query, "basics.data_types", 1)
	await bot.answer_callback_query(callback_query.id)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
	await bot.send_message(
		message.from_user.id,
		emojize("Select language / Выберите язык :earth_asia:", use_aliases=True), 
		reply_markup=keyboards.select_language()
		)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
	executor.start_polling(dp, on_shutdown=shutdown)