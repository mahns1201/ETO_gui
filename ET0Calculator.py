
##******************************************************************************
##** 
##**	   TITLE: ET0_PenmanMonteith_calc
##**            
##**	   OBJECTIVES: FAO Penman-Monteith 일기준증발산량(ET0) 계산
##**	   Description: 기상관측소별 일기준증발산량 계산
##**       Input: 날짜(YYYYMMDD), 최고온도(섭씨), 최저온도(섭씨), 평균풍속(%),
##**                평균풍속(m/s), 일조시간(hr) or 일조량(MJm^-2/day) 
##**       Output: 날짜(YYYYMMDD), 일기준증발산량(mm/day)
##**       Use: python ET0_PenmanMonteith_calc.py
##**	   Creator:  Jang, Min-Won (09/26/2018)
##**	   Modified:  Jang, Min-Won (09/26/2019)
##**
##**
##******************************************************************************
import tkinter as tk
import pandas as pd

import sys
import math
import datetime
import time
import os
import shutil

##01 Difference between times (days): 입력-String, 출력-Date
##def getDiffDay_Str(year, month, day):
##    input_day = datetime.date(year, month, day)
##    today = datetime.date.today()
##    delta = today - input_day
##    return delta.days 

##01 Difference between times (days): 입력-Date, 출력-Date
##def getDiffDay_Date(input_day, today):
##    delta = input_day - today
##    return delta.days


##01 Defining a function for reading the meteorological station information



def readinput_Metstation(Metstation):
    filein = open("metstation_2018.dat", 'r')
    line = filein.readline()

    while True:
        line = filein.readline()

        if not line:
            break

        anslist = line.split(',')

        if anslist[0] == str(Metstation):
            latitude = float(anslist[2])
            stationheight = float(anslist[4])
            anemoheight = float(anslist[7])
            break

    filein.close()

    return latitude, stationheight, anemoheight

##02 Defining a function for reading the daily climate data
def readinput_Climatefile(Metstation):
    filename = "MET" + str(Metstation) + ".csv"

    try:
        filein = open(filename, 'r', encoding='UTF8')
        line = filein.readline()

        dailyclimate = list()
        fmt = '%Y%m%d'
        
        while True:
            line = filein.readline()
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

        return dailyclimate
    
    except IOError:
        print("***  파일 읽기 오류: 파일이 없거나 내용에 오류가 있습니다.")
        sys.exit(1)

##03 Defining a function for calculating a daily Penman-Monteith reference evapotranspiration
def dailyReferenceET0_Sunhour (Metstation, day, Tmax, Tmin, RHmean, Windmean, Sunhour):

    try:
        metinfo = readinput_Metstation(Metstation)

        dt = datetime.datetime.strptime(day[:8],'%Y%m%d')
        JulianD = int(dt.timetuple().tm_yday) #Date를 Julian day로 변환
        
        Tmean = (Tmax + Tmin) / 2.0     #일평균기온(Celsius)
        #e0 = 0.6108 * math.exp(17.27*Tmean / (Tmean + 237.3)) #포화수증기압(최고기온, 최저기온 없을 경우)
        #es = 0.5 * (0.6108 * math.exp(17.27*Tmax / (Tmax+237.3)) + 0.6108 * math.exp(17.27*Tmin /(Tmin+237.3))) #평균포화수증기압(kPa)
        e0_tmax = 0.6108 * math.exp(17.27*Tmax / (Tmax + 237.3)) #포화수증기압
        e0_tmin = 0.6108 * math.exp(17.27*Tmin / (Tmin + 237.3)) #포화수증기압
        es = (e0_tmax + e0_tmin) / 2.0 #평균포화수증기압(kPa)
        
        ea = es * RHmean /100.0     #실제수증기압(kPa)
        P = 101.3 * math.pow( ((293.0-0.0065*metinfo[1]) / 293.0), 5.26)    #대기압
        gamma = 0.665 * math.pow(10, -3) * P    #건습계상수

        Ddelta = 4098 * 0.6108 * math.exp(17.27*Tmean/(Tmean + 237.3)) / (Tmean + 237.3)**2    #포화증기압 곡선 기울기(kPa/Celsius)

        Gsc = 0.082     #태양상수(MJm^-2min^-1)
        dr = 1+ 0.033 * math.cos(2*math.pi/365.0*JulianD)     # (radian)
        sdelta = 0.409 * math.sin(2*math.pi*JulianD/365.0 - 1.39)    # (radian)
        phi = math.radians(metinfo[0])    #위도를 radian으로 (북반구 +, 남반구 -, 위도 55도 이상인 경우 별도)
        omega_s = math.acos(-1 * math.tan(phi) * math.tan(sdelta))    #태양 일몰각
        Ra = 24*60/math.pi*Gsc*dr * (omega_s*math.sin(phi)*math.sin(sdelta) + math.cos(phi)*math.cos(sdelta)*math.sin(omega_s))
        
        N = 24 / math.pi * omega_s  #주간시간

        a_s, b_s = 0.25, 0.5
        Rs = (a_s + b_s*Sunhour/N) * Ra     #지표면 도달 태양복사에너지
        R_50 = (0.75 + 0.00002 * metinfo[1]) * Ra
        if Rs/R_50 > 1.0:
            print ("***  Rs / R_50 is greater than 1.0. It should be 0.33 ~ 1.0")
            #break
        alpha = 0.23    #하얀눈 0.95, 젖은토양면 0.05, 녹색작물 0.20~0.25 
        Rns = (1-alpha) * Rs

        sigma = 4.903 * math.pow(10,-9)     #Stefan-Bolzmann constant(MJ K^-4m^-2day^-1)
        Rnl = sigma * (math.pow(Tmax+273.16, 4) + math.pow(Tmin+273.16, 4)) / 2 * (0.34-0.14*math.pow(ea, 0.5)) * (1.35*Rs/R_50-0.35)   #순 복사에너지
        Rn = Rns - Rnl      #지구표면에 축적되는 에너지(MJ m^-2day^-1)

        G = 0.0     # 토양 열 유속, 1일 혹은 10일 단위 계산에선 무시

        u_2m = Windmean * 4.87 / math.log(67.8*metinfo[2] - 5.42)   #2m 높이 풍속

        T_Kv = 1.01 * (Tmean + 273)     #가온도
        R = 0.287       #고유기체상수 (KJ Kg^-1K^-1)
        rou_a = P / (T_Kv * R)      #평균대기밀도

        ETr_numerator = 0.408 * Ddelta * (Rn - G) + gamma*900/(Tmean+273)*u_2m*(es-ea)
        ETr_denumerator = Ddelta + gamma*(1+0.34*u_2m)
        ETr = ETr_numerator / ETr_denumerator       #FAO Penman-Monteith reference ET (mm/day)

        return ETr
    
    except IOError:
        print ("*** 파일 읽기 오류: 파일이 없거나 내용에 오류가 있습니다.")
        sys.exit(1)
    except ValueError:
        print ("*** 자료 형태가 적절하지 않습니다.")
        sys.exit(1)

