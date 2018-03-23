#!/usr/bin/python -W all
"""
    getNewspaperText.py: retrieve all text of a newspaper edition from the KB
    usage: getNewspaperText.py id
    note: id is an identifier of a (daily) newspaper edition: a number
    20180323 erikt(at)xs4all.nl
"""

import codecs
from io import BytesIO
import pycurl
import re
import sys
import time

COMMAND = sys.argv.pop(0)
URLARTICLE = 'http://resolver.kb.nl/resolve?urn=ddd:'
URLPAGE = 'https://www.delpher.nl/nl/pres/view/pageocr?coll=ddd&identifier=ABCDDD:'
USAGE = COMMAND+" id"
pageNbr = 1
pageNbrs = {}

def readWebPage(url):
    time.sleep(1)
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL,url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    body = body.decode('utf8')
    return(body)

def makeArticleNbr(articleNbr):
    articleNbr = str(articleNbr)
    while len(articleNbr) < 4: articleNbr = "0"+articleNbr
    return("a"+articleNbr)

def makePageNbr(pageNbr):
    pageNbr = str(pageNbr)
    while len(pageNbr) < 3: pageNbr = "0"+pageNbr
    return("p"+pageNbr)

def makeUrlArticle(myId,articleNbr):
    articleNbr = makeArticleNbr(articleNbr)
    url = URLARTICLE+str(myId)+":mpeg21:"+articleNbr+":ocr"
    return(url)

def makeUrlPage(myId,pageNbr):
    pageNbrString = makePageNbr(pageNbr)
    url = URLPAGE+str(myId)+":mpeg21:"+pageNbrString
    return(url)

def writeText(myId,articleNbr,text):
    global pageNbrs

    if articleNbr in pageNbrs: pageNbr = pageNbrs[articleNbr]
    else: pageNbr = 0
    articleNbr = makeArticleNbr(articleNbr)
    pageNbr = makePageNbr(pageNbr)
    outFile = codecs.open(myId+"."+pageNbr+"."+articleNbr+".xml","w","utf8")
    outFile.write(text)
    outFile.close()
    return()

def processNextPage(myId):
    global pageNbr, pageNbrs

    articlesFound = 0
    url = makeUrlPage(myId,pageNbr)
    html = readWebPage(url)
    matches = re.findall(r":a0*([0-9]+)",html)
    for i in range(0,len(matches)):
        if not int(matches[i]) in pageNbrs:
            pageNbrs[int(matches[i])] = pageNbr
            articlesFound += 1
    pageNbr += 1
    return(articlesFound)

def main(argv):
    try: myId = argv.pop(0)
    except: sys.exit(USAGE)
    while True:
        returnValue = processNextPage(myId)
        if returnValue < 1: break
    articleNbr = 1
    url = makeUrlArticle(myId,articleNbr)
    text = readWebPage(url)
    while re.search(r"xml version=",text):
        writeText(myId,articleNbr,text)
        articleNbr += 1
        url = makeUrlArticle(myId,articleNbr)
        text = readWebPage(url)
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
