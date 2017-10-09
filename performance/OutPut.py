files =[]
for i in range(1947,2018):
    files.append(open("C:/Users/yifan/Desktop/Performance/finalResult/"+str(i)+'.csv','a'))
source = open('results.csv','r')
for line in source:
    parts = line.replace('\n','').split('|');
    partsNew = []
    for part in parts:
        partsNew.append(part.replace(","," "))
    year = partsNew[2]
    # print len(partsNew)
    # print partsNew[0]+","+partsNew[1]+","+partsNew[2]+","+partsNew[3]+","+partsNew[4]+","+partsNew[5]+","+partsNew[6]+","+partsNew[7]+","+partsNew[8]+","+partsNew[9]+","+partsNew[10]+","+partsNew[11]+","+partsNew[12]+","+partsNew[13]+","+partsNew[14]+","+partsNew[15]+","+partsNew[16]+","+partsNew[17]+","+partsNew[18]+","+partsNew[19]+","+partsNew[20]+","+partsNew[21]+","+partsNew[22]+","+partsNew[23]+","+partsNew[24]+","++partsNew[25]
    print len(files)
    # print int(year)-1947
    files[int(year)-1947].write(partsNew[0]+","+partsNew[1]+","+partsNew[2]+","+partsNew[3]+","+partsNew[4]+","+partsNew[5]
                                +","+partsNew[6]+","+partsNew[7]+","+partsNew[8]+","+partsNew[9]+","+partsNew[10]+","
                                +partsNew[11]+","+partsNew[12]+","+partsNew[13]+","+partsNew[14]+","+partsNew[15]+","+partsNew[16]
                                +","+partsNew[17]+","+partsNew[18]+","+partsNew[19]+","+partsNew[20]+","+partsNew[21]+","
                                +partsNew[22]+","+partsNew[23]+","+partsNew[24]+","+partsNew[25]+'\n')

    # files[int(year)-1947].write(partsNew[0])


source.close()
for file in files:
    file.close()
print "Done!!"