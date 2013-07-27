#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011, Dan Sheffner Dan@Sheffner.org
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

"""
mtgoxTicker.py - This program will write out a number of values
                 based on the mtgox ticker so I can display them on the pi
                 lcd

"""

import urllib2
import simplejson as json
import time


class Mtgox:

    def __init__(self):

        self.url = 'http://data.mtgox.com/api/2/BTCUSD/money/ticker_fast'
        self.file = './mtgox.txt'
        self.jsonObj = {}

    def readValues(self):
        response = urllib2.urlopen(self.url)
        html = response.read()
        self.jsonObj = json.loads(html)
        #print self.jsonObj

    def writeValues(self):
        f = open(self.file, 'w')
        f.write(self.jsonObj['data']['last_local']['display'] + '\n')
        f.write(self.jsonObj['data']['buy']['display'] + '\n')
        f.write(self.jsonObj['data']['sell']['display'] + '\n')
        f.close()

if __name__ == "__main__":

    mtgox = Mtgox()

    while 1 == 1:
        mtgox.readValues()
        mtgox.writeValues()
        time.sleep(1)
