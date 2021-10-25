import os
import json

ru_directory = "locales/ru"
en_directory = "locales/en"

file_handles = []

try:
	file_handles.append(open(f"{ru_directory}/basics.json", "r", encoding="utf-8"))
	RU_BASICS = json.load(file_handles[0])
	file_handles.append(open(f"{ru_directory}/navigation.json", "r", encoding="utf-8"))
	RU_NAV = json.load(file_handles[1])
	file_handles.append(open(f"{ru_directory}/menu.json", "r", encoding="utf-8"))
	RU_MENU = json.load(file_handles[2])

	file_handles.append(open(f"{en_directory}/basics.json", "r", encoding="utf-8"))
	EN_BASICS = json.load(file_handles[3])
	file_handles.append(open(f"{en_directory}/navigation.json", "r", encoding="utf-8"))
	EN_NAV = json.load(file_handles[4])
	file_handles.append(open(f"{en_directory}/menu.json", "r", encoding="utf-8"))
	EN_MENU = json.load(file_handles[5])
	
finally:
	for file in file_handles:
		file.close()