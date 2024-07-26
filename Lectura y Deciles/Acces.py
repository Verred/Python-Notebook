import pandas as pd
import pyodbc

# Supongamos que ya tienes un DataFrame llamado df
df = pd.DataFrame({
    'col1': [1, 2, 3],
    'col2': ['A', 'B', 'C'],
    'col3': [10.5, 20.5, 30.5]
})

# Configura la conexión a la base de datos de Access
conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ruta\a\tu\base_de_datos.accdb;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Crea la tabla en Access si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS MiTabla (
    col1 INTEGER,
    col2 TEXT(255),
    col3 DOUBLE
)
''')
conn.commit()

# Inserta el DataFrame en la tabla
for index, row in df.iterrows():
    cursor.execute('''
    INSERT INTO MiTabla (col1, col2, col3)
    VALUES (?, ?, ?)
    ''', row['col1'], row['col2'], row['col3'])
conn.commit()

# Cierra la conexión
cursor.close()
conn.close()

###

import pandas as pd
import pyodbc

# Supongamos que ya tienes un DataFrame llamado df
df = pd.DataFrame({
    'fecha': ['2023-07-25', '2023-07-25', '2023-07-26'],
    'col1': [1, 2, 3],
    'col2': ['A', 'B', 'C'],
    'col3': [10.5, 20.5, 30.5]
})

# Configura la conexión a la base de datos de Access
conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ruta\a\tu\base_de_datos.accdb;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Crea la tabla en Access si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS MiTabla (
    fecha DATE,
    col1 INTEGER,
    col2 TEXT(255),
    col3 DOUBLE
)
''')
conn.commit()

def replace_data_by_date(df, conn, table_name='MiTabla'):
    cursor = conn.cursor()
    
    # Encuentra todas las fechas únicas en el DataFrame
    unique_dates = df['fecha'].unique()
    
    for date in unique_dates:
        # Elimina los datos de la tabla para la fecha específica
        cursor.execute(f'''
        DELETE FROM {table_name} WHERE fecha = ?
        ''', date)
        conn.commit()
    
    # Inserta los nuevos datos en la tabla
    for index, row in df.iterrows():
        # Verifica si el registro ya existe
        cursor.execute(f'''
        SELECT COUNT(*) FROM {table_name} WHERE fecha = ? AND col1 = ? AND col2 = ? AND col3 = ?
        ''', row['fecha'], row['col1'], row['col2'], row['col3'])
        
        if cursor.fetchone()[0] == 0:  # Si no existe, inserta el registro
            cursor.execute(f'''
            INSERT INTO {table_name} (fecha, col1, col2, col3)
            VALUES (?, ?, ?, ?)
            ''', row['fecha'], row['col1'], row['col2'], row['col3'])
            conn.commit()
    
    cursor.close()

# Llama a la función para reemplazar los datos por fecha
replace_data_by_date(df, conn)

# Cierra la conexión
conn.close()
