import pandas as pd
import numpy as np

# Asumiendo que df es tu dataframe
# df = pd.read_csv('tu_archivo.csv')

# Paso 1: Encontrar los 3 comercios con mayor monto vendido
top_comercios = df.groupby('comercio')['monto'].sum().nlargest(3)

# Paso 2: Filtrar el dataframe para incluir solo esos comercios y hacer una copia explícita
df_top = df[df['comercio'].isin(top_comercios.index)].copy()

# Paso 3: Crear intervalos dinámicos basados en cuantiles
num_bins = 5  # Puedes ajustar el número de bins según lo necesario
df_top['monto_intervalo'] = pd.qcut(df_top['monto'], q=num_bins, precision=0)

# Paso 4: Agrupar por comercio e intervalo y calcular métricas del 'score' y frecuencia de transacciones
resultados = df_top.groupby(['comercio', 'monto_intervalo']).agg(
    frecuencia=('monto', 'size'),
    media_score=('score', 'mean'),
    mediana_score=('score', 'median'),
    moda_score=('score', lambda x: x.mode()[0] if not x.empty else np.nan)
)

# Mostrar resultados
print(resultados)


############
import pandas as pd
import numpy as np
import math

def divide_deciles_por_filas(df, column, num_divisions, label_prefix='D'):
    df_sorted = df.sort_values(column, ascending=True)
    num_rows = len(df_sorted)
    rows_per_decil = math.ceil(num_rows / num_divisions)
    labels = np.repeat([f'{label_prefix}{i+1:02d}' for i in range(num_divisions)], rows_per_decil)
    labels = labels[:num_rows]  # Ajustar el tamaño del array de labels
    df_sorted[f'{label_prefix}_Decil'] = labels
    return df_sorted

def subdivide_selected_decil(df, column, num_divisions, selected_decil):
    # Filtra para obtener solo las filas del decil seleccionado
    selected_df = df[df['D_Decil'] == f'D{selected_decil:02d}'].copy()
    
    # Divide el decil seleccionado en sub-deciles
    sub_deciles_df = divide_deciles_por_filas(selected_df, column, num_divisions, f'SubD{selected_decil}')
    
    return sub_deciles_df

# Divide el DataFrame completo en deciles
final_df = divide_deciles_por_filas(final_df, 'Monto', 10)

# Solicita al usuario que ingrese el número del decil del que quiere sub-dividir
selected_decil = int(input("Ingrese el número del decil del que desea subdividir (1-10): "))

# Asegurarse de que la entrada es válida
if 1 <= selected_decil <= 10:
    # Crea un nuevo DataFrame solo con las filas del decil seleccionado y lo subdivide en 10 sub-deciles
    sub_deciles_df = subdivide_selected_decil(final_df, 'Monto', 10, selected_decil)
    
    # Muestra el nuevo DataFrame con sub-deciles
    print(sub_deciles_df)
else:
    print("Número de decil inválido. Por favor ingrese un número entre 1 y 10.")


#####################


#!pip install ipywidgets
import pandas as pd
import numpy as np
import math
import ipywidgets as widgets
from IPython.display import display

def divide_deciles_por_filas(df, column, num_divisions, label_prefix='D'):
    df_sorted = df.sort_values(column, ascending=True)
    num_rows = len(df_sorted)
    rows_per_decil = math.ceil(num_rows / num_divisions)
    labels = np.repeat([f'{label_prefix}{i+1:02d}' for i in range(num_divisions)], rows_per_decil)
    labels = labels[:num_rows]  # Ajustar el tamaño del array de labels
    df_sorted[f'{label_prefix}_Decil'] = labels
    return df_sorted

def subdivide_selected_decil(df, column, num_divisions, selected_decil):
    selected_df = df[df['D_Decil'] == f'D{selected_decil:02d}'].copy()
    sub_deciles_df = divide_deciles_por_filas(selected_df, column, num_divisions, f'SubD{selected_decil}')
    print(sub_deciles_df)  # Imprimir directamente el DataFrame subdividido

# Divide el DataFrame completo en deciles
final_df = divide_deciles_por_filas(final_df, 'Monto', 10)

# Widget de selección para el decil
decil_selector = widgets.IntSlider(
    value=1,
    min=1,
    max=10,
    step=1,
    description='Decil:',
    continuous_update=False
)

# Botón para activar la subdivisión
button = widgets.Button(description="Subdividir Decil")

# Función para manejar el evento del botón
def on_button_clicked(b):
    subdivide_selected_decil(final_df, 'Monto', 10, decil_selector.value)

button.on_click(on_button_clicked)

# Mostrar los widgets
display(decil_selector, button)


####---------------------############

import pandas as pd
import matplotlib.pyplot as plt

def plot_bar_chart(df, x, y):
    """
    Plots a bar chart using the provided DataFrame and column names for x and y axes.
    
    Args:
    df (pandas.DataFrame): The DataFrame containing the data.
    x (str): The name of the column to use for the x-axis.
    y (str): The name of the column to use for the y-axis.
    """
    plt.figure(figsize=(10, 5))  # Configura el tamaño del gráfico
    plt.bar(df[x], df[y], color='blue')  # Crea un gráfico de barras con color azul
    plt.xlabel(x)  # Etiqueta del eje x
    plt.ylabel(y)  # Etiqueta del eje y
    plt.title(f'Bar Chart of {y} vs {x}')  # Título del gráfico
    plt.xticks(rotation=45)  # Rota las etiquetas del eje x para mejor visualización
    plt.grid(True)  # Añade una cuadrícula
    plt.show()  # Muestra el gráfico
