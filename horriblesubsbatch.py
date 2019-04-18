import os
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup

loadedSoup=BeautifulSoup(features="html.parser")
nameList = []
hrefStrings = ""
linksDict = {}
landingurl = "https://horriblesubs.info/"


#==========
#Init GUI
#==========
main = tk.Tk()
main.title("HorribleSubs Magnet Downloader")
main.geometry("680x260")
main.resizable(True, True)
app = tk.Frame(main)
app.grid()


dlButton = ttk.Button(main, text="Download")
label3 = ttk.Label(app, text="Batches:")
label4 = ttk.Label(app, text="Start Episode:")
label5 = ttk.Label(app, text="End Episode:")
batchButton = ttk.Button(main, text="Batch Download", width=20)

dropVar = tk.StringVar()
qualityVar = tk.StringVar()
sEpVar = tk.StringVar()
eEpVar = tk.StringVar()
batchText = tk.StringVar()

sEpDrop = ttk.Combobox(app, textvariable=sEpVar, width=6, state="readonly")
eEpDrop = ttk.Combobox(app, textvariable=eEpVar, width=6, state="readonly")
batchSelect = ttk.Combobox(app, textvariable=batchText, width=6, state="readonly")

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
label1.grid(column = 0, row = 0, pady = 10, padx=10, sticky = "W")
dropVar.set("Please Select...")
dropDown = ttk.Combobox(app, width = 66, textvariable = dropVar, values = nameList, state = "readonly")
dropDown.grid(column = 1, row = 0, columnspan=3)


#===================
#Quality Dropdown
#===================
label2 = ttk.Label(app, text="Quality:")
label2.grid(row = 1, column = 0, pady = 10, padx=10, sticky = "W")
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

	if requests.get(landingurl + apiLink).text == "There are no individual episodes for this show":
		sEpDrop.grid_forget()
		eEpDrop.grid_forget()
		label4.grid_forget()
		label5.grid_forget()
		apiLink = "api.php?method=getshows&type=batch&showid=" + showid

		while True:
			loadedPage = requests.get(landingurl + apiLink + "&nextid=" + str(nextid))

			if loadedPage.text == "There are no batches for this show yet":
				if nextid == 0:
					messagebox.showinfo("No Batches", "There are no batches for this show")
				break

			finalLoad += loadedPage.text
			nextid += 1

		return BeautifulSoup(finalLoad, features="html.parser"), True

	while True:
		loadedPage = requests.get(landingurl + apiLink + "&nextid=" + str(nextid))

		if loadedPage.text == "DONE":
			break

		finalLoad += loadedPage.text
		nextid += 1

	return BeautifulSoup(finalLoad,features="html.parser"), False


def loadEpisodes(*args):
		global loadedSoup
		episodeList = []
		
		loadedSoup, batchOnly = loadPage()
		
		if batchOnly:
			batchElements(loadedSoup)

			qualityCheck(batch=True, soup=loadedSoup)

			messagebox.showinfo("Batch Only", "There is only a batch download for this series")
			displayBatchDownload()
			dlButton.grid_forget()

		else:
			#======================================================
			#Checks for number of episodes for the given series
			#======================================================
			for episodes in loadedSoup.find_all(class_="rls-info-container"):
				episodeList.append(str(episodes["id"]))

			episodeList.reverse()


			#==============================
			#Episode Selection Dropdowns
			#==============================
			
			label4.grid(row = 2, column = 0, pady = 10, padx=10, sticky = "W")
			label5.grid(row = 3, column = 0, pady = 10, padx=10, sticky = "W")

			sEpVar.set(str(episodeList[0]))
			sEpDrop["values"] = episodeList
			sEpDrop.grid(row = 2, column = 1, sticky="W")

			eEpVar.set(str(episodeList[-1]))
			eEpDrop["values"] = episodeList
			eEpDrop.grid(row = 3, column = 1, sticky="W")

			qualityCheck(soup=loadedSoup)

			if checkBatch():
				messagebox.showinfo("Batch Found!", "Batch Found! Please click on the 'Download Batch' button to start your batch download")
				displayBatchDownload()

			else:
				label3.grid_forget()
				batchButton.grid_forget()
				batchSelect.grid_forget()

			dlButton.grid(row = 5, column = 0, sticky = "E")


def checkBatch():
	url = getBatches()

	if "href" in url.text:
		batchSoup = BeautifulSoup(url.text, features="html.parser")
		batchElements(batchSoup)
		return True

	return False


def getBatches():
	showid = getShowID()

	if not showid:
		messagebox.showerror("Error", "Invalid Series Name!!")

	apiLink = "api.php?method=getshows&type=batch&showid=" + showid

	return requests.get(landingurl + apiLink)


def batchElements(loadedSoup):
	batchList = []
	for episodes in loadedSoup.find_all(class_="rls-info-container"):
		batchList.append(str(episodes["id"]))

	batchList.reverse()

	label3.grid(row = 4, column = 0, pady = 10, padx=10, sticky = "W")

	batchText.set(str(batchList[0]))
	batchSelect["values"] = batchList
	batchSelect.grid(row = 4, column = 1, sticky="W")



