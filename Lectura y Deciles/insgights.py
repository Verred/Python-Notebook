import pandas as pd
import numpy as np

# Suponiendo que df es tu DataFrame original con las columnas 'idcliente', 'fecha' y 'monto'
df['fecha'] = pd.to_datetime(df['fecha'])

# Agrupa por 'idcliente' y 'fecha', y cuenta las transacciones por grupo
frecuencia_trx = df.groupby(['idcliente', 'fecha']).size().reset_index(name='num_trx')

# Calcula los valores máximo y mínimo de transacciones
max_trx = frecuencia_trx['num_trx'].max()
min_trx = frecuencia_trx['num_trx'].min()

# Define el número de intervalos que deseas, por ejemplo, 5
num_intervals = 5

# Crea los intervalos desde el mínimo al máximo
if max_trx == min_trx:  # Evita la creación de intervalos inválidos si todos los valores son iguales
    bins = [min_trx - 1, max_trx]
else:
    bins = np.linspace(min_trx, max_trx, num_intervals + 1)

# Ajusta los bins para asegurar que el último bin incluya el máximo valor
bins[-1] = bins[-1] + 1

# Etiquetas para los intervalos
labels = [f'{int(bins[i])}-{int(bins[i+1])-1}' for i in range(len(bins)-1)]

# Clasifica las transacciones en los intervalos definidos
frecuencia_trx['intervalo'] = pd.cut(frecuencia_trx['num_trx'], bins=bins, labels=labels, right=False)

# Cuenta cuántas transacciones caen en cada intervalo
intervalo_frecuencia = frecuencia_trx['intervalo'].value_counts().reset_index(name='cantidad')
intervalo_frecuencia.columns = ['intervalo', 'cantidad']

# Calcula el porcentaje de cada intervalo respecto al total de transacciones
intervalo_frecuencia['porcentaje'] = (intervalo_frecuencia['cantidad'] / intervalo_frecuencia['cantidad'].sum()) * 100

# Ordena los resultados por el intervalo
intervalo_frecuencia = intervalo_frecuencia.sort_values('index')

print(intervalo_frecuencia)



############

import pandas as pd

# Supongamos que tienes el siguiente DataFrame
data = {'hora': ['12:00', '13:30', '14:00', '12:30', '13:00', '14:00', '13:30']}
df = pd.DataFrame(data)

# Convertir la columna 'hora' a datetime
df['hora'] = pd.to_datetime(df['hora'], format='%H:%M').dt.time

# Calcular el valor decimal de la hora para facilitar la creación de intervalos
df['hora_decimal'] = df['hora'].apply(lambda x: x.hour + x.minute / 60)

# Crear una columna de intervalos dividiendo el día en 8 partes de 3 horas cada una
intervalos = pd.interval_range(start=0, end=24, periods=8, closed='left')
df['intervalo'] = pd.cut(df['hora_decimal'], bins=intervalos)

# Contar las frecuencias
frecuencias = df['intervalo'].value_counts().sort_index()

# Calcular porcentajes
porcentajes = (frecuencias / frecuencias.sum()) * 100

# Crear un DataFrame con los resultados
resultado = pd.DataFrame({
    'Intervalo': frecuencias.index,
    'Frecuencia': frecuencias.values,
    'Porcentaje': porcentajes.values
})

print(resultado)


#############

import pandas as pd
import numpy as np

# Supongamos que df es tu dataframe con las ventas
# df = pd.read_csv('tu_archivo.csv')  # Suponiendo que tienes los datos en un CSV

# Paso 1: Encontrar los 3 comercios con mayor monto vendido
top_comercios = df.groupby('comercio')['monto'].sum().nlargest(3)

# Paso 2: Filtrar el dataframe para incluir solo esos comercios
df_top = df[df['comercio'].isin(top_comercios.index)]

# Paso 3: Definir intervalos de monto de transacción
bins = pd.interval_range(start=0, end=5000, freq=500)  # Cambia los valores según sea necesario
df_top['monto_intervalo'] = pd.cut(df_top['monto'], bins=bins)

# Paso 4: Agrupar por comercio e intervalo y calcular métricas del 'score'
resultados = df_top.groupby(['comercio', 'monto_intervalo'])['score'].agg(['mean', 'median', lambda x: x.mode()[0]])

# Mostrar resultados
print(resultados)

import pandas as pd
import numpy as np

# Asumiendo que df es tu dataframe
# df = pd.read_csv('tu_archivo.csv')

# Paso 1: Encontrar los 3 comercios con mayor monto vendido
top_comercios = df.groupby('comercio')['monto'].sum().nlargest(3)

# Paso 2: Filtrar el dataframe para incluir solo esos comercios
df_top = df[df['comercio'].isin(top_comercios.index)]

# Paso 3: Crear intervalos dinámicos basados en cuantiles
num_bins = 5  # Puedes ajustar el número de bins según lo necesario
quantile_bins = pd.qcut(df_top['monto'], q=num_bins, precision=0)

df_top['monto_intervalo'] = pd.qcut(df_top['monto'], q=num_bins, precision=0)

# Paso 4: Agrupar por comercio e intervalo y calcular métricas del 'score'
resultados = df_top.groupby(['comercio', 'monto_intervalo'])['score'].agg(['mean', 'median', lambda x: x.mode()[0] if not x.empty else np.nan])

# Mostrar resultados
print(resultados)


########-------------------

import pandas as pd
import numpy as np

# Suponiendo que df es tu DataFrame original con las columnas 'idcliente', 'fecha' y 'monto'
df['fecha'] = pd.to_datetime(df['fecha'])

# Agrupa por 'idcliente' y 'fecha', y cuenta las transacciones por grupo
frecuencia_trx = df.groupby(['idcliente', 'fecha']).size().reset_index(name='num_trx')

# Calcula los valores máximo y mínimo de transacciones
max_trx = frecuencia_trx['num_trx'].max()
min_trx = frecuencia_trx['num_trx'].min()

# Define el número de intervalos que deseas, por ejemplo, 5
num_intervals = 5

# Crea los intervalos desde el mínimo al máximo
if max_trx == min_trx:  # Evita la creación de intervalos inválidos si todos los valores son iguales
    bins = [min_trx - 1, max_trx + 1]
else:
    bins = np.linspace(min_trx, max_trx, num_intervals + 1)

# Ajusta los bins para asegurar que el último bin incluya el máximo valor
bins[-1] = bins[-1] + 1

# Etiquetas para los intervalos
labels = [f'[{int(bins[i])}-{int(bins[i+1])-1}]' for i in range(len(bins)-1)]

# Clasifica las transacciones en los intervalos definidos
frecuencia_trx['intervalo'] = pd.cut(frecuencia_trx['num_trx'], bins=bins, labels=labels, right=True)

# Cuenta cuántas transacciones caen en cada intervalo
intervalo_frecuencia = frecuencia_trx['intervalo'].value_counts().reset_index(name='cantidad')
intervalo_frecuencia.columns = ['intervalo', 'cantidad']

# Calcula el porcentaje de cada intervalo respecto al total de transacciones
intervalo_frecuencia['porcentaje'] = (intervalo_frecuencia['cantidad'] / intervalo_frecuencia['cantidad'].sum()) * 100

# Ordena los resultados por el intervalo
intervalo_frecuencia = intervalo_frecuencia.sort_values('index')

print(intervalo_frecuencia)
