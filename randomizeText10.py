#!/usr/bin/python3 -W all
"""
    randomizeText10.py: randomize line order of a text
    usage: randomizeText10.py < file
    20171120 erikt(at)xs4all.nl
"""

import random
import sys

COMMAND = sys.argv.pop(0)
N = 10

def getLabel(line):
    return(line.split()[0])

def readData():
    data = []
    labelCount = {}
    for line in sys.stdin:
        label = getLabel(line)
        if not label in labelCount: labelCount[label] = 0
        labelCount[label] += 1
        data.append(line.strip())
    return(data,labelCount)

def randomizeList(listIn):
    random.seed()
    listOut = []
    while listIn:
        i = random.randint(0,len(listIn)-1)
        listOut.append(listIn[i])
        listIn[i] = listIn[-1]
        listIn.pop(-1)
    return(listOut)

def divideData(data,labelCount):
    buckets = []
    bucketLengths = {}
    currentBuckets = {}
    for i in range(0,N): buckets.append([])
    for label in labelCount:
        currentBuckets[label] = 0
        bucketLengths[label] = 0
    for d in data:
        label = getLabel(d)
        buckets[currentBuckets[label]].append(d)
        bucketLengths[label] += 1
        if int((bucketLengths[label]-1)*N/labelCount[label]) < \
           int(bucketLengths[label]*N/labelCount[label]):
            currentBuckets[label] += 1
    return(buckets)

def printData(data):
    for i in range(0,len(data)): print(data[i])

def main(argv):
    data,labelCount = readData()
    buckets = divideData(randomizeList(data),labelCount)
    for i in range(0,len(buckets)): 
        printData(randomizeList(buckets[i]))
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
