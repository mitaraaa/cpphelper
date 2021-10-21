import os
import json
import pickle

from emoji import emojize
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import update, user
import keyboards

bot = Bot(os.environ["TOKEN"])
dp = Dispatcher(bot)

# Localisation files
locale_ru = json.load(open("locales/ru.json", "r", encoding="utf-8"))
locale_en = json.load(open("locales/en.json", "r", encoding="utf-8"))

# Read from locales.pickle dictionary of locales
def read_pickle():
	with open("locales.pickle", "rb") as file_r:
		while True:
			try:
				data = pickle.load(file_r)
			except EOFError:
				break
	return data

def parse_article(article):
	text = ""
	for line in article:
		text += article[line] + "\n"
	return text

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("button"))
async def process_callback_button(callback_query: types.CallbackQuery):
	user_id = callback_query.from_user.id
	query_text = callback_query.data
	data = read_pickle()

	if query_text == "button_ru" or query_text == "button_en":
		with open("locales.pickle", "wb") as file:
			locale_str = "ru" if query_text == "button_ru" else "en"
			data[user_id] = locale_str
			menu = locale_ru["menu"] if locale_str == "ru" else locale_en["menu"]
			pickle.dump(data, file)
		await bot.edit_message_text(text=("Выбран язык: Русский" if query_text == "button_ru" else "Picked language: English"), message_id=callback_query.message.message_id, chat_id=user_id)
		await bot.send_message(user_id, emojize(menu["pick_category"], use_aliases=True), reply_markup=keyboards.menu(menu))

	locale = locale_ru if data[user_id] == "ru" else locale_en
	if query_text.startswith("button_navigation"):
		if query_text == "button_navigation_prev_page": pass
		elif query_text == "button_navigation_to_menu": await bot.edit_message_text(text=emojize(locale["menu"]["pick_category"], use_aliases=True), message_id=callback_query.message.message_id, chat_id=user_id, reply_markup=keyboards.menu(locale["menu"]))
		elif query_text == "button_navigation_next_page": pass

	if query_text.startswith("button_menu"):
		articles = locale["articles"]
		navigation = locale["navigation"]
		if query_text == "button_menu_basics":
			await bot.edit_message_text(text=parse_article(articles["basics"]), message_id=callback_query.message.message_id, chat_id=user_id, reply_markup=keyboards.navigation(navigation))

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
	await bot.send_message(message.from_user.id, emojize("Select language / Выберите язык :earth_asia:", use_aliases=True), reply_markup=keyboards.select_language())	

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)