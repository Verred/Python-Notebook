import pandas as pd
import numpy as np

# Suponiendo que df es tu DataFrame y 'columna_mixed' es la columna problemática
# Convertir toda la columna a string y luego aplicar una transformación
df['columna_mixed'] = df['columna_mixed'].astype(str)

# Usar expresiones regulares para mantener solo números y convertir cadenas vacías en NaN
df['columna_mixed'] = df['columna_mixed'].str.extract('(\d+)', expand=False)
df['columna_mixed'] = pd.to_numeric(df['columna_mixed'], errors='coerce')

# Ahora convertimos la columna a tipo entero, llenando los NaN con un valor por defecto, por ejemplo 0
df['columna_mixed'] = df['columna_mixed'].fillna(0).astype(int)

# Convertir los enteros a string y formatear con dos dígitos, rellenando con ceros a la izquierda si es necesario
df['columna_mixed'] = df['columna_mixed'].apply(lambda x: f'{x:02}')

# Revisar los resultados
print(df['columna_mixed'].head())



####################
import pandas as pd
import numpy as np

# Suponiendo que df es tu DataFrame y 'columna_mixed' es la columna problemática
# Convertir toda la columna a string y luego aplicar una transformación
df['columna_mixed'] = df['columna_mixed'].astype(str)

# Usar expresiones regulares para mantener solo números y convertir cadenas vacías en NaN
df['columna_mixed'] = df['columna_mixed'].str.extract('(\d+)', expand=False)
df['columna_mixed'] = pd.to_numeric(df['columna_mixed'], errors='coerce')

# Ahora convertimos la columna a tipo entero, llenando los NaN con un valor por defecto, por ejemplo 0
df['columna_mixed'] = df['columna_mixed'].fillna(0).astype(int)

# Revisar los resultados
print(df['columna_mixed'].head())

##############################
import pandas as pd

# Suponiendo que tienes tres DataFrames: df1, df2, y df3
# Asegúrate de que todos tienen las mismas columnas y en el mismo orden

# Concatenar los DataFrames
df_concatenado = pd.concat([df1, df2, df3], ignore_index=True)

# Mostrar las primeras filas del DataFrame resultante
print(df_concatenado.head())

##################
columnas_castear = {'ingreso_aplicante':'float64','credito_anterior':'category'}
df = df.astype(columnas_castear)

########
import pandas as pd

# Supongamos que 'key' es la llave única en df1 y df2, y 'campo1', 'campo2', 'campo3' son los campos en común entre df1 y df3

# Unir df1 y df2
df1 = df1.merge(df2[['key', 'finan']], on='key', how='left')

# Unir df1 y df3
df1 = df1.merge(df3[['campo1', 'campo2', 'campo3', 'finan']], on=['campo1', 'campo2', 'campo3'], how='left')

# Mostrar el resultado
print(df1.head())