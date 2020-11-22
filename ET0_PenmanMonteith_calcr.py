# -*- coding: cp949 -*-
##******************************************************************************
##** 
##**	   TITLE: ET0_PenmanMonteith_calc
##**            
##**	   OBJECTIVES: FAO Penman-Monteith �ϱ������߻귮(ET0) ���
##**	   Description: �������Һ� �ϱ������߻귮 ���
##**       Input: ��¥(YYYYMMDD), �ְ�µ�(����), �����µ�(����), ���ǳ��(%),
##**                ���ǳ��(m/s), �����ð�(hr) or ������(MJm^-2/day) 
##**       Output: ��¥(YYYYMMDD), �ϱ������߻귮(mm/day)
##**       Use: python ET0_PenmanMonteith_calc.py
##**	   Creator:  Jang, Min-Won (09/26/2018)
##**	   Modified:  Jang, Min-Won (09/26/2019)
##**
##**
##******************************************************************************

import sys
import math
import datetime
import time
import os
import shutil

##01 Difference between times (days): �Է�-String, ���-Date
##def getDiffDay_Str(year, month, day):
##    input_day = datetime.date(year, month, day)
##    today = datetime.date.today()
##    delta = today - input_day
##    return delta.days 

##01 Difference between times (days): �Է�-Date, ���-Date
##def getDiffDay_Date(input_day, today):
##    delta = input_day - today
##    return delta.days


##01 Defining a function for reading the meteorological station information
def readinput_Metstation(Metstation):
    filein = open("metstation_2018.dat",'r')
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
        filein = open(filename,'r')
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
        print("***  ���� �б� ����: ������ ���ų� ���뿡 ������ �ֽ��ϴ�.")
        sys.exit(1)
        



##03 Defining a function for calculating a daily Penman-Monteith reference evapotranspiration
def dailyReferenceET0_Sunhour (Metstation, day, Tmax, Tmin, RHmean, Windmean, Sunhour):

    try:
        metinfo = readinput_Metstation(Metstation)

        dt = datetime.datetime.strptime(day[:8],'%Y%m%d')
        JulianD = int(dt.timetuple().tm_yday) #Date�� Julian day�� ��ȯ
        
        Tmean = (Tmax + Tmin) / 2.0     #����ձ��(Celsius)
        #e0 = 0.6108 * math.exp(17.27*Tmean / (Tmean + 237.3)) #��ȭ�������(�ְ���, ������� ���� ���)
        #es = 0.5 * (0.6108 * math.exp(17.27*Tmax / (Tmax+237.3)) + 0.6108 * math.exp(17.27*Tmin /(Tmin+237.3))) #�����ȭ�������(kPa)
        e0_tmax = 0.6108 * math.exp(17.27*Tmax / (Tmax + 237.3)) #��ȭ�������
        e0_tmin = 0.6108 * math.exp(17.27*Tmin / (Tmin + 237.3)) #��ȭ�������
        es = (e0_tmax + e0_tmin) / 2.0 #�����ȭ�������(kPa)
        
        ea = es * RHmean /100.0     #�����������(kPa)
        P = 101.3 * math.pow( ((293.0-0.0065*metinfo[1]) / 293.0), 5.26)    #����
        gamma = 0.665 * math.pow(10, -3) * P    #�ǽ�����

        Ddelta = 4098 * 0.6108 * math.exp(17.27*Tmean/(Tmean + 237.3)) / (Tmean + 237.3)**2    #��ȭ����� � ����(kPa/Celsius)

        Gsc = 0.082     #�¾���(MJm^-2min^-1)
        dr = 1+ 0.033 * math.cos(2*math.pi/365.0*JulianD)     # (radian)
        sdelta = 0.409 * math.sin(2*math.pi*JulianD/365.0 - 1.39)    # (radian)
        phi = math.radians(metinfo[0])    #������ radian���� (�Ϲݱ� +, ���ݱ� -, ���� 55�� �̻��� ��� ����)
        omega_s = math.acos(-1 * math.tan(phi) * math.tan(sdelta))    #�¾� �ϸ���
        Ra = 24*60/math.pi*Gsc*dr * (omega_s*math.sin(phi)*math.sin(sdelta) + math.cos(phi)*math.cos(sdelta)*math.sin(omega_s))
        
        N = 24 / math.pi * omega_s  #�ְ��ð�

        a_s, b_s = 0.25, 0.5
        Rs = (a_s + b_s*Sunhour/N) * Ra     #��ǥ�� ���� �¾纹�翡����
        R_50 = (0.75 + 0.00002 * metinfo[1]) * Ra
        if Rs/R_50 > 1.0:
            print ("***  Rs / R_50 is greater than 1.0. It should be 0.33 ~ 1.0")
            #break
        alpha = 0.23    #�Ͼᴫ 0.95, �������� 0.05, ����۹� 0.20~0.25 
        Rns = (1-alpha) * Rs

        sigma = 4.903 * math.pow(10,-9)     #Stefan-Bolzmann constant(MJ K^-4m^-2day^-1)
        Rnl = sigma * (math.pow(Tmax+273.16, 4) + math.pow(Tmin+273.16, 4)) / 2 * (0.34-0.14*math.pow(ea, 0.5)) * (1.35*Rs/R_50-0.35)   #�� ���翡����
        Rn = Rns - Rnl      #����ǥ�鿡 �����Ǵ� ������(MJ m^-2day^-1)

        G = 0.0     # ��� �� ����, 1�� Ȥ�� 10�� ���� ��꿡�� ����

        u_2m = Windmean * 4.87 / math.log(67.8*metinfo[2] - 5.42)   #2m ���� ǳ��

        T_Kv = 1.01 * (Tmean + 273)     #���µ�
        R = 0.287       #������ü��� (KJ Kg^-1K^-1)
        rou_a = P / (T_Kv * R)      #��մ��е�

        ETr_numerator = 0.408 * Ddelta * (Rn - G) + gamma*900/(Tmean+273)*u_2m*(es-ea)
        ETr_denumerator = Ddelta + gamma*(1+0.34*u_2m)
        ETr = ETr_numerator / ETr_denumerator       #FAO Penman-Monteith reference ET (mm/day)

        return ETr
    
    except IOError:
        print ("*** ���� �б� ����: ������ ���ų� ���뿡 ������ �ֽ��ϴ�.")
        sys.exit(1)
    except ValueError:
        print ("*** �ڷ� ���°� �������� �ʽ��ϴ�.")
        sys.exit(1)

