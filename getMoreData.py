#!/usr/bin/python3 -W all
"""
    getModeData.py: download more news articles from delpher
    usage: tr '\r' '\n' < file | getMoreData.py
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

def readData():
    csvreader = csv.reader(sys.stdin,delimiter="\t")
    dateCodes = {}
    for row in csvreader:
        for i in range(0,len(row)):
            if re.search("http:",row[i]):
                fields = row[i].split(":")
                if len(fields) > 2: dateCodes[fields[2]] = True
    return(dateCodes)

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

def addSourceInfo(xml,dateCode,articleCode): 
    root = ET.fromstring(xml)
    for e in root.iter('text'):
        e.attrib["date"] = dateCode
        e.attrib["article"] = articleCode
    newXml = ET.tostring(root)
    newXml = newXml.decode('utf8')
    return(newXml)

def getMoreData(dateCodes):
    for c in dateCodes:
       code = int(c)
       for n in range(code-MAXOFFSET,code+MAXOFFSET+1):
           newCode = str(n)
           while len(newCode) < DATECODELENGTH: newCode = "0"+newCode
           if not newCode in dateCodes:
               for a in range(1,MAXARTICLE):
                   article = str(a)
                   while len(article) < ARTICLECODELENGTH: article = "0"+article
                   article = "a"+article
                   url = URLBASE+newCode+URLCENTER+article+URLEND
                   status,xml = readWebPage(url)
                   if status != HTTPSTATUSOK: break
                   print(addSourceInfo(xml,newCode,article))
                   time.sleep(1)

def main(argv):
    dateCodes = readData()
    getMoreData(dateCodes)
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
