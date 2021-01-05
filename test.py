import pandas as pd

selection_list = ["최고기온", "최저기온", "상대습도", "평균풍속", "일조시간", "일조량"]

def rearrange_csv():
    df = pd.read_csv("MET090.csv", encoding = 'cp949')

    SOLAR = 1

    for col in df.columns:
        parsed_col = col.replace(" ", "")
        df.rename(columns={col:parsed_col}, inplace=True)
    
    for col in df.columns:
        for i in selection_list:
            if col.find(i) != -1: df.rename(columns={col:i}, inplace=True)
    
    date = df.columns[0]

    if SOLAR == 1: df = df[[date, "최고기온", "최저기온", "상대습도", "평균풍속", "일조시간"]]
    elif SOLAR == 2: df = df[[date, "최고기온", "최저기온", "상대습도", "평균풍속", "일조량"]]
    
    df.to_csv("MET090.csv", header=True, index=False)
    
    return df

df = rearrange_csv()

print(df)


'''
filein = open("MET090.csv",'w')

for i in range(len(df)):
    filein.write('\n')

    for j in range(len(df.columns)):
        filein.write(str(df.iloc[i, j]) + ',')

filein.close()
'''
