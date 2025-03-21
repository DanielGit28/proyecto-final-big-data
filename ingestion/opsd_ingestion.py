import requests
import os

def descargar_opsd():
    url = "https://data.open-power-system-data.org/time_series/2020-10-06/time_series_60min_singleindex.csv"
    output_folder = "output/opsd"
    os.makedirs(output_folder, exist_ok=True)
    output_file = f"{output_folder}/opsd_timeseries.csv"

    print(f"Descargando dataset de OPSD...\nDesde: {url}")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Descarga completada: {output_file}")
    else:
        print(f"rror en la descarga. Código: {response.status_code}")
