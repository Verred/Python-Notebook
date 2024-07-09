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
