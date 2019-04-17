import os
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup


nameList = []
hrefStrings = ""
linksDict = {}
quality = ""
landingurl = "https://horriblesubs.info/"


#==========
#Init GUI
#==========
main = tk.Tk()
main.title("HorribleSubs Magnet Downloader")
main.geometry("660x240")
main.resizable(True, True)
app = tk.Frame(main)
app.grid()
dlButton = ttk.Button(main, text="Download")
dlButton.grid(row = 4, column = 0, sticky = "E")
dropVar = tk.StringVar()
qualityVar = tk.StringVar()
sEpVar = tk.StringVar()
eEpVar = tk.StringVar()

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
dropVar.set(nameList[0])
dropDown = ttk.Combobox(app, width = 66, textvariable = dropVar, values = nameList, state = "readonly")
dropDown.grid(column = 1, row = 0)


#===================
#Quality Dropdown
#===================
label2 = ttk.Label(app, text="Quality:")
label2.grid(row = 1, column = 0, pady = 10, sticky = "W")
qualityVar.set("1080p")
qualityDrop = ttk.Combobox(app, textvariable=qualityVar, values=["1080p", "720p", "480p","360p"], width=6, state="readonly")
qualityDrop.grid(row = 1, column = 1, sticky="W")


#==================================================================================
# Obtaining showid value from wepage in order to query API to obtain magnet link  
#==================================================================================
def getShowID():
	url = "https://horriblesubs.info" + str(linksDict.get(dropVar.get()))

	showsoup = BeautifulSoup(requests.get(url).text, features="html.parser")

	scriptList = showsoup.find_all("script")

	for tag in scriptList:
		if "hs_showid" in tag.text:
			return tag.text[16:-1]

	return false


#======================================================
#Loading the whole page by doing all API calls
#======================================================
def loadPage(*args):
	finalLoad = ""
	nextid = 0
	showid = getShowID()

	if not showid:
		messagebox.showerror("Error", "Invalid Series Name!!")

	apiLink = "api.php?method=getshows&type=show&showid=" + showid
	while True:
		loadedPage = requests.get(landingurl + apiLink + "&nextid=" + str(nextid))

		if loadedPage.text == 'DONE':
			break

		finalLoad += loadedPage.text
		nextid += 1

	return BeautifulSoup(finalLoad,features="html.parser")

def loadEpisodes(*args):
	global loadedSoup
	episodeList = []
	quality = loadQuality()
	
	loadedSoup = loadPage()


	#======================================================
	#Checks for number of episodes for the given series
	#======================================================
	for episodes in loadedSoup.find_all(class_="rls-info-container"):
		episodeList.append(str(episodes["id"]))

	episodeList.reverse()


	#==============================
	#Episode Selection Dropdowns
	#==============================
	label3 = ttk.Label(app, text="Start Episode:")
	label3.grid(row = 2, column = 0, pady = 10, sticky = "W")
	sEpVar.set(str(episodeList[0]))
	sEpDrop = ttk.Combobox(app, textvariable=sEpVar, values=episodeList, width=6, state="readonly")
	sEpDrop.grid(row = 2, column = 1, sticky="W")

	label4 = ttk.Label(app, text="End Episode:")
	label4.grid(row = 3, column = 0, pady = 10, sticky = "W")
	eEpVar.set(str(episodeList[-1]))
	eEpDrop = ttk.Combobox(app, textvariable=eEpVar, values=episodeList, width=6, state="readonly")
	eEpDrop.grid(row = 3, column = 1, sticky="W")

	qualityCheck()

	if checkBatch():
		displayBatchDownload()



def loadQuality(*args):
	return qualityVar.get()


def checkBatch(*args):
	showid = getShowID()
	apiLink = "api.php?method=getshows&type=batch&showid=" + showid
	batchPage = requests.get(landingurl + apiLink)

	if "href" in batchPage:
		return True

	return False


def displayBatchDownload():
	batchButton = ttk.Button(main, text="Batch Download", width=20)
	batchButton.grid(row = 3, column = 0, sticky = "E")


def qualityCheck(*args):
	validEpList = []
	notDownloaded = []
	qualityEpisodes = len(loadedSoup.find_all("div", class_="link-" + qualityVar.get()))

	for validEpisodes in loadedSoup.find_all("div", class_="link-" + qualityVar.get()):
		validEpList.append(str(int(validEpisodes["id"][:len(validEpisodes["id"]) - len(qualityVar.get()) - 1])))

	for eachEpisode in range(int(sEpVar.get()), int(eEpVar.get()) + 1):
		if str(eachEpisode) not in validEpList:
			notDownloaded.append(eachEpisode)

	if int(eEpVar.get()) != qualityEpisodes:
		if qualityEpisodes == 0:
			messagebox.showinfo("Alert", "There are no episodes in the given quality")
			return
		messagebox.showinfo("Alert", "There are only " + str(qualityEpisodes) + " episodes in " + qualityVar.get() + ". Only episodes with " + qualityVar.get() + " will be downloaded.")
		messagebox.showinfo("Alert", "Episodes that were not downloaded: " + str(notDownloaded))

#======================================================
#Obtaining magnet links from API call and execution
#======================================================
def executeMagnetLinks(event):
	quality = loadQuality()
	loadedSoup = loadPage()

	for span in loadedSoup.find_all(class_="link-" + qualityVar.get()):
		for magnets in span.find_all(class_="hs-magnet-link"):
			for aTags in magnets.find_all("a", href=True):
				print("Success!")
				# os.startfile(str(aTags["href"]))
				break
	
dropVar.trace_add("write", loadEpisodes)
qualityVar.trace_add("write", qualityCheck)
dlButton.bind("<Button-1>", executeMagnetLinks)

main.mainloop()