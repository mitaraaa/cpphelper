import os
import pickle
from aiohttp.helpers import current_task

from emoji import emojize
from aiogram import Bot, Dispatcher, executor, types

import localization as lang
import keyboards

bot = Bot(os.environ["TOKEN"])
dp = Dispatcher(bot)
current_page = []


# Read from locales.pickle dictionary of locales
def read_pickle():
	with open("locales.pickle", "rb") as file_r:
		while True:
			try:
				data = pickle.load(file_r)
			except EOFError:
				break
	return data

# Combines all strings from json into one
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
	global current_page

	if query_text == "button_ru" or query_text == "button_en":
		with open("locales.pickle", "wb") as file:
			locale_str = "ru" if query_text == "button_ru" else "en"
			data[user_id] = locale_str
			menu = lang.RU_MENU if locale_str == "ru" else lang.EN_MENU
			pickle.dump(data, file)
		await bot.edit_message_text(
			text=("Выбран язык: Русский" if query_text == "button_ru" else "Picked language: English"), 
			message_id=callback_query.message.message_id, 
			chat_id=user_id
			)
		await bot.send_message(user_id, emojize(menu["name"], use_aliases=True), reply_markup=keyboards.menu(menu))

	l = True if data[user_id] == "ru" else False
	menu = lang.RU_MENU if l else lang.EN_MENU
	navigation = lang.RU_NAV if l else lang.EN_NAV
	basics = lang.RU_BASICS  if l else lang.EN_BASICS

	if query_text.startswith("button_navigation"):
		if query_text == "button_navigation_to_menu": 
			await bot.edit_message_text(
					text=emojize(menu["name"], 
					use_aliases=True), 
					message_id=callback_query.message.message_id, 
					chat_id=user_id, 
					reply_markup=keyboards.menu(menu)
				)
		else:
			try:
				page = int(current_page[1]) + 1 if query_text == "button_navigation_next_page" else int(current_page[1]) - 1
				next_page = current_page[0][f"page_{page}"]
				text = parse_article(next_page)
				await bot.edit_message_text(
					text=text, 
					parse_mode="markdown", 
					message_id=callback_query.message.message_id, 
					chat_id=user_id, 
					reply_markup=keyboards.navigation(navigation)
				)
				current_page[1] = page
			except KeyError:
				text = navigation["err_last"] if page > current_page[1] else navigation["err_first"]
				await bot.answer_callback_query(callback_query_id=callback_query.id,text=text)
				return

	if query_text.startswith("button_menu"):
		if query_text == "button_menu_basics":
			text = "".join(basics["name"] + '\n' + basics["overview"])
			await bot.edit_message_text(
					text=text, 
					parse_mode="markdown", 
					message_id=callback_query.message.message_id, 
					chat_id=user_id, 
					reply_markup=keyboards.generate_keyboard(basics)
				)

	if query_text.startswith("button_basics"):
		if query_text == "button_basics_data_types":
			current_page = [basics["data_types"], 1]
			await bot.edit_message_text(
					text=parse_article(basics["data_types"]["page_1"]), 
					parse_mode="markdown", 
					message_id=callback_query.message.message_id, 
					chat_id=user_id, 
					reply_markup=keyboards.navigation(navigation)
			)
	await bot.answer_callback_query(callback_query.id)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
	await bot.send_message(
		message.from_user.id,
		emojize("Select language / Выберите язык :earth_asia:", use_aliases=True), 
		reply_markup=keyboards.select_language()
		)

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)