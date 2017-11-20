#!/usr/bin/python3 -W all
"""
    data2fasttext-test.py: tests for data2fasttext.py
    usage: data2fasttext-test.py
    20171120 erikt(at)xs4all.nl
"""

import unittest
import data2fasttext

class myTest(unittest.TestCase):
    def testAbbreviateName(self):
        self.assertEqual(data2fasttext.abbreviateName("test"),"TES")

    def testRemoveXML(self):

        self.assertEqual(data2fasttext.removeXML("<a>abc\n</a>")," abc\n ")
    def testRemoveRedundantWhiteSpace(self):
        self.assertEqual(data2fasttext.removeRedundantWhiteSpace(" a  b\n "),"a b")

    def testTokenize(self):
        self.assertEqual(data2fasttext.tokenize("Hi? No!"),"Hi ? No !")

if __name__ == '__main__':
    unittest.main()
