#!/usr/bin/python3

import re
import os
from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen


orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)
def prettify(self, encoding=None, formatter="minimal", indent_width=2):
	return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
BeautifulSoup.prettify = prettify

def get_html(u):
	s = ""
	if "://" in u:
		s = urlopen(u).read().decode("utf-8")
	else:
		s = open(u, "r").read()
	return BeautifulSoup(s, "html.parser")

def extract(elements):
	for e in elements:
		e.extract()

def strip(h):
	extract(h.find_all("div", id="header"))
	extract(h.find_all("div", class_="search_bar"))
	extract(h.find_all("ul", class_="sub-navigation"))
	extract(h.find_all("div", class_="sidebar"))
	extract(h.find_all("div", id="footer"))
	extract(h.find_all(text=lambda text:isinstance(text, Comment)))
	extract(h.find_all("script"))
	for link in h.find_all("link"):
		if "stylesheet" in link["rel"] and "online.css" in link["href"]:
			link["href"] = "online.css"
		else:
			link.decompose()

def main():
	docs = "docs/"
	url = "http://doc.qt.io/qt-5/"
	minimal = True
	restrip_local = False
	paths = [x for x in open("files.txt", "r").read().split("\n") if len(x) > 3]
	files404 = [x for x in open("404.txt", "r").read().split("\n") if len(x) > 3]
	for path in paths:
		print(path + " ", end="")
		if path not in files404:
			if os.path.exists(docs+path):
				h = get_html(docs+path)
				print("(" + "local" + ")")
			else:
				h = get_html(url+path)
				print("(" + "online" + ")")
			if restrip_local:
				strip(h)
			txt = ""
			if minimal:
				txt = h.prettify(indent_width=0).replace("\n"," ")
			else:
				txt = h.prettify(indent_width=2)
			open(docs+path, "w").write(txt)

if __name__ == '__main__':
	main()
