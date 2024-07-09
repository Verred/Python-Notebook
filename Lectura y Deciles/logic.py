import pandas as pd
from Levenshtein import ratio  # Puede que necesites instalar la biblioteca python-Levenshtein

# Simulación de DataFrames
data1 = {'ID': [1, 2, 3, 4], 'COD VALIDACION': ['A12', 'B34', 'C56', 'D78'], 'MONTO': [100, 200, 300, 400], 'COMERCIO': ['Supermercado', 'Tiendita', 'Mercado', 'Bodega'], 'FECHA': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04']}
data2 = {'ID': [1, 2, 3, 4], 'COD VALIDACION': ['A12', 'X34', 'Y56', 'Z78'], 'MONTO': [100, 200, 300, 400], 'COMERCIO': ['Supermercado', 'Tienda', 'Mercadillo', 'Bodeguita'], 'FECHA': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04']}
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

def comercio_similar(name1, name2, threshold=0.8):
    return ratio(name1.lower(), name2.lower()) >= threshold

# Corrección de códigos de validación
for index, row in df1.iterrows():
    # Buscar en df2 donde el monto y el comercio son similares
    similar_rows = df2[(df2['MONTO'] == row['MONTO']) & (df2['COMERCIO'].apply(lambda x: comercio_similar(x, row['COMERCIO'])))]
    for _, correct_row in similar_rows.iterrows():
        # Verificar unicidad del nuevo par ID y código de validación
        if not ((df1['ID'] == row['ID']) & (df1['COD VALIDACION'] == correct_row['COD VALIDACION'])).any():
            # Actualizar el código de validación
            df1.at[index, 'COD VALIDACION'] = correct_row['COD VALIDACION']
            break  # Romper el bucle una vez hecho el cambio

print(df1)


#############
# Diccionario para rastrear los códigos de validación ya usados por cada ID
used_codes = {id: set() for id in df1['ID'].unique()}

# Corrección de códigos de validación
for index, row in df1.iterrows():
    # Intentar encontrar una fila en df2 con el mismo monto y un comercio similar
    similar_rows = df2[(df2['MONTO'] == row['MONTO']) & (df2['COMERCIO'].apply(lambda x: comercio_similar(x, row['COMERCIO'])))]
    for _, correct_row in similar_rows.iterrows():
        # Verificar unicidad del nuevo par ID y código de validación
        if correct_row['COD VALIDACION'] not in used_codes[row['ID']]:
            # Actualizar el código de validación si es diferente y no usado previamente
            df1.at[index, 'COD VALIDACION'] = correct_row['COD VALIDACION']
            # Registrar el código usado
            used_codes[row['ID']].add(correct_row['COD VALIDACION'])
            break  # Romper el bucle una vez hecho el cambio


##############
import pandas as pd
from Levenshtein import ratio

# Crear los DataFrames con tus datos
data_errada = {
    'ID': [2, 2, 2, 3, 3, 4, 4],
    'COD VALIDACION': [23, 24, 54, 35, 45, 63, 60],
    'MONTO': [12, 12, 13, 54, 43, 78, 32],
    'COMERCIO': ['Luna', 'Lunaas', 'Luna', 'app', 'app', 'cas', 'cas'],
    'FECHA': ['12/03/2024', '12/03/2024', '15/03/2024', '16/03/2024', '16/03/2024', '16/03/2024', '16/03/2024']
}

data_valida = {
    'ID': [2, 2, 2, 3, 3, 4, 4],
    'COD VALIDACION': [53, 56, 54, 35, 45, 63, 60],
    'MONTO': [12, 12, 13, 54, 43, 78, 32],
    'COMERCIO': ['Luna', 'Lunaas', 'Luna', 'app', 'app', 'cas', 'cas'],
    'FECHA': ['12/03/2024', '12/03/2024', '15/03/2024', '16/03/2024', '16/03/2024', '16/03/2024', '16/03/2024']
}

df1 = pd.DataFrame(data_errada)
df2 = pd.DataFrame(data_valida)

def comercio_similar(name1, name2, threshold=0.8):
    return ratio(name1.lower(), name2.lower()) >= threshold

used_codes = {id: set(df1[df1['ID'] == id]['COD VALIDACION'].tolist()) for id in df1['ID'].unique()}

def correct_cod_validation(row):
    similar_rows = df2[(df2['MONTO'] == row['MONTO']) & (df2['COMERCIO'].apply(lambda x: comercio_similar(x, row['COMERCIO'])))]
    for _, correct_row in similar_rows.iterrows():
        if correct_row['COD VALIDACION'] not in used_codes[row['ID']]:
            used_codes[row['ID']].add(correct_row['COD VALIDACION'])
            return correct_row['COD VALIDACION']
    return row['COD VALIDACION']

df1['COD VALIDACION'] = df1.apply(correct_cod_validation, axis=1)

print(df1)
################
import pandas as pd
from Levenshtein import ratio

# Crear los DataFrames con tus datos
data_errada = {
    'ID': [2, 2, 2, 3, 3, 4, 4],
    'COD VALIDACION': [23, 24, 54, 35, 45, 63, 60],
    'MONTO': [12, 12, 13, 54, 43, 78, 32],
    'COMERCIO': ['Luna', 'Lunaas', 'Luna', 'app', 'app', 'cas', 'cas'],
    'FECHA': ['12/03/2024', '12/03/2024', '15/03/2024', '16/03/2024', '16/03/2024', '16/03/2024', '16/03/2024']
}

data_valida = {
    'ID': [2, 2, 2, 3, 3, 4, 4],
    'COD VALIDACION': [53, 56, 54, 35, 45, 63, 60],
    'MONTO': [12, 12, 13, 54, 43, 78, 32],
    'COMERCIO': ['Luna', 'Lunaas', 'Luna', 'app', 'app', 'cas', 'cas'],
    'FECHA': ['12/03/2024', '12/03/2024', '15/03/2024', '16/03/2024', '16/03/2024', '16/03/2024', '16/03/2024']
}

df1 = pd.DataFrame(data_errada)
df2 = pd.DataFrame(data_valida)

def comercio_similar(name1, name2, threshold=0.8):
    return ratio(name1.lower(), name2.lower()) >= threshold

# Corrección de códigos de validación
for index, row in df1.iterrows():
    # Intentar encontrar una fila en df2 con el mismo monto y un comercio similar
    similar_rows = df2[(df2['MONTO'] == row['MONTO']) & (df2['COMERCIO'].apply(lambda x: comercio_similar(x, row['COMERCIO'])))]
    for _, correct_row in similar_rows.iterrows():
        # Verificar unicidad del nuevo par ID y código de validación
        if not ((df1['ID'] == row['ID']) & (df1['COD VALIDACION'] == correct_row['COD VALIDACION'])).any():
            # Actualizar el código de validación si es diferente
            if df1.at[index, 'COD VALIDACION'] != correct_row['COD VALIDACION']:
                df1.at[index, 'COD VALIDACION'] = correct_row['COD VALIDACION']
            break  # Romper el bucle una vez hecho el cambio
    # Si no se encuentra ninguna fila adecuada en df2, se conserva el código original (no se hace cambio)

print(df1)
