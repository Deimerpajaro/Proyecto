import pandas as pd

# Cargar los datos desde la URL
df = pd.read_excel('https://raw.githubusercontent.com/Deimerpajaro/Proyecto/refs/heads/main/DataBases/Datos_2021_356.xlsx')

# Realiza cualquier procesamiento necesario aquí
print(df.head()) 