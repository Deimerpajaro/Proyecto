import plotly.express as px
import pandas as pd
import datetime

# Cargar los datos desde el archivo Excel
df_fuente = pd.read_csv('https://www.datos.gov.co/resource/3y4s-dmxy.csv')
df = df_fuente

# Mostrar los primeros registros del DataFrame para verificar
print(df)