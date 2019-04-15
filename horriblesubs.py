import os
import requests
from bs4 import BeautifulSoup
import re

nameList = []
startPage = requests.get("https://horriblesubs.info/shows/")

htmlStart = startPage.text

soup = BeautifulSoup(htmlStart, features="html.parser")

linkList = soup.find_all(class_="ind-show")

for x in linkList:
    nameList.append(x.text)


print(soup.find_all("a",text=nameList[1]))
