import pandas as pd
import numpy as np

# Suponiendo que df es tu DataFrame con las columnas 'idcliente', 'fecha', 'monto', y 'cupon'
df['fecha'] = pd.to_datetime(df['fecha'])

# Agrupa por 'idcliente' y 'fecha', y cuenta las transacciones por grupo
frecuencia_trx = df.groupby(['idcliente', 'fecha']).size().reset_index(name='num_trx')

# Crear una columna que indica si se usó cupón en cada transacción
# Supongamos que la columna 'cupon' es booleana: True si se usó un cupón, False si no.
frecuencia_trx['uso_cupon'] = df.groupby(['idcliente', 'fecha'])['cupon'].any().map({True: 'Sí', False: 'No'}).reset_index(name='uso_cupon')['uso_cupon']

# Definir los intervalos fijos
bins = [0, 1, 2, 3, 4, 5, 6, 9, 20, float('inf')]  # Incluye un extremo superior para '20+'
labels = ['1', '2', '3', '4', '5', '6', '7-9', '10-20', '20+']

# Clasificar las transacciones en los intervalos definidos
frecuencia_trx['intervalo'] = pd.cut(frecuencia_trx['num_trx'], bins=bins, labels=labels, right=False)

# Contar cuántos clientes caen en cada intervalo, y cuántos usaron cupones
resultado = frecuencia_trx.pivot_table(index='intervalo', columns='uso_cupon', aggfunc='size', fill_value=0)

# Imprime el resultado
print(resultado)

###################
import pandas as pd

# Suponiendo que df es tu DataFrame con las columnas 'idcliente', 'fecha', 'monto', y 'cupon'
df['fecha'] = pd.to_datetime(df['fecha'])

# Función para clasificar las transacciones basada en la columna 'cupon'
def clasificar_cupon(valor):
    if 'F' in valor:
        return 'Genuina'
    else:
        return 'No Genuina'

# Aplicar la función para crear una nueva columna 'tipo_cupon'
df['tipo_cupon'] = df['cupon'].apply(clasificar_cupon)

# Agrupa por 'idcliente', 'fecha' y 'tipo_cupon', y cuenta las transacciones por grupo
frecuencia_trx = df.groupby(['idcliente', 'fecha', 'tipo_cupon']).size().reset_index(name='num_trx')

# Pivotar la tabla para tener las columnas de 'Genuina' y 'No Genuina'
pivot_frecuencia = frecuencia_trx.pivot_table(index=['idcliente', 'fecha'], columns='tipo_cupon', values='num_trx', aggfunc='sum', fill_value=0).reset_index()

# Agregar columna de transacciones totales por cliente y por día
pivot_frecuencia['total_trx'] = pivot_frecuencia['Genuina'] + pivot_frecuencia['No Genuina']

# Definir los intervalos fijos y las etiquetas
bins = [0, 1, 2, 3, 4, 5, 6, 9, 20, float('inf')]
labels = ['1', '2', '3', '4', '5', '6', '7-9', '10-20', '20+']

# Clasificar las transacciones totales en los intervalos definidos
pivot_frecuencia['intervalo'] = pd.cut(pivot_frecuencia['total_trx'], bins=bins, labels=labels, right=False)

# Agrupar por intervalo y sumarizar las transacciones 'Genuina', 'No Genuina', y 'total_trx'
resultado_intervalos = pivot_frecuencia.groupby('intervalo').agg({
    'Genuina': 'sum',
    'No Genuina': 'sum',
    'total_trx': 'sum'
}).reset_index()

print(resultado_intervalos)
##&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

import pandas as pd

# Suponiendo que df es tu DataFrame con las columnas 'idcliente', 'fecha', 'monto', y 'cupon'
df['fecha'] = pd.to_datetime(df['fecha'])

# Función para clasificar las transacciones basada en la columna 'cupon'
def clasificar_cupon(valor):
    if 'F' in valor:
        return 'Genuina'
    else:
        return 'No Genuina'

# Aplicar la función para crear una nueva columna 'tipo_cupon'
df['tipo_cupon'] = df['cupon'].apply(clasificar_cupon)

# Agrupar por 'idcliente', 'fecha', y contar las transacciones totales y por tipo de cupón
agrupado = df.groupby(['idcliente', 'fecha', 'tipo_cupon']).size().unstack(fill_value=0).reset_index()
agrupado['total_trx'] = agrupado.sum(axis=1)

# Definir los intervalos fijos y las etiquetas
bins = [0, 1, 2, 3, 4, 5, 6, 9, 20, float('inf')]
labels = ['1', '2', '3', '4', '5', '6', '7-9', '10-20', '20+']

# Clasificar las transacciones totales en los intervalos definidos
agrupado['intervalo'] = pd.cut(agrupado['total_trx'], bins=bins, labels=labels, right=False)

# Reagrupar para obtener la suma por intervalo y tipo de cupón
resultado_final = agrupado.groupby('intervalo').agg({
    'Genuina': 'sum',
    'No Genuina': 'sum',
    'total_trx': 'sum'
}).reset_index()

