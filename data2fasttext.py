#!/usr/bin/python3 -W all
"""
    data2fasttext.py: convert NEWSGAC data format to fasttext format
    usage: tr '\r' '\n' < juliette-data.txt | ./data2fasttext.py
    notes: expects TAB separated file with fields Genre Identifier Datum Prediction
    20171120 erikt(at)xs4all.nl
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
HEADINGDATE = "Datum"
HEADINGGENRE = "Genre"
HEADINGIDENTIFIER = "Identifier"
HEADINGPREDICTION = "Prediction"
INSECUREURL = r"^http:"
LABELLENGTH = 3
LABELPREFIX = "__label__"
SECUREURL = r"https:"
SEPARATOR = "\t"
URLPREFIX = r"http"
URLSUFFIX = ":ocr"

def readFile():
    articles = []
    lineNbr = 0
    csvReader = csv.DictReader(sys.stdin,delimiter=SEPARATOR)
    for row in csvReader:
        lineNbr += 1
        try:
            date = row[HEADINGDATE]
            genre = row[HEADINGGENRE]
            identifier = row[HEADINGIDENTIFIER]
            prediction = row[HEADINGPREDICTION]
            articles.append({"date":date,"genre":genre,"identifier":identifier,"prediction":prediction})
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

def isUrl(url):
    return(re.search(URLPREFIX,url))

def makeUrlSecure(url):
    return(re.sub(INSECUREURL,SECUREURL,url))

def addUrlSuffix(url):
    if not re.search(URLSUFFIX+"$",url): url += URLSUFFIX
    return(url)

def printData(articles):
    cache = {}
    for i in range(0,len(articles)):
        date = articles[i]["date"]
        genre = abbreviateName(articles[i]["genre"])
        # the url can be either in column identifier or in prediction
        url = articles[i]["identifier"].rstrip()
        if not isUrl(url): 
            url = articles[i]["prediction"].rstrip()
        if isUrl(url):
            url = addUrlSuffix(makeUrlSecure(url))
            if url in cache: 
                text = cache[url]
            else:
                text = removeRedundantWhiteSpace(tokenize(removeXML(readWebPage(url))))
                cache[url] = text
            print(LABELPREFIX+genre+" DATE="+date+" "+text)

def main(argv):
    articles = readFile()
    printData(articles)
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
