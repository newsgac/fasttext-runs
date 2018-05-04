#!/usr/bin/python3
"""
    kimcsv2fasttext.py: convert kim's balanced data format to fasttext format
    usage: ./kimcsv2fasttext.py < BalancedDataSet.csv
    20180504 erikt(at)xs4all.nl
"""

import csv
import html
import nltk
import re
import sys
import time

from io import BytesIO
from urllib.request import urlopen

COMMAND = sys.argv.pop(0)
HEADINGDATE = "Date"
HEADINGGENRE = "Genre"
HEADINGIDENTIFIER = "Artikel-ID"
HEADINGNEWSPAPER = "Newspaper"
HEADINGSUBJECT = "Prediction"
LABELLENGTH = 3
LABELPREFIX = "__label__"
SEPARATOR = ","
URLPREFIX = r"^https?://"
URLSTART = "http://resolver.kb.nl/resolve?urn="
URLSUFFIX = ":ocr"

def isUrl(url):
    return(re.search(URLPREFIX,url))

def readFile():
    articles = []
    lineNbr = 0
    csvReader = csv.DictReader(sys.stdin,delimiter=SEPARATOR)
    for row in csvReader:
        lineNbr += 1
        try:
            date = row[HEADINGDATE]
            genre = row[HEADINGGENRE]
            identifiers = []
            for cellValue in row.values():
                if not cellValue is None and isUrl(cellValue): 
                    identifiers.append(cellValue)
            articles.append({"date":date,"genre":genre,"identifiers":identifiers})
        except: sys.exit(COMMAND+": missing data on line "+str(lineNbr))
    return(articles)

def abbreviateName(name): 
    return(name[0:LABELLENGTH].upper())

def readWebPage(url):
    time.sleep(1)
    return(str(urlopen(url,data=None).read(),encoding="utf-8"))

def removeXML(text):
    text = re.sub(r"<[^<>]*>",r" ",text)
    text = html.unescape(text)
    return(text)

def removeRedundantWhiteSpace(text):
    text = re.sub(r"\s+",r" ",text)
    text = re.sub(r"^\s+",r"",text)
    text = re.sub(r"\s+$",r"",text)
    return(text)

def tokenize(text):
    tokenizedSentenceList = nltk.word_tokenize(text)
    tokenizedText = " ".join(tokenizedSentenceList)
    return(tokenizedText)

def makeUrl(articleId):
    return(URLSTART+articleId+URLSUFFIX)

def getArticleIdFromUrl(url):
    fields = url.split("=")
    return(":".join(fields[-1:]))

def printData(articles):
    for i in range(0,len(articles)):
        date = articles[i]["date"]
        genre = abbreviateName(articles[i]["genre"])
        text = ""
        for url in articles[i]["identifiers"]:
            url = makeUrl(getArticleIdFromUrl(url))
            if len(text) > 0: text += " "
            text += removeRedundantWhiteSpace(tokenize(removeXML(readWebPage(url))))
        print(LABELPREFIX+genre+" DATE="+date+" "+text)

def main(argv):
    articles = readFile()
    printData(articles)
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
