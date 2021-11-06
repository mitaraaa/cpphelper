import json


ru_directory = "locales/ru"
en_directory = "locales/en"

# List of all opened files
file_handles = []

# Sends json data into variables
try:
	file_handles.append(open(f"{ru_directory}/basics.json", "r", encoding="utf-8"))
	RU_BASICS = json.load(file_handles[0])
	file_handles.append(open(f"{ru_directory}/navigation.json", "r", encoding="utf-8"))
	RU_NAV = json.load(file_handles[1])
	file_handles.append(open(f"{ru_directory}/menu.json", "r", encoding="utf-8"))
	RU_MENU = json.load(file_handles[2])
	file_handles.append(open(f"{ru_directory}/functions.json", "r", encoding="utf-8"))
	RU_FUNCTIONS = json.load(file_handles[3])
	file_handles.append(open(f"{ru_directory}/pointers.json", "r", encoding="utf-8"))
	RU_POINTERS = json.load(file_handles[4])
	file_handles.append(open(f"{ru_directory}/object_oriented_lang.json", "r", encoding="utf-8"))
	RU_OOP = json.load(file_handles[5])
	file_handles.append(open(f"{ru_directory}/exceptions.json", "r", encoding="utf-8"))
	RU_EXCEPTIONS = json.load(file_handles[6])
	file_handles.append(open(f"{ru_directory}/containers.json", "r", encoding="utf-8"))
	RU_CONTAINERS = json.load(file_handles[7])
	file_handles.append(open(f"{ru_directory}/streams.json", "r", encoding="utf-8"))
	RU_STREAMS = json.load(file_handles[8])
	file_handles.append(open(f"{ru_directory}/patterns.json", "r", encoding="utf-8"))
	RU_PATTERNS = json.load(file_handles[9])

	file_handles.append(open(f"{en_directory}/basics.json", "r", encoding="utf-8"))
	EN_BASICS = json.load(file_handles[10])
	file_handles.append(open(f"{en_directory}/navigation.json", "r", encoding="utf-8"))
	EN_NAV = json.load(file_handles[11])
	file_handles.append(open(f"{en_directory}/menu.json", "r", encoding="utf-8"))
	EN_MENU = json.load(file_handles[12])
	file_handles.append(open(f"{en_directory}/functions.json", "r", encoding="utf-8"))
	EN_FUNCTIONS = json.load(file_handles[13])
	file_handles.append(open(f"{en_directory}/pointers.json", "r", encoding="utf-8"))
	EN_POINTERS = json.load(file_handles[14])
	file_handles.append(open(f"{en_directory}/object_oriented_lang.json", "r", encoding="utf-8"))
	EN_OOP = json.load(file_handles[15])
	file_handles.append(open(f"{en_directory}/exceptions.json", "r", encoding="utf-8"))
	EN_EXCEPTIONS = json.load(file_handles[16])
	file_handles.append(open(f"{en_directory}/containers.json", "r", encoding="utf-8"))
	EN_CONTAINERS = json.load(file_handles[17])
	file_handles.append(open(f"{en_directory}/streams.json", "r", encoding="utf-8"))
	EN_STREAMS = json.load(file_handles[18])
	file_handles.append(open(f"{en_directory}/patterns.json", "r", encoding="utf-8"))
	EN_PATTERNS = json.load(file_handles[19])

	
# Closes all files
finally:
	for file in file_handles:
		file.close()