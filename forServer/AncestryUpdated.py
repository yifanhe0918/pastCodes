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
                '=1264&path=Alabama&pageName=ancestry%20us%20%3A%20search%20%3A%20form%20%3A%20database'
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
            if self.states[i] == 'Alabama': ######### CONDITION
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
        cookie = 'ANCUUID=14586063e9a24a129f778ba9a0e7e38f; an_split=93; __gads=ID=b51fe0690ca4af60:T=1479539401:S=ALNI_Mbstn_5KBsXkiK2CeLDdmTPKs-w3g; fsr.r=%7B%22d%22%3A90%2C%22i%22%3A%22d44bc89-86357296-ab50-5fb2-85f42%22%2C%22e%22%3A1480144989190%7D; WRUID=2097027762.2073572126; __CT_Data=gpv=9&apv_53161_www=7&cpv_53161_www=1; ATT=jS3XSULQT2OcrVWQI0zCAG*CvPAsheIAbqSaEY; ANCATT=jS3XSULQT2OcrVWQI0zCAG*CvPAsheIAbqSaEY; LAU=04692a9b-0006-0000-0000-000000000000; RMEATT=jS3XSULQT2OcrVWQI0zCAG*CvPAsheIAbqSaEY; OMNITURE=TYPE=Trialer; ANCSESSIONID=199e2c31-6ae4-4ce0-b5f1-e1b15bf881ba; BAIT=Id%3d04692a9b-0006-0000-0000-000000000000%3bLanguage%3dEnglish%3bOldDna%3d0%3bFreeDnaUp%3d0%3bDnaPilot%3d0%3bNewDna%3d0%3bDnaGF%3d0%3bDnaDSP%3d0%3bDnaDSAC%3d0%3bht%3d1%3btn%3d1-5%3brt%3dd1-7%3bct%3d%3bcr%3d%3bownership%3dAncestry_World_Deluxe%3bhasgs%3d0%3bhadgs%3d0%3bbuygs%3d0%3bduration%3dDays_14%3bCSub%3d0%3bESub%3d0%3bCTrial%3d1%3bETrial%3d1%3bBT%3dM%3bLSub%3d%3bLSubDuration%3d%3bLSubPrice%3d0.00%3bLSubCurrency%3d%3bDSSE%3d0%3bLoggedIn%3d1%3bNBP_ONSITE%3d1234%3bINF_ONSITE%3d1234%3bCOL_ONSITE%3d1234%3bGEN_ONSITE%3d1234%3bRegType%3dUnknown%3bdne%3d0%3beoi%3d1; TI.SI=0; TI=0; VARS=LCID=1033&WTT=Gsd_pUMeVYcmUs2muE40WG*CvPQ3FeIAbqSaEY&UR=32768&UREXP=11/24/2016 8:52:31 AM&USID=D732EED6-47CA-414F-9CED-DD3A8312F0A6&COUNTRYCODE=US&NODOUBLEBILLSTATEFOUND=11/23/2016 10:52:34 PM&S1=1&NEWSFLAGS=5242881; an_s_split=14; fs_dnaQ=0; OMNITURET=MR=1033; PrefID=12-4676627539; VARSESSION=S=g73npvotL06wIYhHlqc74Q%3d%3d&SLI=1&ITT=jS3XSULQT2OcrVWQI0zCAG*CvPAsheIAbqSaEY&URE=52XMZn_ocPM3qB6_sFZtvE*CvPAsheI*LIBppymAY&UG=1&ISAIALE=028ab3c862f&ACCTSTAT=0&HASPIV=False&LOGINNAME=xiaxinwang&FAILBILL=0|1/1/0001 12:00:00 AM&CLSRM=0&CVREF=bcol:d=1264,p=; mbox=PC#1479539354833-795767.28_87#1482565454|session#1479973453018-407657#1479975314; s_cc=true; _ga=GA1.2.211774191.1479539356; CBROWSES=PATHDB=1264&PATH=Colorado.Arapahoe+through+Weld+Counties%3b+1864; utag_main=v_id:01587b6aeede00079e02e59d4d2505072001806a00bd0$_sn:17$_ss:0$_st:1479975904979$dc_visit:5$ses_id:1479966755275%3Bexp-session$_pn:14%3Bexp-session$dc_event:1%3Bexp-session$mm_uuid:4bb657f0-8288-4d00-8942-b34ff07284e6%3Bexp-session$dc_region:us-east-1%3Bexp-session; gpv_pn=ancestry%20us%20%3A%20interactive%20image%20%3A%20forms%20%3A%20imageload; an_hasTree=1; s_sq=%5B%5BB%5D%5D; s_vi=[CS]v1|2C17FD4D05013ED3-4000010A600042D4[CE]; SOURCES=DID=3&DDD=11%2f24%2f2016+01%3a23%3a11&CID=78f0deff-d005-4a1b-a25e-e000ffe21e8c; fsr.s=%7B%22v1%22%3A-1%2C%22v2%22%3A-2%2C%22rid%22%3A%22d44bc89-86357296-ab50-5fb2-85f42%22%2C%22to%22%3A4.6%2C%22c%22%3A%22http%3A%2F%2Finteractive.ancestry.com%2F1264%2Frhusa1862_101373-00396%22%2C%22pv%22%3A14%2C%22lc%22%3A%7B%22d6%22%3A%7B%22v%22%3A14%2C%22s%22%3Atrue%7D%7D%2C%22cd%22%3A6%2C%22f%22%3A1479975793075%2C%22sd%22%3A6%7D'
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