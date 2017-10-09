import urllib2
import urllib
import re
import thread
import time
import sys
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
import string

class Spider_Model:


    def __init__(self):
        self.listOfYear = self.yearIterator()

    def saveHTML(self, year):

        myUrl = "https://www.eskimo.com/~pbender/misc/salaries"+str(year)[2:]+".txt"
        # print myUrl
        req = urllib2.Request(myUrl)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        sName = "year" + str(year) + '.txt'
        f = open(sName, 'w+')
        f.write(myPage)
        # lines = f.read().getlines()
        # print lines
        f.close()

    def yearIterator(self):
        l = [0]*28
        l[0] = 1986
        l[1] = 1988
        l[2] = 1989
        year = 1991
        for i in range (3,28):
            l[i] = year
            year+=1
        # print l
        return l


pbender = Spider_Model()

# sasve html
for i in range(0,28):
    pbender.saveHTML(pbender.listOfYear[i])

# extract useful part
for i in range (0,28):
    occurCounter = 0
    with open('year'+ str(pbender.listOfYear[i]) + '.txt', 'r+') as f:
        content = f.read()
        # f.close()
        # print content
    with open('year' + str(pbender.listOfYear[i]) + 'v1' + '.txt', 'w') as f2:
        if pbender.listOfYear[i] == 1996 or pbender.listOfYear[i] == 1998 or pbender.listOfYear[i] == 1999:
            for m in re.finditer('Boston', content):
                occurCounter += 1
                # print pbender.listOfYear[i]
                # print "Boston"
                # print(m.start(), m.end())
                if occurCounter == 2:
                    content = content[m.start():]
                    f2.write(content)
                    # f.close()

        else:
            for m in re.finditer('Atlanta', content):
                occurCounter += 1
                # print pbender.listOfYear[i]
                # print "Atlanta"
                # print(m.start(), m.end())
                if occurCounter == 2:
                    content = content[m.start():]
                    f2.write(content)
                    # print content
                    # f.close()

# delete '......'
for i in range (0,28):
    with open('year' + str(pbender.listOfYear[i]) + 'v1' + '.txt', 'r+') as f:
        content = f.read()
        # f.close()
    with open('year' + str(pbender.listOfYear[i]) + 'v2' + '.txt', 'w+') as f2:
        content = content.replace('.','')
        f2.write(content)



# delete '-----' and find blank lines
for i in range (0,1):
    with open('year' + str(pbender.listOfYear[i]) + 'v2' + '.txt', 'r+') as f:
        lineNo = 0
        blankline = []
        with open('year' + str(pbender.listOfYear[i]) + 'v3' + '.txt', 'w+') as f2:
            for x in f:
                if "---" not in x:
                    f2.write(x)
                    lineNo += 1
                    if len(x)<2:
                        blankline.append(lineNo)
