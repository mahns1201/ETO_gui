import pandas as pd

df = pd.read_csv("MET090.csv", 'r', encoding="UTF8")

print(df)

header = list(df)
header = header[0].split(',')

print(header)