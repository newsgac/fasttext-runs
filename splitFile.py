#!/usr/bin/python3 -W all
"""
    splitFile.py: split file in N parts
    usage: splitFile.py -f file [ -n N ]
    note: default size for N is 10
    20171123 erikt(at)xs4all.nl
"""

import getopt
import sys

COMMAND = sys.argv[0]
USAGE = "usage: "+COMMAND+" -f file [-n N]"
DEFAULTN = 10

def processOpts(argv):
    n = DEFAULTN
    inFileName = ""
    try: options = getopt.getopt(argv,"f:n:",[])
    except: sys.exit(USAGE)
    for option in options[0]:
        if option[0] == "-f": inFileName = option[1]
        elif option[0] == "-n": n = option[1]
    if inFileName == "": sys.exit(USAGE)
    return(inFileName,n)

def readData(inFileName):
    data = []
    inFile = open(inFileName,"r")
    for line in inFile: data.append(line.rstrip())
    inFile.close()
    return(data)

def writeData(inFileName,data,n):
    for counter in range(0,n):
        outFileName = inFileName+"."+str(counter)
        outFile = open(outFileName,"w")
        if counter == 0: start = 0
        else: start = int(counter*len(data)/n)
        if counter == n-1: end = len(data)
        else: end = int((counter+1)*len(data)/n)
        for i in range(start,end): print(data[i],file=outFile)
        outFile.close()
    return()

def main(argv):
    inFileName, n = processOpts(argv)
    data = readData(inFileName)
    writeData(inFileName,data,n)
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
