import pandas as pd
import openpyxl

# Ejemplo de creación de los DataFrames
df1 = pd.DataFrame({
    'Nombre': ['Comercio1', 'Comercio2'],
    'Descripcion': ['Des1', 'Des2']
})

df2 = pd.DataFrame({
    'Nombre': ['Comercio1', 'Comercio1', 'Comercio2'],
    'OtraColumna1': [4, 5, 6],
    'OtraColumna2': ['g', 't', 't']
})

# Guardar cada conjunto de datos en un archivo Excel separado
for index, row in df1.iterrows():
    nombre = row['Nombre']
    descripcion = row['Descripcion']
    
    # Filtrar filas correspondientes en df2
    df_filtered = df2[df2['Nombre'] == nombre].copy()
    
    # Crear un nuevo DataFrame para la descripción
    descripcion_df = pd.DataFrame({'Descripcion': [descripcion]})
    
    # Escribir en el archivo Excel
    with pd.ExcelWriter(f"{nombre}.xlsx", engine='openpyxl') as writer:
        df_filtered.to_excel(writer, sheet_name='Datos', index=False)
        descripcion_df.to_excel(writer, sheet_name='Descripción', index=False, startrow=0, startcol=len(df_filtered.columns) + 1)

print("Archivos Excel generados exitosamente.")


########
import pandas as pd
import openpyxl

# Ejemplo de creación de los DataFrames
df1 = pd.DataFrame({
    'Nombre': ['Comercio1', 'Comercio2'],
    'Descripcion': ['Des1', 'Des2']
})

df2 = pd.DataFrame({
    'Nombre': ['Comercio1', 'Comercio1', 'Comercio2'],
    'OtraColumna1': [4, 5, 6],
    'OtraColumna2': ['g', 't', 't']
})

# Crear un archivo Excel
with pd.ExcelWriter("output.xlsx", engine='openpyxl') as writer:
    for index, row in df1.iterrows():
        nombre = row['Nombre']
        descripcion = row['Descripcion']
        
        # Filtrar filas correspondientes en df2
        df_filtered = df2[df2['Nombre'] == nombre].copy()
        
        # Crear un nuevo DataFrame para la descripción
        descripcion_df = pd.DataFrame({'Descripcion': [descripcion]})
        
        # Escribir las filas correspondientes de df2
        df_filtered.to_excel(writer, sheet_name=nombre, index=False, startrow=0, startcol=0)
        
        # Escribir la descripción al lado derecho de las filas correspondientes de df2
        descripcion_df.to_excel(writer, sheet_name=nombre, index=False, startrow=0, startcol=len(df_filtered.columns) + 1)

print("Archivo Excel generado exitosamente.")