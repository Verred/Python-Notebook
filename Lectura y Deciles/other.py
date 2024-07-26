# Crear el primer DataFrame con columnas A, B, C, D y eliminar duplicados
df1 = df[['A', 'B', 'C', 'D']].drop_duplicates()

# Crear el segundo DataFrame con columnas A, F y eliminar duplicados
df2 = df[['A', 'F']].drop_duplicates()


# Función para convertir listas a string
def list_to_string(lst):
    if isinstance(lst, list):
        return ', '.join(lst)
    return lst

# Aplicar la función a las columnas deseadas
df['col1'] = df['col1'].apply(list_to_string)
df['col2'] = df['col2'].apply(list_to_string)