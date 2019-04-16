import os
import requests
from bs4 import BeautifulSoup

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

#Please enter your desired anime name here
chosenAnime = "Sword Art Online – Alicization"

url = "https://horriblesubs.info" + linksDict.get(chosenAnime)

#or uncomment the line below and enter the url to the show here 
#url = https://horriblesubs.info/shows/sword-art-online-alicization/")

showsoup = BeautifulSoup(requests.get(url).text, features="html.parser")

scriptList = showsoup.find_all("script")

for tag in scriptList:
	if "hs_showid" in tag.text:
		showid = tag.text[16:-1]


apiLink = "api.php?method=getshows&type=show&showid=" + showid

nextid = 0
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


"""
TODO

DYNAMICALLY LOADED ELEMENTS IN PAGES (NEED TO EMULATE OURSELF AS A BROWSER/CLIENT AND LOAD THE JS FOR THE PAGE IN ORDER TO LOAD THE LINKS)

FIND A GUI LIBRARY TO USE YOUR PROGRAM MORE EASILY



"""
