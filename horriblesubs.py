import os
import requests
from bs4 import BeautifulSoup
import re
import urllib.request

nameList = []
hrefStrings = ""
linksDict = {}

startPage = requests.get("https://horriblesubs.info/shows/")

soup = BeautifulSoup(startPage.text, features="html.parser")

for div in soup.find_all(class_="shows-wrapper"):
	aTags = div.find_all("a", href=True)
	for line in aTags:
		linksDict[line.text] = line['href']

#choose by dropdown, chose name
chosenAnime = "Sword Art Online – Alicization"

req = urllib.request.Request("https://horriblesubs.info" + linksDict.get(chosenAnime), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'})

chosenPage = urllib.request.urlopen(req)

showsoup = BeautifulSoup(chosenPage, features="html.parser")

print(showsoup.text)

quality = "1080p"
for div in showsoup.find_all(class_="hs-shows"):
	print(div)
	for x in div.find_all(class_="link-1080p"):
		print(x)
		for y in x.find_all(class_="hs-magnet-link"):
			print(y)


"""
TODO

DYNAMICALLY LOADED ELEMENTS IN PAGES (NEED TO EMULATE OURSELF AS A BROWSER/CLIENT AND LOAD THE JS FOR THE PAGE IN ORDER TO LOAD THE LINKS)

FIND A GUI LIBRARY TO USE YOUR PROGRAM MORE EASILY



"""
