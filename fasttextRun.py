#!/usr/bin/python3 -W all
"""
    fasttextRun.py: run fasttext via python interface
    usage: fasttextRun.py -f file [-n N]
    note: default number of N is 10 (10-fold cross validation)
    20180105 erikt(at)xs4all.nl
"""

import fasttext
import os
import random
import splitFile
import sys

DIM = 300
LARGENUMBER = 100000
MINCOUNT = 5
random.seed()
TMPFILENAME = "fasttextRun."+str(os.getpid())+"."+str(random.randint(0,LARGENUMBER))

def makeTrainFile(inFileName,i,n):
    outFileName = TMPFILENAME+".train"
    outFile = open(outFileName,"w")
    for j in range(0,n):
        if j != i:
            inFile = open(inFileName+"."+str(j),"r")
            for line in inFile: outFile.write(line)
            inFile.close()
    outFile.close()
    return(outFileName)

def fasttextRun(inFileName,i,n):
    trainFileName = makeTrainFile(inFileName,i,n)
    modelFileName = TMPFILENAME+".model"
    testFileName = inFileName+"."+str(i)
    classifier = fasttext.supervised(trainFileName,modelFileName,dim=DIM,min_count=MINCOUNT)
    # ,pretrained_vectors="/home/erikt/software/fastText/wiki.nl.vec")
    result = classifier.test(testFileName)
    os.unlink(trainFileName)
    os.unlink(modelFileName+".bin")
    return(result.precision)

def main(argv):
    inFileName, n = splitFile.processOpts(list(argv))
    data = splitFile.readData(inFileName)
    splitFile.writeData(inFileName,data,n)
    accuracyTotal = 0.0
    for i in range(0,n):
        accuracy = fasttextRun(inFileName,i,n)
        accuracyTotal += accuracy
        print("Fold: {0:0d}; Accuracy: {1:0.3f}".format(i,accuracy))
    print("Average accuracy {0:0.3f}".format(accuracyTotal/float(n)))
    return(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