def displayBatchDownload():
	batchButton.grid(row = 5, column = 0, padx=10, sticky = "W")
	batchButton.bind("<Button-1>", executeBatchLinks)


def qualityCheck(*args, batch=False, soup=loadedSoup):
	validEpList = []
	notDownloaded = []

	qualityEpisodes = soup.find_all("div", class_="link-" + qualityVar.get())
	noQualityEpisodes = len(qualityEpisodes)

	if batch:
		if noQualityEpisodes == 0:
			messagebox.showinfo("Alert", "There are no batches in the given quality")
			return False

		for validBatches in qualityEpisodes:
			validEpList.append(str(validBatches["id"][:len(validBatches["id"]) - len(qualityVar.get()) - 1]))

		for eachBatch in soup.find_all(class_="rls-info-container"):
			if eachBatch["id"] not in validEpList:
				notDownloaded.append(eachBatch["id"])

		if len(loadedSoup.find_all(class_="rls-info-container")) != noQualityEpisodes:
			messagebox.showinfo("Alert", "There are only " + str(noQualityEpisodes) + " batches in " + qualityVar.get() + ". Only batches in " + qualityVar.get() + " will be downloaded.")
			messagebox.showinfo("Alert", "Batches that will not be downloaded: " + str(notDownloaded))

		return True

	else:
		if noQualityEpisodes == 0:
			messagebox.showinfo("Alert", "There are no episodes in the given quality")
			return False

		for validEpisodes in qualityEpisodes:
			validEpList.append(str(validEpisodes["id"][:len(validEpisodes["id"]) - len(qualityVar.get()) - 1]))

		for eachEpisode in soup.find_all(class_="rls-info-container"):
			if eachEpisode["id"] not in validEpList:
				notDownloaded.append(eachEpisode["id"])

		if len(soup.find_all(class_="rls-info-container")) != noQualityEpisodes:
			messagebox.showinfo("Alert", "There are only " + str(noQualityEpisodes) + " episodes in " + qualityVar.get() + ". Only episodes in " + qualityVar.get() + " will be downloaded.")
			messagebox.showinfo("Alert", "Episodes that will not be downloaded: " + str(notDownloaded))

		return True

def buttonQualityCheck(*args):
	validEpList = []
	notDownloaded = []

	qualityEpisodes = loadedSoup.find_all("div", class_="link-" + qualityVar.get())
	noQualityEpisodes = len(qualityEpisodes)

	if noQualityEpisodes == 0:
		messagebox.showinfo("Alert", "There are no episodes in the given quality")
		return

	for validEpisodes in qualityEpisodes:
		validEpList.append(str(validEpisodes["id"][:len(validEpisodes["id"]) - len(qualityVar.get()) - 1]))

	for eachEpisode in loadedSoup.find_all(class_="rls-info-container"):
		if eachEpisode["id"] not in validEpList:
			notDownloaded.append(eachEpisode["id"])

	if len(loadedSoup.find_all(class_="rls-info-container")) != noQualityEpisodes:
		messagebox.showinfo("Alert", "There are only " + str(noQualityEpisodes) + " episodes in " + qualityVar.get() + ". Only episodes in " + qualityVar.get() + " will be downloaded.")
		messagebox.showinfo("Alert", "Episodes that will not be downloaded: " + str(notDownloaded))



#======================================================
#Obtaining magnet links from API call and execution
#======================================================
def executeMagnetLinks(event):
	loadedSoup, batchOnly = loadPage()
	if qualityCheck(soup=loadedSoup):

		if batchOnly:
			executeBatchLinks()
			return

		for span in loadedSoup.find_all(class_="link-" + qualityVar.get()):
			for magnets in span.find_all(class_="hs-magnet-link"):
				for aTags in magnets.find_all("a", href=True):
					# print("Success!")
					os.startfile(str(aTags["href"]))
					break


def executeBatchLinks(event):
	url = getBatches()
	batchSoup = BeautifulSoup(url.text, features="html.parser")
	# for span in batchSoup.find_all(class_="link-" + qualityVar.get()):
	# 	for magnets in span.find_all(class_="hs-magnet-link"):
	# 		for aTags in magnets.find_all("a", href=True):
	# 			print("Success!")
	# 			# os.startfile(str(aTags["href"]))
	# 			break

	batches = batchSoup.find(id=str(batchText.get()) + "-" + qualityVar.get())
	if batches:
		magnet = batches.find(class_="hs-magnet-link")
		aTag = magnet.find("a", href=True)
		# print("Success!")
		os.startfile(str(aTag["href"]))

	else:
		messagebox.showerror("Quality Invalid", "There doesn't exist a batch for the given quality")

	
dropVar.trace_add("write", loadEpisodes)
qualityVar.trace_add("write", buttonQualityCheck)
dlButton.bind("<Button-1>", executeMagnetLinks)

main.mainloop()