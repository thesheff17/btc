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
I'm going to attempt to pull the 22.5 min hash rate from
eligius pool so I can email myself when my miners fail
or internet fails
"""

import urllib2
import os


class Eligius:

    def __init__(self):

        #url to the pool
        poolUrl = 'http://eligius.st/~wizkid057/newstats/userstats.php/'

        btcAddress = '1BVaSgDdgNmckt1R1wz14yD5i4cqZFpBh5'  # btc address
        self.url = poolUrl + btcAddress  # combined url
        self.threshold = 110  # threshold in Gh/s
        self.email = 'dan@sheffner.org'  # who to email

    def emailMe(self, email, subject, body):
        #I'm lazy here and just use os module plus sendmail
        SENDMAIL = "/usr/sbin/sendmail"  # sendmail location
        p = os.popen("%s -t" % SENDMAIL, "w")
        p.write("To: " + email + "\n")
        p.write("Subject: " + subject + "\n")
        p.write("\n")  # blank line separating headers from body
        p.write(body + "\n")
        p.close()

    def getHashRate(self):
        #I do a try except here in case the site is down
        #I don't want the script to crash
        try:
            response = urllib2.urlopen(self.url)
            html = response.read()
            spaceArray = html.split(" ")
        except:
            self.emailMe("eligius web site looks to be down")

        for value, each in enumerate(spaceArray):
            if "22.5" in each and "minutes" in spaceArray[value + 1]:
                twentyTwoSlot = value

        ghsValue = spaceArray[twentyTwoSlot + 3]

        self.currentGhs = ghsValue[ghsValue.find(">") + 1:-1]
        print "Your current hashrate is " + self.currentGhs + " Gh/s"

    def checkHashRate(self):
        if self.threshold > float(self.currentGhs):
            print "threshold met sending email"
            self.emailMe(self.email, "eligius miner threshold met",
                         "Current hashrate is " + str(self.currentGhs))
        else:
            print "thresold is fine"

if __name__ == "__main__":

    eligius = Eligius()

    eligius.getHashRate()
    eligius.checkHashRate()
