import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime

# Función para convertir semana en fecha aproximada (primer día de la semana)
def semana_a_fecha(anio, semana):
    return datetime.datetime.strptime(f'{anio}-W{semana}-1', "%Y-W%U-%w").date()

# Paso 1: Conexión con la fuente de datos (Archivo en Excel)
file_path = 'C:\\Users\\knives\\Desktop\\Devs\\Python\\BootCampUTB\\Proyecto\\DataBases\\Datos_2021_356.xlsx'
df_fuente = pd.read_excel(file_path)

# Paso 2: Transformaciones iniciales
df_fuente['FechaIncidente'] = df_fuente.apply(lambda row: semana_a_fecha(row['ANO'], row['SEMANA']), axis=1)

# Definir rangos de los ciclos de vida
bins = [0, 5, 11, 18, 26, 59, float('inf')]
labels = ["Primera Infancia", "Infancia", "Adolescencia", "Juventud", "Adultez", "Vejez"]
df_fuente['Ciclo_de_Vida'] = pd.cut(df_fuente['EDAD'], bins=bins, labels=labels, right=True, include_lowest=True)

# Filtrar los departamentos de interés
deptos_interes = ["BOLIVAR", "CORDOBA", "SUCRE", "SAN ANDRES"]
df_dpts = df_fuente[df_fuente["Departamento_ocurrencia"].isin(deptos_interes)]

# Paso 3: Crear gráficos

# Gráfico de calor (heatmap)
df_mp = df_dpts.groupby(['Departamento_ocurrencia', 'ANO']).confirmados.sum().unstack().fillna(0)
fig_mc = px.imshow(df_mp, labels=dict(x="Año", y="Departamento", color="Confirmados"),
                   x=df_mp.columns, y=df_mp.index,
                   title="Intentos de Suicidio en el Caribe Colombiano")

# Gráfico de torta (pie chart)
df_torta = df_dpts.groupby('Departamento_ocurrencia').confirmados.sum().reset_index()
fig_torta = px.pie(df_torta, values='confirmados', names='Departamento_ocurrencia', title='Distribución por Departamentos')

# Generación del dashboard
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Tableros Población'),
    html.Div(children='Tableros interactivos sobre intentos de suicidio en el Caribe Colombiano'),
    dcc.Graph(id='heatmap', figure=fig_mc),
    dcc.Graph(id='pie-chart', figure=fig_torta),
    html.Label('Selecciona el Año:'),
    dcc.Dropdown(
        id='dropdown-ano',
        options=[{'label': str(ano), 'value': ano} for ano in df_dpts['ANO'].unique()],
        value=df_dpts['ANO'].min(),
        clearable=False
    ),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='bar-chart-1'),
    dcc.Graph(id='bar-chart-2'),
    dcc.Graph(id='bar-chart-3')
])

@app.callback(
    [Output('line-chart', 'figure'),
     Output('bar-chart-1', 'figure'),
     Output('bar-chart-2', 'figure'),
     Output('bar-chart-3', 'figure')],
    [Input('dropdown-ano', 'value')]
)
def update_graphs(selected_year):
    df_filtered = df_dpts[df_dpts['ANO'] == selected_year]
    
    # Gráfico de líneas (line chart)
    df1 = df_filtered.groupby(['Departamento_ocurrencia', 'FechaIncidente']).confirmados.sum().reset_index()
    fig_lineas = px.line(df1, x="FechaIncidente", y="confirmados", color="Departamento_ocurrencia",
                         title=f'Tendencia de Incidentes de Suicidio en {selected_year}')
    
    # Gráfico de barras por estrato y departamento (bar chart)
    df2 = df_filtered.groupby(['estrato', 'Departamento_ocurrencia']).confirmados.sum().reset_index()
    fig_columna_1 = px.bar(df2, x="estrato", y="confirmados", color="Departamento_ocurrencia", barmode="group",
                           title=f'Casos por Estratos vs Departamentos en {selected_year}')
    
    # Gráfico de barras por sexo y fecha (bar chart)
    df3 = df_filtered.groupby(['SEXO', 'FechaIncidente']).confirmados.sum().reset_index()
    fig_barras_sexo = px.bar(df3, x='FechaIncidente', y='confirmados', color='SEXO', title=f'Tendencia Suicida según el Género en {selected_year}')
    
    # Gráfico de barras por ciclo de vida y departamento para mujeres (bar chart)
    df_sexf = df_filtered[df_filtered["SEXO"] == "F"]
    df_sexf['Ciclo_de_Vida'] = pd.Categorical(df_sexf['Ciclo_de_Vida'], categories=labels, ordered=True)
    df4 = df_sexf.groupby(['Departamento_ocurrencia', 'Ciclo_de_Vida']).confirmados.sum().reset_index()
    fig_columna_2 = px.bar(df4, x="Ciclo_de_Vida", y="confirmados", color="Departamento_ocurrencia", barmode="group",
                           title=f'Intentos de Suicidio en Mujeres por Ciclo de Vida en {selected_year}')
    
    return fig_lineas, fig_columna_1, fig_barras_sexo, fig_columna_2

if __name__ == '__main__':
    app.run_server(debug=True)
