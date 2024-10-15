import pandas as pd

from pyodide.http import open_url

        # URL del archivo Excel
        file_url = 'https://github.com/Deimerpajaro/Proyecto/blob/main/DataBases/Datos_2021_356.xlsx'

        # Cargar los datos desde la URL
        df = pd.read_excel(open_url(file_url))

        # Realiza cualquier procesamiento necesario aquí
        print(df.head())