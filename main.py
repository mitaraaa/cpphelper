import os
import json
import asyncio
import pickle

from aiogram import Bot, Dispatcher, executor, types
import keyboards

bot = Bot(os.environ["TOKEN"])
dp = Dispatcher(bot)

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

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("button"))
async def process_callback_button(callback_query: types.CallbackQuery):
	cb = callback_query.data
	if cb == "button_ru" or cb == "button_en":
		data = read_pickle()
		with open("locales.pickle", "wb") as file:
			locale_str = "ru" if cb == "button_ru" else "en"
			data[callback_query.from_user.id] = locale_str
			locale = locale_ru if locale_str == "ru" else locale_str == "en"
			pickle.dump(data, file)
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, "Выбран язык: Русский" if cb == "button_ru" else "Picked language: English")
		await bot.send_message(callback_query.from_user.id, locale["menu"]["pick_category"], reply_markup=keyboards.menu(locale["menu"]))

	elif cb.startswith("button_menu"):
		pass

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
	await bot.send_message(message.from_user.id, "Select language / Выберите язык", reply_markup=keyboards.select_language())	

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)