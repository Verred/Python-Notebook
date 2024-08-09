#Importaciones necesarias para leer documentos
import os
import pandas as pd
#Importaciones necesarias para leer access
import pyodbc



## Si necesitas leer un documennto en especifico como excel o csv pues usar 
def ReadExcel():
    data = pd.read_csv("data.csv")
    print(data)
    return data

## Si quieres leer una carpeta con excels 

def ReadFolderwithExcel(path):
    dataframes = []
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_excel(file_path)
            dataframes.append(df)


## Si quieree leer una tabla de access 
def ReadAccess():
    conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\path\to\access\file.accdb;')
    cursor = conn.cursor()
    cursor.execute('select * from table')
    for row in cursor.fetchall():
        print(row)
    conn.close()

## Si quieres separar los primeros caracters que sean digitos 

def split_digits(s):
    head = s.rstrip('0123456789')
    tail = s[len(head):]
    return head, tail

#si quieres separar por guion y separar en 2 string y eliminar espacios en balnco al inicio y al final

def split_hyphen(s):
    head, tail = s.split('-', 1)
    return head.strip(), tail.strip()