##������(Rs): MJm^-2/day
def dailyReferenceET0_SolarRadiation (Metstation, day, Tmax, Tmin, RHmean, Windmean, SolarRadiation):

    try:
        metinfo = readinput_Metstation(Metstation)

        dt = datetime.datetime.strptime(day[:8],'%Y%m%d')
        JulianD = int(dt.timetuple().tm_yday) #Date�� Julian day�� ��ȯ
        
        Tmean = (Tmax + Tmin) / 2.0     #����ձ��(Celsius)
        #e0 = 0.6108 * math.exp(17.27*Tmean / (Tmean + 237.3)) #��ȭ�������(�ְ���, ������� ���� ���)
        #es = 0.5 * (0.6108 * math.exp(17.27*Tmax / (Tmax+237.3)) + 0.6108 * math.exp(17.27*Tmin /(Tmin+237.3))) #�����ȭ�������(kPa)
        e0_tmax = 0.6108 * math.exp(17.27*Tmax / (Tmax + 237.3)) #��ȭ�������
        e0_tmin = 0.6108 * math.exp(17.27*Tmin / (Tmin + 237.3)) #��ȭ�������
        es = (e0_tmax + e0_tmin) / 2.0 #�����ȭ�������(kPa)
        
        ea = es * RHmean /100.0     #�����������(kPa)
        P = 101.3 * math.pow( ((293.0-0.0065*metinfo[1]) / 293.0), 5.26)    #����
        gamma = 0.665 * math.pow(10, -3) * P    #�ǽ�����

        Ddelta = 4098 * 0.6108 * math.exp(17.27*Tmean/(Tmean + 237.3)) / (Tmean + 237.3)**2    #��ȭ����� � ����(kPa/Celsius)

        Gsc = 0.082     #�¾���(MJm^-2min^-1)
        dr = 1+ 0.033 * math.cos(2*math.pi/365.0*JulianD)     # (radian)
        sdelta = 0.409 * math.sin(2*math.pi*JulianD/365.0 - 1.39)    # (radian)
        phi = math.radians(metinfo[0])    #������ radian���� (�Ϲݱ� +, ���ݱ� -, ���� 55�� �̻��� ��� ����)
        omega_s = math.acos(-1 * math.tan(phi) * math.tan(sdelta))    #�¾� �ϸ���
        Ra = 24*60/math.pi*Gsc*dr * (omega_s*math.sin(phi)*math.sin(sdelta) + math.cos(phi)*math.cos(sdelta)*math.sin(omega_s))
        
        N = 24 / math.pi * omega_s  #�ְ��ð�

        a_s, b_s = 0.25, 0.5
        Rs = SolarRadiation     #��ǥ�� ���� �¾纹�翡����
        R_50 = (0.75 + 0.00002 * metinfo[1]) * Ra
        if Rs/R_50 > 1.0:
            print ("***  Rs / R_50 is greater than 1.0. It should be 0.33 ~ 1.0")
            #break
        alpha = 0.23    #�Ͼᴫ 0.95, �������� 0.05, ����۹� 0.20~0.25 
        Rns = (1-alpha) * Rs

        sigma = 4.903 * math.pow(10,-9)     #Stefan-Bolzmann constant(MJ K^-4m^-2day^-1)
        Rnl = sigma * (math.pow(Tmax+273.16, 4) + math.pow(Tmin+273.16, 4)) / 2 * (0.34-0.14*math.pow(ea, 0.5)) * (1.35*Rs/R_50-0.35)   #�� ���翡����
        Rn = Rns - Rnl      #����ǥ�鿡 �����Ǵ� ������(MJ m^-2day^-1)

        G = 0.0     # ��� �� ����, 1�� Ȥ�� 10�� ���� ��꿡�� ����

        u_2m = Windmean * 4.87 / math.log(67.8*metinfo[2] - 5.42)   #2m ���� ǳ��

        T_Kv = 1.01 * (Tmean + 273)     #���µ�
        R = 0.287       #������ü��� (KJ Kg^-1K^-1)
        rou_a = P / (T_Kv * R)      #��մ��е�

        ETr_numerator = 0.408 * Ddelta * (Rn - G) + gamma*900/(Tmean+273)*u_2m*(es-ea)
        ETr_denumerator = Ddelta + gamma*(1+0.34*u_2m)
        ETr = ETr_numerator / ETr_denumerator       #FAO Penman-Monteith reference ET (mm/day)

        return ETr
    
    except IOError:
        print ("*** ���� �б� ����: ������ ���ų� ���뿡 ������ �ֽ��ϴ�.")
        sys.exit(1)
    except ValueError:
        print ("*** �ڷ� ���°� �������� �ʽ��ϴ�.")
        sys.exit(1)



        
