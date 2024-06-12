import pandas as pd

# Suponiendo que 'data' es tu conjunto de datos original, y 'df' se ha creado correctamente.
df = pd.DataFrame(data)
df['fecha'] = pd.to_datetime(df['fecha'])
df['hora'] = df['fecha'].dt.hour  # Extrae la hora del campo 'fecha' si es necesario

# Clasificación de transacciones como Genuinas o indicador de Fraude 'F'
df['Clasificacion'] = df['indicadorFraude'].apply(lambda x: 'Fraude' if x == 'F' else 'Genuina')

# Contar transacciones por hora y clasificación
conteo_transacciones = df.groupby(['hora', 'Clasificacion']).size().reset_index(name='num_trx')

# Pivotar los datos para tener 'Genuina' y 'Fraude' como columnas
resultado_final = conteo_transacciones.pivot(index='hora', columns='Clasificacion', values='num_trx').fillna(0)

# Asegurar que las columnas 'Genuina' y 'Fraude' estén presentes
resultado_final = resultado_final.reindex(columns=['Genuina', 'Fraude'], fill_value=0)

# Calcular el total de transacciones por hora
resultado_final['TRX'] = resultado_final['Genuina'] + resultado_final['Fraude']

# Reordenar las columnas si es necesario y resetear el índice para hacer 'hora' una columna
resultado_final = resultado_final.reset_index()
resultado_final = resultado_final[['hora', 'TRX', 'Genuina', 'Fraude']]

print(resultado_final)


#######%%%%%%%%%%%%%%

import pandas as pd

# Suponiendo que 'data' es tu conjunto de datos original, y 'df' se ha creado correctamente.
df = pd.DataFrame(data)
df['fecha'] = pd.to_datetime(df['fecha'])
df['hora'] = df['fecha'].dt.hour  # Extrae la hora del campo 'fecha'

# Clasificación de transacciones como Genuinas o indicador de Fraude 'F'
df['Clasificacion'] = df['indicadorFraude'].apply(lambda x: 'Fraude' if x == 'F' else 'Genuina')

# Definir los intervalos de horas
bins = [-1, 2, 5, 8, 11, 14, 17, 20, 23, float('inf')]  # ajusta estos valores según tus necesidades
labels = ['0-2', '3-5', '6-8', '9-11', '12-14', '15-17', '18-20', '21-23', '24+']

# Clasificar las horas en los intervalos definidos
df['intervalo_hora'] = pd.cut(df['hora'], bins=bins, labels=labels)

# Contar transacciones por intervalo de hora y clasificación
conteo_transacciones = df.groupby(['intervalo_hora', 'Clasificacion']).size().reset_index(name='num_trx')

# Pivotar los datos para tener 'Genuina' y 'Fraude' como columnas
resultado_final = conteo_transacciones.pivot(index='intervalo_hora', columns='Clasificacion', values='num_trx').fillna(0)

# Asegurarse de que ambas columnas 'Genuina' y 'Fraude' estén presentes
resultado_final = resultado_final.reindex(columns=['Genuina', 'Fraude'], fill_value=0)

# Calcular el total de transacciones por intervalo de hora
resultado_final['TRX'] = resultado_final['Genuina'] + resultado_final['Fraude']

# Restablecer el índice para hacer 'intervalo_hora' una columna y reordenar si es necesario
resultado_final = resultado_final.reset_index()
resultado_final = resultado_final[['intervalo_hora', 'TRX', 'Genuina', 'Fraude']]

print(resultado_final)
