#!/usr/bin/python3 -W all
"""
    randomizeText.py: randomize line order of a text
    usage: randomizeText.py < file
    20171120 erikt(at)xs4all.nl
"""

import random
import sys

def readData():
    data = []
    for line in sys.stdin: 
        line = line.rstrip()
        data.append(line)
    return(data)

def printData(data):
    random.seed()
    while data:
        i = random.randint(0,len(data)-1)
        print(data[i])
        data[i] = data[-1]
        data.pop()
    return()

def main(argv):
    data = readData()
    printData(data)
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