##일조량(Rs): MJm^-2/day
def dailyReferenceET0_SolarRadiation (Metstation, day, Tmax, Tmin, RHmean, Windmean, SolarRadiation):

    try:
        metinfo = readinput_Metstation(Metstation)

        dt = datetime.datetime.strptime(day[:8],'%Y%m%d')
        JulianD = int(dt.timetuple().tm_yday) #Date를 Julian day로 변환
        
        Tmean = (Tmax + Tmin) / 2.0     #일평균기온(Celsius)
        #e0 = 0.6108 * math.exp(17.27*Tmean / (Tmean + 237.3)) #포화수증기압(최고기온, 최저기온 없을 경우)
        #es = 0.5 * (0.6108 * math.exp(17.27*Tmax / (Tmax+237.3)) + 0.6108 * math.exp(17.27*Tmin /(Tmin+237.3))) #평균포화수증기압(kPa)
        e0_tmax = 0.6108 * math.exp(17.27*Tmax / (Tmax + 237.3)) #포화수증기압
        e0_tmin = 0.6108 * math.exp(17.27*Tmin / (Tmin + 237.3)) #포화수증기압
        es = (e0_tmax + e0_tmin) / 2.0 #평균포화수증기압(kPa)
        
        ea = es * RHmean /100.0     #실제수증기압(kPa)
        P = 101.3 * math.pow( ((293.0-0.0065*metinfo[1]) / 293.0), 5.26)    #대기압
        gamma = 0.665 * math.pow(10, -3) * P    #건습계상수

        Ddelta = 4098 * 0.6108 * math.exp(17.27*Tmean/(Tmean + 237.3)) / (Tmean + 237.3)**2    #포화증기압 곡선 기울기(kPa/Celsius)

        Gsc = 0.082     #태양상수(MJm^-2min^-1)
        dr = 1+ 0.033 * math.cos(2*math.pi/365.0*JulianD)     # (radian)
        sdelta = 0.409 * math.sin(2*math.pi*JulianD/365.0 - 1.39)    # (radian)
        phi = math.radians(metinfo[0])    #위도를 radian으로 (북반구 +, 남반구 -, 위도 55도 이상인 경우 별도)
        omega_s = math.acos(-1 * math.tan(phi) * math.tan(sdelta))    #태양 일몰각
        Ra = 24*60/math.pi*Gsc*dr * (omega_s*math.sin(phi)*math.sin(sdelta) + math.cos(phi)*math.cos(sdelta)*math.sin(omega_s))
        
        N = 24 / math.pi * omega_s  #주간시간

        a_s, b_s = 0.25, 0.5
        Rs = SolarRadiation     #지표면 도달 태양복사에너지
        R_50 = (0.75 + 0.00002 * metinfo[1]) * Ra
        if Rs/R_50 > 1.0:
            print ("***  Rs / R_50 is greater than 1.0. It should be 0.33 ~ 1.0")
            #break
        alpha = 0.23    #하얀눈 0.95, 젖은토양면 0.05, 녹색작물 0.20~0.25 
        Rns = (1-alpha) * Rs

        sigma = 4.903 * math.pow(10,-9)     #Stefan-Bolzmann constant(MJ K^-4m^-2day^-1)
        Rnl = sigma * (math.pow(Tmax+273.16, 4) + math.pow(Tmin+273.16, 4)) / 2 * (0.34-0.14*math.pow(ea, 0.5)) * (1.35*Rs/R_50-0.35)   #순 복사에너지
        Rn = Rns - Rnl      #지구표면에 축적되는 에너지(MJ m^-2day^-1)

        G = 0.0     # 토양 열 유속, 1일 혹은 10일 단위 계산에선 무시

        u_2m = Windmean * 4.87 / math.log(67.8*metinfo[2] - 5.42)   #2m 높이 풍속

        T_Kv = 1.01 * (Tmean + 273)     #가온도
        R = 0.287       #고유기체상수 (KJ Kg^-1K^-1)
        rou_a = P / (T_Kv * R)      #평균대기밀도

        ETr_numerator = 0.408 * Ddelta * (Rn - G) + gamma*900/(Tmean+273)*u_2m*(es-ea)
        ETr_denumerator = Ddelta + gamma*(1+0.34*u_2m)
        ETr = ETr_numerator / ETr_denumerator       #FAO Penman-Monteith reference ET (mm/day)

        return ETr
    
    except IOError:
        print ("*** 파일 읽기 오류: 파일이 없거나 내용에 오류가 있습니다.")
        sys.exit(1)
    except ValueError:
        print ("*** 자료 형태가 적절하지 않습니다.")
        sys.exit(1)
        
