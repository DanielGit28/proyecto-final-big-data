import requests
import pandas as pd
import os
import json

def descargar_datos_nasa(ciudad, latitude, longitude):
    # Parámetros fijos
    start_date = '20240101'
    end_date = '20241231'
    community = 'RE'
    
    variables = [
        "T2M",                # Temperatura
        "RH2M",               # Humedad relativa
        "PRECTOTCORR",        # Precipitación
        "ALLSKY_SFC_SW_DWN"   # Radiación solar
    ]

    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?start={start_date}&end={end_date}"
        f"&latitude={latitude}&longitude={longitude}"
        f"&community={community}"
        f"&parameters={','.join(variables)}"
        f"&format=JSON"
    )

    response = requests.get(url)
    print(f"Status code: {response.status_code}")

    data = response.json()

    if 'properties' not in data:
        print("Respuesta inesperada de la API:")
        print(json.dumps(data, indent=4))
        return

    records = data['properties']['parameter']

    # Creamos un DataFrame consolidado
    df = pd.DataFrame()

    for var in variables:
        if var in records:
            print(f"Procesando variable: {var}")
            var_data = pd.DataFrame.from_dict(records[var], orient='index', columns=[var])
            df = pd.concat([df, var_data], axis=1)
        else:
            print(f"Advertencia: {var} no encontrado en la respuesta.")

    df.index.name = 'Date'

    # Crear directorio de salida si no existe
    output_folder = f'output/{ciudad.lower()}'
    os.makedirs(output_folder, exist_ok=True)

    output_file = f"{output_folder}/nasa_power_{ciudad.lower()}_2024.csv"
    df.to_csv(output_file)

    print(f"Archivo guardado en: {output_file}")
