#!/usr/bin/python3 -W all
"""
    data2fasttext.py: convert NEWSGAC data format to fasttext format
    usage: tr '\r' '\n' < file | ./data2fasttext.py
    notes: expects TAB separated file with fields Genre and Identifier
    20171120 erikt(at)xs4all.nl
"""

from io import BytesIO
import csv
import nltk
import pycurl
import re
import sys

HEADINGGENRE = "Genre"
HEADINGIDENTIFIER = "Identifier"
HEADINGPREDICTION = "Prediction"
LABELPREFIX = "__label__"
URLSUFFIX = ":ocr"
LABELLENGTH = 3

def readFile():
    csvreader = csv.reader(sys.stdin,delimiter="\t")
    rowCounter = 0
    columnGenre = -1
    columnIdentifier = -1
    columnPrediction = -1
    data = []
    for row in csvreader:
        rowCounter += 1
        if rowCounter == 1:
            for column in range(0,len(row)):
                if row[column] == HEADINGGENRE: columnGenre = column
                if row[column] == HEADINGIDENTIFIER: columnIdentifier = column
                if row[column] == HEADINGPREDICTION: columnPrediction = column
        else:
            try:
                genre = row[columnGenre]
                identifier = row[columnIdentifier]
                prediction = row[columnPrediction]
                data.append({"genre":genre,"identifier":identifier,"prediction":prediction})
            except:
                sys.exit(COMMAND+": problem reading data: "+columnGenre+" "+columnIdentifier+" "+columnPrediction)
    return(data)

def abbreviateName(name): 
    return(name[0:LABELLENGTH].upper())

def readWebPage(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL,url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    body = body.decode('utf8')
    return(body)

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

def printData(data):
    for i in range(0,len(data)):
        genre = abbreviateName(data[i]["genre"])
        url = data[i]["identifier"]
        if not re.search("^http",url): url = data[i]["prediction"]
        if re.search("^http",url):
            url = re.sub("^http:","https:",url)
            if not re.match(URLSUFFIX+"$",url): url += URLSUFFIX
            text = removeRedundantWhiteSpace(tokenize(removeXML(readWebPage(url))))
            print(LABELPREFIX+genre+" "+text)

def main(argv):
    data = readFile()
    printData(data)
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
