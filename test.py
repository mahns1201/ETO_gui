import sys

##02 Defining a function for reading the daily climate data
def readinput_Climatefile():
    filename = "MET090.csv"

    try:
        filein = open(filename, 'r', encoding="UTF8")
        line = filein.readline()

        dailyclimate = []
        # fmt = '%Y%m%d'
        
        while True:
            line = filein.readline()

            print(line)

            if not line:
                break
            anslist = line.split(',')
            temp = anslist[0]
            anslist.append(temp)
 
            anslist[0] = temp[:8]    
  
            for n in range(1,len(anslist)-1):
                anslist[n] = float(anslist[n])
            dailyclimate.append(anslist)
            
        filein.close()
        
        # print(dailyclimate)

        return dailyclimate
    
    except IOError:
        print("***  파일 읽기 오류: 파일이 없거나 내용에 오류가 있습니다.")
        sys.exit(1)

readinput_Climatefile()