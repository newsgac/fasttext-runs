#!/usr/bin/python3 -W all
"""
    splitFile-test.py: tests for splitFile.py
    usage: splitFile-test.py
    20171124 erikt(at)xs4all.nl
"""

import io
import re
import sys
import unittest
from contextlib import redirect_stdout
import splitFile

DATA = ['a','b','c']
OPTSSHORT = ['-f','DATAFILE']
OPTSLONG = OPTSSHORT+['-n',splitFile.DEFAULTN-1]

def string2list(inString):
    outList = inString.split("\n")
    if re.search("\n$",inString): outList.pop()
    return(outList)

def list2string(inList):
    outString = "\n".join(inList)
    if len(outString) > 0: outString+"\n"
    return(outString)

class myTest(unittest.TestCase):
    def testProcessOpts(self):
        inFileName,n = splitFile.processOpts(OPTSSHORT)
        self.assertEqual(inFileName,OPTSSHORT[-1])
        self.assertEqual(n,splitFile.DEFAULTN)
        inFileName,n = splitFile.processOpts(OPTSLONG)
        self.assertEqual(n,OPTSLONG[-1])

    def testReadData(self): pass

    def testWriteData(self): pass
         
if __name__ == '__main__':
    unittest.main()