print(resultado_final)

##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

import pandas as pd

# Suponiendo que df es tu DataFrame con las columnas 'idcliente', 'fecha', 'indicadorFraude' y otras más.
df['fecha'] = pd.to_datetime(df['fecha'])

# Clasificación de transacciones como Genuinas o indicador de Fraude 'F'
df['Clasificacion'] = df['indicadorFraude'].apply(lambda x: 'Genuina' if x != 'F' else 'Fraude')

# Contar transacciones por cliente y por fecha
conteo_transacciones = df.groupby(['idcliente', 'fecha']).size().reset_index(name='num_trx')

# Clasificar el número de transacciones en los intervalos especificados
bins = [0, 1, 2, 3, 4, 5, 6, 9, 20, float('inf')]
labels = ['1', '2', '3', '4', '5', '6', '7-9', '10-20', '20+']
conteo_transacciones['intervalo'] = pd.cut(conteo_transacciones['num_trx'], bins=bins, labels=labels, right=False)

# Unir los datos clasificados con los datos originales para obtener la clasificación de cada transacción
transacciones_con_intervalo = pd.merge(conteo_transacciones, df, on=['idcliente', 'fecha'])

# Contar transacciones por intervalo, clasificación y día
resultado_final = transacciones_con_intervalo.groupby(['fecha', 'intervalo', 'Clasificacion']).size().unstack(fill_value=0).reset_index()

# Cambiar nombres de columnas para claridad
resultado_final.columns = ['Fecha', 'Intervalo', 'Genuinas', 'Fraude']

print(resultado_final)

##%%%%%%%%%%%%%%%%%%%
df = pd.DataFrame(data)
df['fecha'] = pd.to_datetime(df['fecha'])

# Clasificación de transacciones como Genuinas o indicador de Fraude 'F'
df['Clasificacion'] = df['indicadorFraude'].apply(lambda x: 'Fraude' if x == 'F' else 'Genuina')

# Contar transacciones por cliente y por fecha
conteo_transacciones = df.groupby(['idcliente', 'fecha']).size().reset_index(name='num_trx')

# Unir los datos clasificados con los datos originales para contar la clasificación de cada transacción
conteo_con_clasificacion = pd.merge(conteo_transacciones, df, on=['idcliente', 'fecha'])

# Clasificar el número de transacciones en los intervalos especificados
bins = [0, 1, 2, 3, 4, 5, 6, 9, 20, float('inf')]
labels = ['1', '2', '3', '4', '5', '6', '7-9', '10-20', '20+']
conteo_con_clasificacion['intervalo'] = pd.cut(conteo_con_clasificacion['num_trx'], bins=bins, labels=labels, right=False)

# Agrupar y contar las transacciones por intervalo y clasificación
resultado_final = conteo_con_clasificacion.groupby(['intervalo', 'Clasificacion']).size().unstack(fill_value=0).reset_index()
resultado_final.columns = ['Intervalo', 'Genuina', 'Fraude']

# Calcular el total de transacciones por intervalo
resultado_final['TRX'] = resultado_final['Genuina'] + resultado_final['Fraude']

# Ordenar las columnas según tu ejemplo
resultado_final = resultado_final[['Intervalo', 'TRX', 'Genuina', 'Fraude']]

print(resultado_final)

#################

import pandas as pd

# Supongamos que 'data' es tu conjunto de datos original, y 'df' se ha creado correctamente.
df = pd.DataFrame(data)
df['fecha'] = pd.to_datetime(df['fecha'])

# Clasificación de transacciones como Genuinas o indicador de Fraude 'F'
df['Clasificacion'] = df['indicadorFraude'].apply(lambda x: 'Fraude' if x == 'F' else 'Genuina')

# Contar transacciones por cliente, por fecha y clasificación
conteo_transacciones = df.groupby(['idcliente', 'fecha', 'Clasificacion']).size().reset_index(name='num_trx')

# Clasificar el número de transacciones en los intervalos especificados
bins = [0, 1, 2, 3, 4, 5, 6, 9, 20, float('inf')]
labels = ['1', '2', '3', '4', '5', '6', '7-9', '10-20', '20+']
conteo_transacciones['intervalo'] = pd.cut(conteo_transacciones['num_trx'], bins=bins, labels=labels, right=False)

# Agrupar y contar las transacciones por intervalo y clasificación
resultado_final = conteo_transacciones.groupby(['intervalo', 'Clasificacion']).size().unstack(fill_value=0)

# Asegurarse de que ambas columnas 'Genuina' y 'Fraude' estén presentes
resultado_final = resultado_final.reindex(columns=['Genuina', 'Fraude'], fill_value=0)

# Calcular el total de transacciones por intervalo
resultado_final['TRX'] = resultado_final['Genuina'] + resultado_final['Fraude']

# Restablecer el índice para tener 'Intervalo' como columna
resultado_final = resultado_final.reset_index()
resultado_final = resultado_final[['Intervalo', 'TRX', 'Genuina', 'Fraude']]

print(resultado_final)