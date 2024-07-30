import pandas as pd

# Ejemplo de DataFrame
data = {
    'RatioVenta': [10, 25, 30, 15, 50, 5, 20, 95],
    'RatioClientes': [400, 600, 300, 700, 800, 200, 500, 50],
    'RatioOtros': [5, 7, 3, 9, 10, 2, 8, 100]
}
df = pd.DataFrame(data)

def dividir_dataframe(df, criterios):
    # DataFrames iniciales vacíos para aprobados y desaprobados
    aprobados = pd.DataFrame()
    desaprobados = pd.DataFrame()
    
    # Filtrar los aprobados y desaprobados según los criterios
    for columna, (aprobado_min, aprobado_max, desaprobado_min, desaprobado_max) in criterios.items():
        aprobados = aprobados.append(df[(df[columna] >= aprobado_min) & (df[columna] <= aprobado_max)])
        desaprobados = desaprobados.append(df[(df[columna] >= desaprobado_min) & (df[columna] <= desaprobado_max)])
    
    # Eliminar duplicados en caso de que algunas filas hayan sido añadidas a ambos DataFrames
    aprobados = aprobados.drop_duplicates()
    desaprobados = desaprobados.drop_duplicates()
    
    # Eliminar los aprobados del DataFrame de desaprobados
    desaprobados = desaprobados[~desaprobados.index.isin(aprobados.index)]
    
    return aprobados, desaprobados

# Diccionario de criterios
# Formato: 'NombreColumna': (aprobado_min, aprobado_max, desaprobado_min, desaprobado_max)
criterios = {
    'RatioVenta': (20, 100, 0, 19),    # Aprobado entre 20 y 100, Desaprobado entre 0 y 19
    'RatioClientes': (500, 1000, 0, 499), # Aprobado entre 500 y 1000, Desap


###############
import pandas as pd
import numpy as np

# Crear dataframes de ejemplo
df_incidencias = pd.DataFrame({
    'idincidencia': [1, 2],
    'fecha_inicio': [np.nan, '2024-07-02'],
    'hora_inicio': [np.nan, '14:00:00'],
    'fecha_registro': ['2024-07-01', '2024-07-02'],
    'hora_registro': ['08:00:00', '14:00:00'],
    'fecha_solucion': ['2024-07-01', '2024-07-02'],
    'hora_solucion': ['12:00:00', '16:00:00']
})

df_trx = pd.DataFrame({
    'fecha_trx': ['2024-07-01', '2024-07-02', '2024-07-01'],
    'hora_trx': ['10:00:00', '15:00:00', '13:00:00']
})

# Asegurarse de que las columnas de fecha y hora sean de tipo str
df_incidencias['fecha_inicio'] = df_incidencias['fecha_inicio'].astype(str)
df_incidencias['hora_inicio'] = df_incidencias['hora_inicio'].astype(str)
df_incidencias['fecha_registro'] = df_incidencias['fecha_registro'].astype(str)
df_incidencias['hora_registro'] = df_incidencias['hora_registro'].astype(str)
df_incidencias['fecha_solucion'] = df_incidencias['fecha_solucion'].astype(str)
df_incidencias['hora_solucion'] = df_incidencias['hora_solucion'].astype(str)
df_trx['fecha_trx'] = df_trx['fecha_trx'].astype(str)
df_trx['hora_trx'] = df_trx['hora_trx'].astype(str)

# Convertir fechas y horas a datetime, manejando NaT
df_incidencias['fecha_inicio'] = pd.to_datetime(df_incidencias['fecha_inicio'] + ' ' + df_incidencias['hora_inicio'], errors='coerce')
df_incidencias['fecha_registro'] = pd.to_datetime(df_incidencias['fecha_registro'] + ' ' + df_incidencias['hora_registro'], errors='coerce')
df_incidencias['fecha_solucion'] = pd.to_datetime(df_incidencias['fecha_solucion'] + ' ' + df_incidencias['hora_solucion'], errors='coerce')
df_trx['fecha_trx'] = pd.to_datetime(df_trx['fecha_trx'] + ' ' + df_trx['hora_trx'], errors='coerce')

# Reemplazar fechas de inicio vacías por fechas de registro
df_incidencias['fecha_inicio'].fillna(df_incidencias['fecha_registro'], inplace=True)

# Crear una columna para almacenar los IDs de las incidencias
df_trx['idincidencia'] = [[] for _ in range(len(df_trx))]

# Encontrar incidencias para cada trx
for i, trx_row in df_trx.iterrows():
    trx_time = trx_row['fecha_trx']
    for j, inc_row in df_incidencias.iterrows():
        if inc_row['fecha_inicio'] <= trx_time <= inc_row['fecha_solucion']:
            df_trx.at[i, 'idincidencia'].append(inc_row['idincidencia'])

# Convertir listas vacías a NaN
df_trx['idincidencia'] = df_trx['idincidencia'].apply(lambda x: x if x else None)

# Mostrar resultados
print(df_trx)
