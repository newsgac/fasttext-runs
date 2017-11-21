#!/usr/bin/python3 -W all
"""
    randomizeText-test.py: tests for randomizeText-test.py
    usage: randomizeText-test.py
    20171120 erikt(at)xs4all.nl
"""

import io
import re
import sys
import unittest
from contextlib import redirect_stdout
from randomizeText import readData
from randomizeText import printData

DATA = ['a','b','c']

def string2list(inString):
    outList = inString.split("\n")
    if re.search("\n$",inString): outList.pop()
    return(outList)

def list2string(inList):
    outString = "\n".join(inList)
    if len(outString) > 0: outString+"\n"
    return(outString)

class myTest(unittest.TestCase):
    def testPrintData(self):
        f = io.StringIO()
        with redirect_stdout(f): printData(list(DATA))
        results = string2list(f.getvalue())
        self.assertEqual(len(results),len(DATA))
        self.assertEqual(sorted(results),sorted(DATA))

    def testReadData(self):
        sys.stdin = io.StringIO(list2string(DATA))
        results = readData()
        self.assertEqual(results,DATA)
         
if __name__ == '__main__':
    unittest.main()
