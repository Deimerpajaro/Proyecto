# Paso 1: Conexión con la fuente de datos (Archivo en Excel)
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import datetime
import numpy as np
import seaborn as sns

# Cargar los datos desde el archivo Excel
#df_fuente = pd.read_excel('C:\\Users\\lenovo\\Downloads\\Datos_Proyecto\\Datos_2021_356.xlsx')

# Lista de archivos de Excel que quieres unir
archivos_excel = ['C:\\Users\\lenovo\\Downloads\\Datos_Proyecto\\Datos_2019_356.xlsx', 
                  'C:\\Users\\lenovo\\Downloads\\Datos_Proyecto\\Datos_2020_356.xlsx',
                  'C:\\Users\\lenovo\\Downloads\\Datos_Proyecto\\Datos_2021_356.xlsx',
                  'C:\\Users\\lenovo\\Downloads\\Datos_Proyecto\\Datos_2022_356.xlsx',
                  'C:\\Users\\lenovo\\Downloads\\Datos_Proyecto\\Datos_2023_356.xlsx']

# Crear una lista vacía para almacenar los DataFrames
dataframes = []

# Leer cada archivo y agregarlo a la lista
for archivo in archivos_excel:
    df = pd.read_excel(archivo)
    dataframes.append(df)

# Concatenar todos los DataFrames en uno solo
df_fuente = pd.concat(dataframes, ignore_index=True)

# Función para convertir semana en fecha aproximada (primer día de la semana)
def semana_a_fecha(anio, semana):
    return datetime.datetime.strptime(f'{anio}-W{semana}-1', "%Y-W%U-%w").date()

# Aplicar la función al DataFrame y cargar la fecha aproximada
df_fuente['FechaIncidente'] = df_fuente.apply(lambda row: semana_a_fecha(row['ANO'], row['SEMANA']), axis=1)

#Nueva columna con etapas del ciclo de vida

#Se definen rangoz de los ciclos de vida
conditions=[
    (df_fuente['EDAD']>0) & (df_fuente['EDAD']<=5),
    (df_fuente['EDAD']>5) & (df_fuente['EDAD']<=11),
    (df_fuente['EDAD']>11) & (df_fuente['EDAD']<=18),
    (df_fuente["EDAD"]>18) & (df_fuente["EDAD"]<=26),
    (df_fuente["EDAD"]>26) & (df_fuente["EDAD"]<=59),
    (df_fuente["EDAD"]>=60)
]
values=["Primera Infancia","Infancia","Adolescencia","Juventud","Adultez","Vejez"]

df_fuente["Ciclo_de_Vida"]=np.select(conditions,values)

# Filtrar los departamentos 
df_dpts=df_fuente[(df_fuente["Departamento_ocurrencia"]=="BOLIVAR") | (df_fuente["Departamento_ocurrencia"]=="CORDOBA") | (df_fuente["Departamento_ocurrencia"]=="SUCRE") | (df_fuente["Departamento_ocurrencia"]=="SAN ANDRES")]

#Representacion de intenos de suicidios por departamentos de estudios 

# Tranformación: agrupación por año y departamento 
df_mp = df_dpts.groupby(['Departamento_ocurrencia','ANO']).confirmados.sum().reset_index()

df_pivoteado= df_mp.pivot(index='Departamento_ocurrencia',columns='ANO',values='confirmados')

fig_mc=sns.heatmap(df_pivoteado)
print("Itentos de Suicidios en el caribe Colombiano")
fig_mc
