import os
import requests
from bs4 import BeautifulSoup
import time

nameList = []
hrefStrings = ""
linksDict = {}
quality = ""

landingurl = "https://horriblesubs.info/"

startPage = requests.get(landingurl + "shows/")

soup = BeautifulSoup(startPage.text, features="html.parser")

for div in soup.find_all(class_="shows-wrapper"):
	aTags = div.find_all("a", href=True)
	for line in aTags:
		linksDict[line.text] = line['href']

#choose by dropdown, chose name
chosenAnime = "Sword Art Online – Alicization"

url = "https://horriblesubs.info" + linksDict.get(chosenAnime)

# req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'})

# chosenPage = urllib.request.urlopen(req)

showsoup = BeautifulSoup(requests.get(url).text, features="html.parser")

scriptList = showsoup.find_all("script")

for tag in scriptList:
	# print(tag.text)
	if "hs_showid" in tag.text:
		showid = tag.text[16:-1]


apiLink = "api.php?method=getshows&type=show&showid=" + showid

nextid = 0
test = 0
while True:
	loadedPage = requests.get(landingurl + apiLink + "&nextid=" + str(nextid))
	if loadedPage.text == 'DONE':
		print("hello")
		break

	loadedSoup = BeautifulSoup(loadedPage.text,features="html.parser")

	quality = "1080p"

	for span in loadedSoup.find_all(class_="link-" + quality):
		for x in span.find_all(class_="hs-magnet-link"):
			for y in x.find_all("a", href=True):
				os.startfile(str(y["href"]))
				print(test)
				test+=1
				break
	nextid += 1

# quality = "1080p"
# for div in showsoup.find_all(class_="hs-shows"):
# 	print(div)
# 	for x in div.find_all(class_="link-1080p"):
# 		print(x)
# 		for y in x.find_all(class_="hs-magnet-link"):
# 			print(y)


"""
TODO

DYNAMICALLY LOADED ELEMENTS IN PAGES (NEED TO EMULATE OURSELF AS A BROWSER/CLIENT AND LOAD THE JS FOR THE PAGE IN ORDER TO LOAD THE LINKS)

FIND A GUI LIBRARY TO USE YOUR PROGRAM MORE EASILY



"""