##04 Defining a main function for printing out the daily ET0
def fileET_calculation(Metstation, Solar):

##    today = datetime.date.today()

    try:
        print("[ ����ڷ� �д� ��....... ]")
        inclimate = readinput_Climatefile(Metstation)
 
        filename = "PMET0_"+Metstation+ ".dat"
        fileout = open(filename, 'w')
        fileout.write ("\nDate(yyyymmdd)  P-M ET0(mm)")
        fileout.write ("\n=================================")

 

        dailyclimate = list()
        for n in range(0, len(inclimate)):
            if Solar == "1":
                pet = dailyReferenceET0_Sunhour(Metstation, inclimate[n][0], inclimate[n][1], inclimate[n][2], inclimate[n][3], inclimate[n][4], inclimate[n][5])
            else:
                pet = dailyReferenceET0_SolarRadiation(Metstation, inclimate[n][0], inclimate[n][1], inclimate[n][2], inclimate[n][3], inclimate[n][4], inclimate[n][5])
            climate  = [inclimate[n][0], inclimate[n][6], round(pet,2)]
            fileout.write ("\n%s       %5.1f" % (inclimate[n][0], pet))
            dailyclimate.append(climate)
        if len(dailyclimate) == 0:
            print (" ��󿹺��� �����ϴ�. ")
            sys.exit(1)
        else:
            print (".... %s���� %s���� %d�ϰ� ����Ͽ����ϴ�." % (dailyclimate[0][0], dailyclimate[len(dailyclimate)-1][0], len(dailyclimate)))

        fileout.close()

        print ("������ ���������� �Ϸ��Ͽ����ϴ�.")
        time.sleep(-1)

    except IOError:
        print ("���� ��� ����: ������ �����մϴ�.")
        sys.exit(0)
           

## main
def main():
    Metstation = str(input("��� ��������� �ڵ�(###)�� �Է��ϼ���.:  "))
    Solar = str(input("�Է��ڷᰡ �����ð��̸� 1, �������̸� 2�� �Է��ϼ���.:  "))

    if Solar == "1" or Solar == "2":
        print ("%s�� �����ϼ̽��ϴ�." % Solar)
    else:
        print ("�߸� �����ϼ̽��ϴ�. 1�� 2 �߿� �ϳ��� �Է��ϼ���!")
        sys.exit(0)
    
    fileET_calculation(Metstation, Solar)
        

## ����
main()

