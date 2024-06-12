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