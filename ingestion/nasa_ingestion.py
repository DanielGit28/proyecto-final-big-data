import requests
import pandas as pd
import os
import json
import unicodedata

def quitar_tildes(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )

def descargar_datos_nasa(ciudad, latitude, longitude):
    # Parámetros fijos
    start_date = '20190930'
    end_date = '20200930'
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

    # Se crea un DataFrame consolidado
    df = pd.DataFrame()

    for var in variables:
        if var in records:
            print(f"Procesando variable: {var}")
            var_data = pd.DataFrame.from_dict(records[var], orient='index', columns=[var])
            df = pd.concat([df, var_data], axis=1)
        else:
            print(f"Advertencia: {var} no encontrado en la respuesta.")

    df.index.name = 'Date'
    
    ciudad_sin_tildes = quitar_tildes(ciudad.lower())
    print('ciudad ', ciudad, ciudad_sin_tildes)
    # Crear directorio de salida si no existe o si se quiere
    output_folder = f'output/{ciudad_sin_tildes}'
    os.makedirs(output_folder, exist_ok=True)

    output_file = f"{output_folder}/nasa_power_{ciudad_sin_tildes}.csv"
    df.to_csv(output_file)

    print(f"Archivo guardado en: {output_file}")
