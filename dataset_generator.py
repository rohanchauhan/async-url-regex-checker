import re
import csv
import random
import pickle

# Common Regular Expressions
RE_COMMON_EMAIL_ID = r"/^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})*$/"
RE_UNCOMMON_EMAIL_ID = r"/^([a-z0-9_\.\+-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/"
RE_PHONE = r"/^(?:(?:\(?(?:00|\+)([1-4]\d\d|[1-9]\d?)\)?)?[\-\.\ \\\/]?)?((?:\(?\d{1,}\)?[\-\.\ \\\/]?){0,})(?:[\-\.\ \\\/]?(?:#|ext\.?|extension|x)[\-\.\ \\\/]?(\d+))?$/"
RE_LINK = r'href="(.*?)"'
RE_IMG = r"<img([\w\W]+?)/>"

# Making a list of regular expression
LIST_OF_RE = [RE_COMMON_EMAIL_ID, RE_UNCOMMON_EMAIL_ID, RE_PHONE, RE_LINK, RE_IMG]
l = len(LIST_OF_RE)

"""

Dataset of urls 'ae.csv' downloaded from Citizen Lab and Others. 2014. 
URL Testing Lists Intended for Discovering Website Censorship.
https://github.com/citizenlab/test-lists.

format of 'ae.csv': 
url,category_code,category_description,date_added,source,notes

"""

"""
dataset is a list which contains tuples of (url,[regular expressions])

Each url is coupled with a list of regular expressions randomly
selected from LIST_OF_RE.

This dataset is used for testing final program.
"""

dataset = []
with open("ae.csv") as csvfile:
	data = csv.DictReader(csvfile)
	for row in data:
		regex_list = random.sample(LIST_OF_RE,random.randint(1,l))
		dataset.append((row['url'], regex_list))

# Dumping object using pickle
with open('dataset.pickle', 'wb') as f:
    pickle.dump(dataset, f)


	