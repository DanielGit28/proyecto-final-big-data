import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

def procesar_datos(ruta_archivo, ciudad):
    print(f"\nProcesando datos para {ciudad.title()} desde {ruta_archivo}")

    df = pd.read_csv(ruta_archivo, parse_dates=['Date'])
    print(f"Datos cargados. {len(df)} registros encontrados.")

    # Limpieza de nulos
    df_clean = df.dropna()
    print(f"Después de limpieza: {len(df_clean)} registros")

    # Normalización de las variables (sin la columna Date)
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_clean.iloc[:, 1:]),
                             columns=df_clean.columns[1:],
                             index=df_clean['Date'])

    # Guardar el resultado normalizado
    output_folder = f'output/{ciudad}'
    os.makedirs(output_folder, exist_ok=True)
    output_file = f"{output_folder}/nasa_power_{ciudad}_2024_preprocesado.csv"
    df_scaled.to_csv(output_file)

    print(f"Preprocesamiento completo. Archivo guardado en: {output_file}")
