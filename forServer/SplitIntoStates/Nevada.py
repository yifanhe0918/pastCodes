__author__ = 'YifanHe'

import urllib2
import urllib
import re
import thread
import time
import sys
import csv
import os
import os.path

class Spider_Model:
    def __init__(self):
        self.states = []
        self.entriesByStates = []
        self.totalEntries = 0
        self.entryIds=[]

#### To get state list
    def getStates(self):
        myUrl = 'http://search.ancestry.com/Browse/Controls/List/BrowseHandler.ashx?skipall=1&root=1&dbid' \
                '=1264&path=Nevada&pageName=ancestry%20us%20%3A%20search%20%3A%20form%20%3A%20database'
        req = urllib2.Request(myUrl)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        states = re.findall('value="(.*?)"', myPage, re.S)
        states = states[1:]
        self.states = states
        totalEntries = 0
        for i in states:
            totalEntries += len(i)
        print self.states
        self.totalEntries = totalEntries

### To get entries name and first page number of each state
    def getEntries(self,state):
        # print state
        myUrl = 'http://search.ancestry.com/Browse/Controls/List/BrowseHandler.ashx?skipall=1&root=1&dbid=1264&path='\
                +state\
                +'&pageName=ancestry%20us%20%3A%20search%20%3A%20form%20%3A%20database'
        req = urllib2.Request(myUrl)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        # print myPage
        entryRaw = re.findall('dbid=1264&b=1&iid=(.*?)&nbsp', myPage, re.S)
        # print entryRaw
        entryListOfThisState = []
        for i in entryRaw:
            # print i
            # print "2"
            # time.sleep(2)
            entryId = re.findall('rhusa(.*?)&',i, re.S)
            entryName = re.findall('">(.*?)</a>',i, re.S)
            entry = [entryId[0],entryName[0]]
            entryListOfThisState.append(entry)
            self.entryIds.append(entryId[0])
            # print entry
        self.entriesByStates.append(entryListOfThisState)
        print entryListOfThisState
        # print entryListOfThisState

    def iterateStatesToGetEntries(self):
        for i in self.states:
            print i
            self.getEntries(i)


    ###############
    ##### Start grabbing
    ###############


    def iterateEntries(self):
        cond = True ######### CONDITION
        counter = 0
        for i in range(0,len(self.states)):
            if self.states[i] == 'Nevada': ######### CONDITION
                entries = self.entriesByStates[i]
                print entries
                dir = 'output/'+self.states[i]
                if not os.path.exists(dir):
                    os.makedirs(dir)
                for j in range(0,len(entries)):
                    id = entries[j][0]
                    name = entries[j][1]
                    print id
                    if id == '1862_101641-00000': ######### CONDITION
                        cond = True ######### CONDITION
                    print name
                    dir2 = 'output/' + self.states[i] + '/' + name
                    if not os.path.exists(dir2):
                        os.makedirs(dir2)
                    counter += 1
                    # if j != len(entries)-1:
                    #     nextId = entries[j+1][0]
                    # else:
                    #     nextId = 0
                    if cond:
                        self.iteratePics(self.states[i], id, name,i)
                    # print str(counter)+'/'+str(self.totalEntries)
                f = open(self.states[i]+"done.txt",'w')
                f.close()


    def iteratePics(self,state,id,name,stateIndex):
        # print id
        # idParts1 = id.split('_')
        # id1 = idParts1[0]
        # idParts2 = idParts1[1].split('-')
        # id2 = idParts2[0]
        # idPage = idParts2[1]
        # idPageLen = len(idPage)
        # idPageNum = int(idPage)
        # continounsError = 0
        dir2 = 'output/' + state +'/'+ name

        opener = urllib2.build_opener()
        cookie = 'ANCUUID=599a2c0d687543aa9315037112aa1fd3; an_split=39; fsr.r=%7B%22d%22%3A90%2C%22i%22%3A%22de358f7-93567997-da1c-9539-351a4%22%2C%22e%22%3A1480363905574%7D; __gads=ID=016f877c9eb75b05:T=1479981416:S=ALNI_MZMddMdmGV42JMOEPDoJv1CiFlsLg; giftingCombo2016=1; ATT=FlPhhlUDcAhyhEAGOVJzSE*CvPQZweIAbqSaEY; ANCATT=FlPhhlUDcAhyhEAGOVJzSE*CvPQZweIAbqSaEY; LAU=04692a9b-0006-0000-0000-000000000000; VARS=LCID=1033&COUNTRYCODE=US&WTT=U-v7eeHjVGZB9nGA6aoG7F*CvPA4TeIAbqSaEY&UR=32768&UREXP=11/26/2016 11:37:13 PM&NEWSFLAGS=5242881&USID=5002B8C3-6230-4241-BA9C-F9D90E81E6C5&NODOUBLEBILLSTATEFOUND=11/25/2016 11:45:53 PM&ABANNER=636157143535605512; RMEATT=FlPhhlUDcAhyhEAGOVJzSE*CvPQZweIAbqSaEY; OMNITURE=TYPE=Trialer; ANCSESSIONID=99878cdf-d62e-40eb-93e1-fea7af3db215; BAIT=Id%3d04692a9b-0006-0000-0000-000000000000%3bLanguage%3dEnglish%3bOldDna%3d0%3bFreeDnaUp%3d0%3bDnaPilot%3d0%3bNewDna%3d0%3bDnaGF%3d0%3bDnaDSP%3d0%3bDnaDSAC%3d0%3bht%3d1%3btn%3d1-5%3brt%3dd8-14%3bct%3d%3bcr%3d%3bownership%3dAncestry_World_Deluxe%3bhasgs%3d0%3bhadgs%3d0%3bbuygs%3d0%3bduration%3dDays_14%3bCSub%3d0%3bESub%3d0%3bCTrial%3d1%3bETrial%3d1%3bBT%3dM%3bLSub%3d%3bLSubDuration%3d%3bLSubPrice%3d0.00%3bLSubCurrency%3d%3bDSSE%3d0%3bLoggedIn%3d1%3bNBP_ONSITE%3d1234%3bINF_ONSITE%3d1234%3bCOL_ONSITE%3d1234%3bGEN_ONSITE%3d1234%3bRegType%3dUnknown%3bdne%3d0%3beoi%3d1; an_s_split=78; fs_dnaQ=0; _gat_Google_Universal_Analytics=1; TI.SI=0; TI=0; mbox=PC#1479755227295-658620.20_53#1482784642|session#1480192636400-41919#1480194502; VARSESSION=S=GmsEpZ3tukaEp0187JsZqg%3d%3d&SLI=1&ITT=FlPhhlUDcAhyhEAGOVJzSE*CvPQZweIAbqSaEY&URE=5lZXPwgC-X4KH8B-jmFRzF*CvPQZweI*LIBppymAY&UG=1&ISAIALE=040f47ca78d&ACCTSTAT=0&HASPIV=False&LOGINNAME=xiaxinwang&FAILBILL=0|1/1/0001 12:00:00 AM&CLSRM=0; OMNITURET=MR=1033; utag_main=v_id:0158883ece61001c69288fa7456f0507800330700093c$_sn:18$_ss:0$_st:1480194445643$dc_visit:4$ses_id:1480192637321%3Bexp-session$_pn:3%3Bexp-session$dc_event:1%3Bexp-session$mm_uuid:a4bd5669-dfb0-4900-ac3c-d609f281eda4%3Bexp-session$dc_region:us-east-1%3Bexp-session; gpv_pn=ancestry%20us%20%3A%20search%20%3A%20form%20%3A%20database; an_hasTree=1; s_cc=true; s_sq=%5B%5BB%5D%5D; _ga=GA1.2.865662395.1479754568; s_vi=[CS]v1|2C19A1A385032FDD-6000118B80001619[CE]; PrefID=49-3973468961; _gali=browseOptions0; SOURCES=DID=3&DDD=11%2f26%2f2016+13%3a37%3a40; fsr.s=%7B%22v1%22%3A-1%2C%22v2%22%3A-2%2C%22rid%22%3A%22de358f7-93567997-da1c-9539-351a4%22%2C%22to%22%3A2.8%2C%22c%22%3A%22http%3A%2F%2Fsearch.ancestry.com%2Fsearch%2Fdb.aspx%22%2C%22pv%22%3A3%2C%22lc%22%3A%7B%22d6%22%3A%7B%22v%22%3A3%2C%22s%22%3Atrue%7D%7D%2C%22cd%22%3A6%2C%22f%22%3A1480192662160%2C%22sd%22%3A6%7D'
        opener.addheaders.append(('Cookie', cookie))

        # checkDup=[]
        # for p in self.entriesByStates[stateIndex]:
        #     # print p
        #     checkDup.append(p[0])
        # print checkDup
        # if counter == len(checkDup)-1:
        #     checkDup = []
        # else:
        #     print counter
        #     partA = checkDup[counter + 1:]
        #     partB = checkDup[:counter]
        #     checkDup=[]
        #     for i in partA:
        #         checkDup.append(i)
        #     for i in partB:
        #         checkDup.append(i)

        # print 'checkdup'
        # print checkDup
        # myUrl = 'http://interactive.ancestry.com/api/v2/Media/GetMediaInfo/1264/rhusa'+id+'/1'
                # + id1 + '_' + id2 + '-' + str(
            # idPageNum).zfill(idPageLen) + '/1'

        currentId = id


        nextPicId = 0000
        while currentId != 'null':



                                # continounsError<10 and (id1+'_'+id2+'-'+str(idPageNum).zfill(idPageLen) not in checkDup ): # The page numbers are not continuous and i'm trying to find the end of entries
            # print id1+'_'+id2+'-'+str(idPageNum).zfill(idPageLen)
            # print nextId
            # print nextId==id1+'_'+id2+'-'+str(idPageNum).zfill(idPageLen)

            # modifiedIdList = currentId.split('-')
            # temp = int(modifiedIdList[1])
            # modifiedId = modifiedIdList[0]+'-'+ str(temp)
            saveAs = dir2+'/'+name+"_"+currentId+'.jpg'
            # op = saveAs.split('/')

            # time.sleep(0.1)
            myUrl = 'http://interactive.ancestry.com/api/v2/Media/GetMediaInfo/1264/rhusa' + currentId + '/1'

            myPage = opener.open(myUrl).read()
            # print "RawUrl is okay"

            nextPicIdList = re.findall('NextImageId":(.*?),', myPage, re.S)
            nextPicId = nextPicIdList[0].replace('"', '')
            nextPicId = nextPicId.replace('rhusa', '')

            # currentId = nextPicId

            if not os.path.exists(saveAs):

                picUrlList = re.findall('ImageServiceUrlForPrint":"(.*?)"', myPage, re.S)
                picUrl = picUrlList[0]
                try:
                    picPage = opener.open(picUrl).read()
                except Exception as e:
                    time.sleep(0.5)
                    print "Let me do it again 8=====>"
                    picPage = opener.open(picUrl).read()
                f = open(saveAs, 'wb')
                print "Just saved "+ state + " | "+name+" | "+currentId
                currentId = nextPicId

                # # if "An error has occurred." in myPage:
                # #     continounsError += 1
                # #     idPageNum += 1
                # try:
                #     myPage = opener.open(myUrl).read()
                #     print "RawUrl is okay"
                #     picUrlList = re.findall('ImageServiceUrlForPrint":"(.*?)"', myPage, re.S)
                #     picUrl = picUrlList[0]
                #     print "PicUrl is okay"
                #     picPage = opener.open(picUrl).read()
                #     f = open(saveAs, 'wb')
                #     print "get "+state+ ' '+op[-1]+" done"
                #     print
                #     f.write(picPage)
                #     f.close()
                #     continounsError = 0
                #     idPageNum += 1
                # except urllib2.HTTPError:
                #     print 'rawUrl: '+myUrl
                #     print "This page "+name+"_"+id1+'_'+id2+'-'+str(idPageNum)+" does not exist"
                #     print
                #     continounsError += 1
                #     idPageNum += 1
            else:
                # idPageNum += 1
                print "Already have "+ state + " | "+name+" | "+currentId
                continounsError = 0
                currentId = nextPicId

archives = Spider_Model()
archives.getStates()
archives.iterateStatesToGetEntries()
# print archives.entryIds
archives.iterateEntries()