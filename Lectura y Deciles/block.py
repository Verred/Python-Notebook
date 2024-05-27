import pandas as pd

# Supongamos que este es tu DataFrame original
data = {
    'Decil': ['D1', 'D2', 'D3', 'D1', 'D2', 'D3', 'D1', 'D2', 'D3', 'D4'],
    'monto': [100, 150, 200, 110, 160, 210, 120, 170, 220, 230],
    'aprobada': ['SI', 'NO', 'SI', 'SI', 'ESPERA', 'SI', 'NO', 'SI', 'NO', 'SI']
}
df = pd.DataFrame(data)

# Añadir la columna "Five" con valores predeterminados para simular la condición
df['Five'] = ['F', 'F', 'X', 'X', 'X', 'F', 'X', 'X', 'F', 'X']  # Esta columna la añadimos manualmente como ejemplo

# Asegurarse de que los valores de la columna "Decil" sean consistentes
df['Decil'] = df['Decil'].str.upper()

# Crear un DataFrame resumen que contenga las estadísticas generales por decil
summary_df = df.groupby('Decil').agg(
    Monto_Min=('monto', 'min'),
    Monto_Max=('monto', 'max'),
    Monto_Sum=('monto', 'sum'),
    Total_Trx=('Decil', 'size'),
    Aprobadas_SI=('aprobada', lambda x: (x == 'SI').sum())
).reset_index()

# Calcular el monto total por decil de las transacciones denegadas y que tienen 'F' en la columna "Five"
filtro_denegados_f = df[(df['aprobada'] == 'NO') & (df['Five'] == 'F')]
monto_total_denegado_f = filtro_denegados_f.groupby('Decil')['monto'].sum().reset_index(name='Monto_Denegado_F')

# Unir con el DataFrame de montos denegados con "F"
summary_df = pd.merge(summary_df, monto_total_denegado_f, on='Decil', how='left')

# Llenar NaN con 0 si no hay transacciones que cumplan la condición en algún decil
summary_df['Monto_Denegado_F'] = summary_df['Monto_Denegado_F'].fillna(0)

# Calcular el porcentaje de transacciones aprobadas respecto al total de transacciones por decil
summary_df['Porcentaje_Aprobadas'] = ((summary_df['Aprobadas_SI'] / summary_df['Total_Trx']) * 100).round(2).astype(str) + '%'

# Mostrar el DataFrame final
print(summary_df)



import pandas as pd

# Supongamos que este es tu DataFrame original
data = {
    'Decil': ['D1', 'D2', 'D3', 'D1', 'D2', 'D3', 'D1', 'D2', 'D3', 'D4'],
    'monto': [100, 150, 200, 110, 160, 210, 120, 170, 220, 230],
    'aprobada': ['SI', 'NO', 'SI', 'SI', 'ESPERA', 'SI', 'NO', 'SI', 'NO', 'SI']
}
df = pd.DataFrame(data)

# Añadir la columna "Five" con valores predeterminados para simular la condición
df['Five'] = ['F', 'F', 'X', 'X', 'X', 'F', 'X', 'X', 'F', 'X']  # Esta columna la añadimos manualmente como ejemplo

# Asegurarse de que los valores de la columna "Decil" sean consistentes
df['Decil'] = df['Decil'].str.upper()

# Crear un DataFrame resumen que contenga las estadísticas generales por decil
summary_df = df.groupby('Decil').agg(
    Monto_Min=('monto', 'min'),
    Monto_Max=('monto', 'max'),
    Monto_Sum=('monto', 'sum'),
    Total_Trx=('Decil', 'size'),
    Aprobadas_SI=('aprobada', lambda x: (x == 'SI').sum()),
    Monto_Aprobado=('monto', lambda x: df.loc[x.index, 'monto'][df['aprobada'] == 'SI'].sum())  # Suma de montos aprobados
).reset_index()

# Calcular el total de transacciones aprobadas
total_trx_aprobadas = summary_df['Aprobadas_SI'].sum()

# Calcular la frecuencia de transacciones aprobadas por decil respecto al total de transacciones aprobadas
summary_df['Frecuencia_Trx_Aprobadas'] = ((summary_df['Aprobadas_SI'] / total_trx_aprobadas) * 100).round().astype(int)

# Calcular la frecuencia acumulada de transacciones aprobadas
summary_df['Frecuencia_Acumulada_Trx'] = summary_df['Frecuencia_Trx_Aprobadas'].cumsum()

# Mostrar el DataFrame final
print(summary_df)


###########################
import pandas as pd

# Supongamos que este es tu DataFrame original
data = {
    'Decil': ['D1', 'D2', 'D3', 'D1', 'D2', 'D3', 'D1', 'D2', 'D3', 'D4'],
    'monto': [100, 150, 200, 110, 160, 210, 120, 170, 220, 230],
    'aprobada': ['SI', 'NO', 'SI', 'SI', 'ESPERA', 'SI', 'NO', 'SI', 'NO', 'SI'],
    'Five': ['F', 'F', 'X', 'X', 'X', 'F', 'X', 'X', 'F', 'X']  # Columna Five ya incluida
}
df = pd.DataFrame(data)

# Asegurarse de que los valores de la columna "Decil" sean consistentes
df['Decil'] = df['Decil'].str.upper()

# Filtrar las transacciones que fueron denegadas y tienen "F" en la columna "Five"
denied_f_df = df[(df['aprobada'] == 'NO') & (df['Five'] == 'F')]

# Calcular el monto total y la cantidad de transacciones que fueron denegadas con "F"
monto_denegado_f = denied_f_df.groupby('Decil')['monto'].sum().reset_index(name='Monto_Denegado_F')
cantidad_denegado_f = denied_f_df.groupby('Decil').size().reset_index(name='Cantidad_Denegado_F')

# Crear un DataFrame resumen que contenga las estadísticas generales por decil
summary_df = df.groupby('Decil').agg(
    Monto_Min=('monto', 'min'),
    Monto_Max=('monto', 'max'),
    Monto_Sum=('monto', 'sum'),
    Total_Trx=('Decil', 'size'),
    Aprobadas_SI=('aprobada', lambda x: (x == 'SI').sum()),
    Monto_Aprobado=('monto', lambda x: df.loc[x.index, 'monto'][df['aprobada'] == 'SI'].sum())  # Suma de montos aprobados
).reset_index()

# Unir con los montos y cantidades de las transacciones denegadas con "F"
summary_df = pd.merge(summary_df, monto_denegado_f, on='Decil', how='left')
summary_df = pd.merge(summary_df, cantidad_denegado_f, on='Decil', how='left')

# Llenar NaN con 0 en caso de que no haya transacciones que cumplan la condición en algún decil
summary_df['Monto_Denegado_F'] = summary_df['Monto_Denegado_F'].fillna(0)
summary_df['Cantidad_Denegado_F'] = summary_df['Cantidad_Denegado_F'].fillna(0)

# Mostrar el DataFrame final
print(summary_df)