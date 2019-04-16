import os
import requests
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup

nameList = []
hrefStrings = ""
linksDict = {}
quality = ""
finalLoad = ""
landingurl = "https://horriblesubs.info/"
episodeList = []


#==========
#Init GUI
#==========
main = tk.Tk()
main.title("HorribleSubs Magnet Downloader")
main.geometry("510x190")
main.resizable(True, True)
app = tk.Frame(main)
app.grid()
ttk.Button(main, text="Download").grid(row = 4, column = 0, sticky = "E")


#======================================
#Extracting series' links from page
#======================================
startPage = requests.get(landingurl + "shows/")

soup = BeautifulSoup(startPage.text, features="html.parser")

for div in soup.find_all(class_="shows-wrapper"):
	aTags = div.find_all("a", href=True)
	for line in aTags:
		linksDict[line["title"]] = line["href"]


#===========================================
#Initialising of List of all series names
#===========================================
for name, link in linksDict.items():
	nameList.append(name)


#===================
#Series Dropdown
#===================
label1 = ttk.Label(app, text = "Select Series:")
label1.grid(column = 0, row = 0, pady = 10, sticky = "W")
dropVar = tk.StringVar()
dropVar.set(nameList[0])
dropDown = ttk.Combobox(app, width = 66, textvariable = dropVar, values = nameList, state = "readonly")
dropDown.grid(column = 1, row = 0)


#==================================================================================
# Obtaining showid value from wepage in order to query API to obtain magnet link  
#==================================================================================
chosenAnime = nameList[347]

url = "https://horriblesubs.info" + str(linksDict.get("Absolute Duo"))

showsoup = BeautifulSoup(requests.get(url).text, features="html.parser")

scriptList = showsoup.find_all("script")

for tag in scriptList:
	if "hs_showid" in tag.text:
		showid = tag.text[16:-1]



#===================
#Quality Dropdown
#===================
label2 = ttk.Label(app, text="Quality:")
label2.grid(row = 1, column = 0, pady = 10, sticky = "W")
qualityVar = tk.StringVar()
qualityVar.set("1080p")
qualityDrop = ttk.Combobox(app, textvariable=qualityVar, values=["1080p", "720p", "360p"], width=6, state="readonly")
qualityDrop.grid(row = 1, column = 1, sticky="W")


#======================================================
#Loading the whole page by doing all API calls
#======================================================
def loadDynamicElements():
	nextid = 0
	apiLink = "api.php?method=getshows&type=show&showid=" + showid
	while True:
		loadedPage = requests.get(landingurl + apiLink + "&nextid=" + str(nextid))

		if loadedPage.text == 'DONE':
			break

		finalLoad += loadedPage.text
		nextid += 1

	loadedSoup = BeautifulSoup(finalLoad,features="html.parser")


#======================================================
#Checks for number of episodes for the given series
#======================================================
def loadEpisodes():
	for episodes in loadedSoup.find_all(class_="rls-info-container"):
		episodeList.append(episodes["id"])

	lastEp = episodeList[0]
	firstEp = episodeList[-1]


	#==============================
	#Episode Selection Dropdowns
	#==============================
	label3 = ttk.Label(app, text="Start Episode:")
	label3.grid(row = 2, column = 0, pady = 10, sticky = "W")
	sEpVar = tk.StringVar()
	sEpVar.set(firstEp)
	sEpDrop = ttk.Combobox(app, textvariable=sEpVar, values=episodeList, width=6, state="readonly")
	sEpDrop.grid(row = 2, column = 1, sticky="W")

	label4 = ttk.Label(app, text="End Episode:")
	label4.grid(row = 3, column = 0, pady = 10, sticky = "W")
	eEpVar = tk.StringVar()
	eEpVar.set(lastEp)
	eEpDrop = ttk.Combobox(app, textvariable=eEpVar, values=episodeList, width=6, state="readonly")
	eEpDrop.grid(row = 3, column = 1, sticky="W")


#======================================================
#Obtaining magnet links from API call and execution
#======================================================
def executeMagnetLinks():
	

	for span in loadedSoup.find_all(class_="link-" + quality):
		for x in span.find_all(class_="hs-magnet-link"):
			for y in x.find_all("a", href=True):
				# os.startfile(str(y["href"]))
				break
	
main.mainloop()