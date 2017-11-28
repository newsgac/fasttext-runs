#!/usr/bin/python3 -W all
"""
    xml2txt.py: convert xml to text and tokenize
    usage: xml2txt.py < file
    20171128 erikt(at)xs4all.nl
"""

from io import BytesIO
import csv
import nltk
import pycurl
import re
import sys
import xml.etree.ElementTree as ET
import time

HEADINGGENRE = "Genre"
HEADINGIDENTIFIER = "Identifier"
HEADINGPREDICTION = "Prediction"
LABELPREFIX = "__label__"
URLSUFFIX = ":ocr"
LABELLENGTH = 3
URLBASE = "https://resolver.kb.nl/resolve?urn=KBNRC01:"
URLCENTER = ":mpeg21:"
URLEND = ":ocr"
MAXOFFSET = 5
ARTICLECODELENGTH = 4
DATECODELENGTH = 9
MAXARTICLE = 500
HTTPSTATUSOK = 200

hapaxes = {}
other = {}

def readData():
    text = ""
    for line in sys.stdin:
        text += line
        if re.search("</text>",line): break
    return(text)

def readWebPage(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL,url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    body = buffer.getvalue()
    body = body.decode('utf8')
    status = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    return(status,body)

def removeXML(text):
    text = re.sub("<[^<>]*>"," ",text)
    return(text)

def removeRedundantWhiteSpace(text):
    text = re.sub("\s+"," ",text)
    text = re.sub("^\s+","",text)
    text = re.sub("\s+$","",text)
    return(text)

def tokenize(text):
    tokenizedList = nltk.word_tokenize(text)
    tokenized = ""
    for i in range(0,len(tokenizedList)):
        if i == 0: tokenized = tokenizedList[i]
        else: tokenized += " "+tokenizedList[i]
    return(tokenized)

def hapaxCount(text):
    tokens = text.split()
    unique = {}
    counter = 0
    for token in tokens: unique[token] = True
    for token in unique:
        if not token in hapaxes and not token in other:
            hapaxes[token] = True
            counter += 1
        elif token in hapaxes:
            other[token] = True
            hapaxes.pop(token)
    return(counter/len(unique))

def printData(text): 
    root = ET.fromstring(text)
    allText = ""
    for e in root.iter('title'):
        try:
            tokenized = tokenize(e.text)
            print(tokenized)
            allText += " "+tokenized
        except: pass
    for e in root.iter('p'): 
        try:
            tokenized = tokenize(e.text)
            print(tokenized)
            allText += " "+tokenized
        except: pass
    #hapaxScore = hapaxCount(allText)
    #print("HAPAX: ",hapaxScore)
    return()

def main(argv):
    text = readData()
    while text != "":
        printData(text)
        text = readData()
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
