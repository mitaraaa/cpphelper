import pickle
import gzip

# Read from locales.pickle dictionary of locales
def read_pickle():
	data = { }
	with gzip.open("locales.pickle", "rb") as file_r:
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