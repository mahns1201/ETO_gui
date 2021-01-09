import pandas as pd
import sys

def readinput_Climatefile(Metstation):
    filename = "MET" + str(Metstation) + ".csv"

    try:
        df = pd.read_csv(filename, 'r', encoding="cp949")

        dailyclimate = []
        fmt = '%Y%m%d'

        for i in range(0, len(df)):
            anslist = df.iloc[i].split(',')
            print(anslist[0])

            '''
            temp = dailyclimate[0]
            anslist.append(temp)
    
            anslist[0] = temp[:8]

            for n in range(1,len(anslist)-1):
                anslist[n] = float(anslist[n])

            dailyclimate.append(anslist)
            '''

        # return dailyclimate
    
    except IOError:
        print("***  파일 읽기 오류: 파일이 없거나 내용에 오류가 있습니다.")
        sys.exit(1)

Metstation = "090"
test = readinput_Climatefile(Metstation)
print(test)