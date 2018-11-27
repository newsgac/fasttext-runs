#!/usr/bin/python3 -W all
"""
    randomizeText10.py: randomize line order of a text
    usage: randomizeText10.py < file
    20171120 erikt(at)xs4all.nl
"""

import random
import sys

N = 10

def readData():
    data = []
    labelCount = {}
    for line in sys.stdin: 
        line = line.rstrip()
        fields = line.split()
        label = fields[0]
        if not label in labelCount: labelCount[label] = 0
        labelCount[label] += 1
        data.append(line)
    return(data,labelCount)

def randomizeData(data):
    random.seed()
    randomData = []
    while data:
        i = random.randint(0,len(data)-1)
        randomData.append(data[i])
        data[i] = data[-1]
        data.pop()
    return(randomData)

def divideData(data,labelCount):
    buckets = []
    bucketLengths = {}
    currentBuckets = {}
    for i in range(0,N): buckets.append([])
    for label in labelCount:
        currentBuckets[label] = 0
        bucketLengths[label] = 0
    for d in data:
        fields = d.split()
        label = fields[0]
        buckets[currentBuckets[label]].append(d)
        bucketLengths[label] += 1
        if bucketLengths[label] >= labelCount[label]/N:
            currentBuckets[label] += 1
            bucketLengths[label] = 0
    return(buckets)

def printData(data):
    for i in range(0,len(data)): print(data[i])

def main(argv):
    data,labelCount = readData()
    buckets = divideData(randomizeData(data),labelCount)
    for i in range(0,len(buckets)): printData(buckets[i])
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