##04 Defining a main function for printing out the daily ET0
def fileET_calculation(Metstation, SOLAR):

##    today = datetime.date.today()

    try:
        print("[ 기상자료 읽는 중....... ]")
        inclimate = readinput_Climatefile(Metstation)
 
        filename = "PMET0_"+Metstation+ ".dat"
        fileout = open(filename, 'w')
        fileout.write ("\nDate(yyyymmdd)  P-M ET0(mm)")
        fileout.write ("\n=================================")

        dailyclimate = list()
        for n in range(0, len(inclimate)):
            if SOLAR == "1":
                pet = dailyReferenceET0_Sunhour(Metstation, inclimate[n][0], inclimate[n][1], inclimate[n][2], inclimate[n][3], inclimate[n][4], inclimate[n][5])
            else:
                pet = dailyReferenceET0_SolarRadiation(Metstation, inclimate[n][0], inclimate[n][1], inclimate[n][2], inclimate[n][3], inclimate[n][4], inclimate[n][5])
            climate  = [inclimate[n][0], inclimate[n][6], round(pet,2)]
            fileout.write ("\n%s       %5.1f" % (inclimate[n][0], pet))
            dailyclimate.append(climate)
        if len(dailyclimate) == 0:
            print (" 기상예보가 없습니다. ")
            sys.exit(1)
        else:
            print (".... %s부터 %s까지 %d일간 계산하였습니다." % (dailyclimate[0][0], dailyclimate[len(dailyclimate)-1][0], len(dailyclimate)))

        fileout.close()

        print ("실행을 성공적으로 완료하였습니다.")
        time.sleep(1)

    except IOError:
        print ("파입 출력 오류: 실행을 종료합니다.")
        sys.exit(0)
        

'''
def import_csv_data():
    global v
    global csv_file_path

    csv_file_path = askopenfilename()
    print(csv_file_path)
    v.set(csv_file_path)
    df = pd.read_csv(csv_file_path, encoding = 'cp949')

    print(df)

    return csv_file_path

SOLAR = 0

def solar_time():
    global SOLAR
    SOLAR = '1'

    print("일조시간을 선택하셨습니다.")
    return SOLAR

def solar_amount():
    global SOLAR
    SOLAR = '2'

    print("일조량을 선택하셨습니다.")
    return SOLAR

root = tk.Tk()
root.title("기준증발산량 계산")
tk.Label(root, text='파일 순서: ').grid(row = 0, column = 0)
tk.Label(root, text='날짜, 최고기온, 최저기온, 상대습도, 평균풍속, 일조시간 or 일조량').grid(row = 0, column = 1)
v = tk.StringVar()
entry = tk.Entry(root, textvariable=v).grid(row = 1, column = 1)

tk.Button(root, text = 'Browse',command=import_csv_data).grid(row = 1, column = 0)
tk.Button(root, text = "일조시간", command = lambda: solar_time()).grid(row = 2, column = 0)
tk.Button(root, text = "일조량", command = lambda: solar_amount()).grid(row = 2, column = 1)
tk.Button(root, text = '확인',command = root.destroy).grid(row = 2, column = 2)

root.mainloop()
'''

'''
csv_file_path = csv_file_path.split('/')
Metstation = csv_file_path[-1]
Metstation = Metstation[3:6]



def main():
    if SOLAR == "1" or SOLAR == "2":
        print ("%s를 선택하셨습니다." % SOLAR)

    else:
        print ("잘못 선택하셨습니다. 1과 2 중에 하나만 입력하세요!")
        sys.exit(0)
    
    fileET_calculation(Metstation, SOLAR)
'''
        
