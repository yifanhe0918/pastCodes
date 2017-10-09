import urllib2
import urllib
import re
import thread
import time
import sys
import csv
class Spider_Model:

    def __init__(self):
        self.playerList = []
        self.playerNames = []

    def getEachYear(self,year):
        myUrl = 'http://basketball.realgm.com/nba/players/'+str(year)
        req = urllib2.Request(myUrl)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        entry = re.findall('<td data-th="Player" class="nowrap" rel="(.*?)"><a href="(.*?)">(.*?)</a></td>', myPage, re.S)
        name=[]
        nameurl=[]
        for i in range(0,len(entry)):
            name.append(entry[i][2])
            nameurl.append(entry[i][1])
        teams = re.findall('<td data-th="Teams" rel="(.*?)"><a href', myPage, re.S)
        self.getDetailsMT(0,len(name),name,nameurl)


    def getDetailsMT(self,part,perpart,name,nameurl):
        with open('names.csv', 'a') as f:
            for i in range(part*perpart,(part+1)*perpart):
                if name[i] not in self.playerNames:
                    #self.getDetails(name[i],nameurl[i])
                    self.playerNames.append(name[i])
                    f.write(name[i]+","+nameurl[i]+"\n")


    def getDetails(self,name,url):
        myUrl = 'http://basketball.realgm.com' + url
        #print myUrl
        req = urllib2.Request(myUrl)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        # print myPage

        table = re.findall('<h2>NBA Regular Season Stats - Per Game(.*?)<td>CAREER</td>', myPage, re.S)
        stat=re.findall('<td>(.*?)</td>', table[0], re.S)
        teamDraft=re.findall('<td id="teamLinenba_reg_Per_Game(.*?)">(.*?)</td>', table[0], re.S)
        team = []
        # print stat
        for i in range(0,len(teamDraft)):
            team.append(teamDraft[i][1])


        table2 = re.findall('<h2>NBA Regular Season Stats - Advanced Stats(.*?)<td>CAREER</td>', myPage, re.S)
        stats2 = re.findall('<td>(.*?)</td>', table2[0], re.S)
        per =[]
        # print stats2
        for k in range(0,len(team)):
            per.append(stats2[k*19+18])
        # print per
        #
        # print team

        for j in range(0,len(team)):
            if str(stat[j*22][0:2])==str(19):
                stat[j * 22] = "19"+str(stat[j*22][5:7])
            else:
                stat[j * 22] = "20" + str(stat[j * 22][5:7])
            performanceByYear = PerformanceByYear(stat[j*22],team[j],stat[j*22+1],stat[j*22+2],stat[j*22+3],stat[j*22+4],stat[j*22+5],stat[j*22+6],stat[j*22+7],stat[j*22+8],stat[j*22+9],stat[j*22+10],stat[j*22+11],stat[j*22+12],stat[j*22+13],stat[j*22+14],stat[j*22+15],stat[j*22+16],stat[j*22+17],stat[j*22+18],stat[j*22+19],stat[j*22+20],stat[j*22+21],per[j])
            # print performanceByYear.year
            # print performanceByYear.team
            # print performanceByYear.gp
            # print performanceByYear.gs
            # print performanceByYear.pts
            # print performanceByYear.per
            player = Players(name,performanceByYear)
            self.playerList.append(player)



class Players:

    def __init__(self,name,performanceByYear):
        self.name=name
        self.year = performanceByYear.year
        self.performanceByYear=performanceByYear

class PerformanceByYear:

    def __init__(self,year,team,GP,GS,MIN,FGM,FGA,FG,PM3,PA3,P3,FTM,FTA,FT,OFF,DEF,TRB,AST,STL,BLK,PF,TOV,PTS,PER):
        self.year = year
        self.team = team
        self.gp = GP
        self.gs = GS
        self.min = MIN
        self.fgm = FGM
        self.fga = FGA
        self.fg = FG
        self.pm3 = PM3
        self.pa3 = PA3
        self.p3 = P3
        self.ftm = FTM
        self.fta = FTA
        self.ft = FT
        self.off = OFF
        self.def1 = DEF
        self.trb = TRB
        self.ast = AST
        self.stl = STL
        self.blk = BLK
        self.pf = PF
        self.tov = TOV
        self.pts = PTS
        self.per = PER



PlayerPerformance = Spider_Model()
names = []
urls = []
Results = []
with open('names.csv', 'r') as f:
    for line in f:
        names.append(line.replace('\n','').split(',')[0])
        urls.append(line.replace('\n','').split(',')[1])


for x in range(2001,3000):
    PlayerPerformance.getDetails(names[x],urls[x])
    print str(x)+"/"+str(1000)

for pp in PlayerPerformance.playerList:
    with open('result__2001-3000.csv', 'a') as f:
        f.write(pp.name+','+pp.performanceByYear.year+','+pp.performanceByYear.team +','+pp.performanceByYear.gp +','+pp.performanceByYear.gs +','+pp.performanceByYear.min +','+pp.performanceByYear.fgm +','+pp.performanceByYear.fga +','+pp.performanceByYear.fg +','+pp.performanceByYear.pm3 +','+pp.performanceByYear.pa3+','+pp.performanceByYear.p3 +','+pp.performanceByYear.ftm +','+pp.performanceByYear.fta +','+pp.performanceByYear.ft +','+pp.performanceByYear.off +','+pp.performanceByYear.def1 +','+pp.performanceByYear.trb +','+pp.performanceByYear.ast +','+pp.performanceByYear.stl +','+pp.performanceByYear.blk +','+pp.performanceByYear.pf +','+pp.performanceByYear.tov +','+pp.performanceByYear.pts +','+pp.performanceByYear.per+'\n')
