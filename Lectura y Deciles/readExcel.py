import pandas as pd
import os


def cargar_lista(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as file:
            nombres = file.read().splitlines()
        return nombres
    except FileNotFoundError:
        return []
    

def guardar_lista(ruta_archivo, nombres):
    with open(ruta_archivo, 'w') as file:
        for nombre in nombres:
            file.write(f"{nombre}\n")


def seleccionar_o_crear_sector(ruta_base):
    sectores = [d for d in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, d))]
    print("Sectores disponibles:", sectores)
    sector = input("Ingresa el nombre del sector o crea uno nuevo: ")
    ruta_sector = os.path.join(ruta_base, sector)
    
    if not os.path.exists(ruta_sector):
        os.makedirs(ruta_sector)
        open(os.path.join(ruta_sector, 'whitelist.txt'), 'w').close()
        open(os.path.join(ruta_sector, 'blacklist.txt'), 'w').close()
    
    return ruta_sector

# Configuración inicial
ruta_base = 'C:/Users/Angel/Documents/Python Trabajo/Proceso Deciles/Lista de Comercios'
ruta_sector = seleccionar_o_crear_sector(ruta_base)
ruta_lista_blanca = os.path.join(ruta_sector, 'whitelist.txt')
ruta_lista_negra = os.path.join(ruta_sector, 'blacklist.txt')

# Cargar listas del sector elegido
whitelist = cargar_lista(ruta_lista_blanca)
blacklist = cargar_lista(ruta_lista_negra)

# Ruta a los archivos Excel
path = 'C:/Users/Angel/Documents/Python Trabajo/Proceso Deciles/8750 Comercios'
files = [f for f in os.listdir(path) if f.endswith('.xlsx')]

# Proceso para revisar y actualizar listas
nuevos_comercios = set()
for file in files:
    file_path = os.path.join(path, file)
    df = pd.read_excel(file_path, sheet_name='Hoja1', header=10)
    nuevos_comercios.update(df['Comercio'].unique())

comercios_no_listados = [c for c in nuevos_comercios if c not in whitelist and c not in blacklist]

for comercio in comercios_no_listados:
    respuesta = input(f"¿A qué lista deseas agregar el comercio {comercio}? (W para whitelist, B para blacklist, ninguna tecla para ignorar): ")
    if respuesta.lower() == 'w':
        whitelist.append(comercio)
    elif respuesta.lower() == 'b':
        blacklist.append(comercio)

guardar_lista(ruta_lista_blanca, whitelist)
guardar_lista(ruta_lista_negra, blacklist)

# Procesar los archivos con las listas actualizadas
dfs = []
for file in files:
    file_path = os.path.join(path, file)
    df = pd.read_excel(file_path, sheet_name='Hoja1', header=10)
    df = df[df['Comercio'].isin(whitelist) & ~df['Comercio'].isin(blacklist)]
    dfs.append(df)

final_df = pd.concat(dfs, ignore_index=True)

def divide_deciles_por_filas(df, column, num_divisions, label_prefix='D'):
    # Ordena el DataFrame por la columna especificada
    df_sorted = df.sort_values(column, ascending=True)
    
    # Calcula el número de filas por decil
    num_rows = len(df_sorted)
    rows_per_decil = num_rows // num_divisions
    
    # Genera las etiquetas para los deciles
    labels = np.repeat([f'{label_prefix}{i+1:02d}' for i in range(num_divisions)], rows_per_decil)
    
    # Maneja el caso donde el número total de filas no sea un múltiplo exacto de num_divisions
    remainder = num_rows % num_divisions
    if remainder > 0:
        labels = np.append(labels, np.repeat(f'{label_prefix}{num_divisions:02d}', remainder))
    
    # Asigna las etiquetas
    df_sorted[f'{label_prefix}_Decil'] = labels
    
    return df_sorted

final_df = divide_deciles(final_df, 'Monto', 10)

# Muestra el resultado
final_df


##################
import pandas as pd
import numpy as np
import math

def divide_deciles_por_filas(df, column, num_divisions, label_prefix='D'):
    df_sorted = df.sort_values(column, ascending=True)
    num_rows = len(df_sorted)
    rows_per_decil = math.ceil(num_rows / num_divisions)
    labels = np.repeat([f'{label_prefix}{i+1:02d}' for i in range(num_divisions)], rows_per_decil)
    labels = labels[:num_rows]  # Ajustar el tamaño del array de labels
    df_sorted[f'{label_prefix}_Decil'] = labels
    return df_sorted

# Divide el DataFrame completo en deciles
final_df = divide_deciles_por_filas(final_df, 'Monto', 10)

# Encuentra las filas que pertenecen al décimo decil
decil_diez = final_df[final_df['D_Decil'] == 'D10']

# Divide este décimo decil en 10 sub-deciles adicionales
decil_diez_dividido = divide_deciles_por_filas(decil_diez, 'Monto', 10, 'D10')

# Actualiza las etiquetas en el DataFrame original para el décimo decil
for i in range(1, 11):
    # Identifica las filas que pertenecen a cada sub-decil dentro del décimo decil
    sub_decil_rows = decil_diez_dividido[decil_diez_dividido['D10_Decil'] == f'D10{i:02d}']
    # Actualiza la columna 'D_Decil' en el DataFrame original con las nuevas etiquetas
    final_df.loc[sub_decil_rows.index, 'D_Decil'] = f'D10-D{i}'

# Muestra el DataFrame actualizado
print(final_df)