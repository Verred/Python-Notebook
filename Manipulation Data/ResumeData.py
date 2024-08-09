import pandas as pd 

def ReadCSV(path):
    data = pd.read_csv(path)
    print(data)
    return data

def main():
    df_accidentes = ReadCSV(r"C:\Users\Angel\Downloads\OpenData.csv")