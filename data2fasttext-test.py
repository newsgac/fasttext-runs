#!/usr/bin/python3 -W all
"""
    data2fasttext-test.py: tests for data2fasttext.py
    usage: data2fasttext-test.py
    20171120 erikt(at)xs4all.nl
"""

import io
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import data2fasttext

HEADING = data2fasttext.HEADINGGENRE+"\t"+data2fasttext.HEADINGIDENTIFIER+"\t"+data2fasttext.HEADINGPREDICTION+"\n"
DATAREAD =   [ "1Genre\t\t\n" ,
               "2Genre\thttp://i2\t\n" ,
               "3Genre\thttp://i3\thttp://p3\n" ,
               "4Genre\t\thttp://p4\n" ]
DATAINTERN = [ {"genre":"1Genre","identifier":"","prediction":""},
               {"genre":"2Genre","identifier":"http://i2","prediction":""},
               {"genre":"3Genre","identifier":"http://i3","prediction":"http://p3"},
               {"genre":"4Genre","identifier":"","prediction":"http://p4"} ]
DATAOUT =    [ "",
               "__label__2GE https : //i2 : ocr",
               "__label__3GE https : //i3 : ocr",
               "__label__4GE https : //p4 : ocr"] 
URLIN = "http://resolver.kb.nl/resolve?urn=KBNRC01:000035728:mpeg21:a0007:ocr"
URLOUT = """<?xml version="1.0" encoding="UTF-8"?> <text> <title>Angst voor revolutie in India Weer 160 communisten gearresteerd</title> <p>In India zijn donderdag opnieuw 160 communisten gearresteerd. In totaal werden deze week 660 communistische leiders aangehouden. De pro-Chinese communisten hebben een vergadering van hun centrale comité, die morgen in Trlchoer, in de staat Kerala, zou worden gehouden, afgelast. De Indische minister van binnenlandse zaken, Nanda, verklaarde gisteren voor de radio, dat enkele groepen communisten een revolutie voorbereiden, die moet samenvallen met een Chinese inval in het noorden van het land.</p> </text>"""

class myTest(unittest.TestCase):
    def testAbbreviateName(self):
        self.assertEqual(data2fasttext.abbreviateName("test"),"TES")

    @patch("data2fasttext.readWebPage")
    def testPrintData(self,mockedReadWebPage):
        def mockedReadWebPageFunction(url): return(url)
        mockedReadWebPage.side_effect = mockedReadWebPageFunction
        for i in range(0,len(DATAINTERN)):
            f = io.StringIO()
            with redirect_stdout(f): data2fasttext.printData([DATAINTERN[i]])
            results = data2fasttext.removeRedundantWhiteSpace(f.getvalue())
            self.assertEqual(results,DATAOUT[i])

    def testReadFile(self):
        for i in range(0,len(DATAREAD)):
            sys.stdin = io.StringIO(HEADING+DATAREAD[i])
            results = data2fasttext.readFile()
            self.assertEqual(results,[DATAINTERN[i]])

    # warning: test success depends on external web content
    def testReadWebPage(self):
        results = data2fasttext.removeRedundantWhiteSpace(data2fasttext.readWebPage(URLIN))
        self.assertEqual(results,URLOUT)

    def testRemoveRedundantWhiteSpace(self):
        self.assertEqual(data2fasttext.removeRedundantWhiteSpace(" a  b\n "),"a b")

    def testRemoveXML(self):
        self.assertEqual(data2fasttext.removeXML("<a>abc\n</a>")," abc\n ")

    def testTokenize(self):
        self.assertEqual(data2fasttext.tokenize("Hi? No!"),"Hi ? No !")

if __name__ == '__main__':
    unittest.main()
