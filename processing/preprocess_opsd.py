import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

# Diccionario de países (puedes expandirlo)
PAISES_OPSD = {
    'DE': 'Alemania',
    'GB': 'Reino Unido',
    'SE': 'Suecia',
    'FR': 'Francia',
    'ES': 'España',
    'IT': 'Italia',
    'PL': 'Polonia',
    'NL': 'Países Bajos'
}

def procesar_opsd_por_pais():
    input_file = "output/opsd/opsd_timeseries.csv"
    output_folder = "output/opsd"
    os.makedirs(output_folder, exist_ok=True)

    try:
        df = pd.read_csv(input_file, parse_dates=['utc_timestamp'])
        print(f"Filtrado cargado: {len(df)} registros")

        # Listamos países disponibles basados en columnas
        columnas_disponibles = [col for col in df.columns if '_load_actual_entsoe_transparency' in col]

        print("\nPaíses disponibles:")
        disponibles = []
        for i, col in enumerate(columnas_disponibles):
            codigo_pais = col.split('_')[0]
            nombre_pais = PAISES_OPSD.get(codigo_pais, "Desconocido")
            print(f"{i+1}. {codigo_pais} - {nombre_pais}")
            disponibles.append((codigo_pais, col, nombre_pais))

        eleccion = int(input("\nSelecciona el número del país a procesar: "))
        codigo_pais, columna_pais, nombre_pais = disponibles[eleccion - 1]

        # Filtramos y limpiamos
        df_clean = df[['utc_timestamp', columna_pais]].dropna()
        print(f"Registros después de limpieza: {len(df_clean)}")

        # Normalizamos solo la columna elegida
        scaler = MinMaxScaler()
        df_clean[columna_pais] = scaler.fit_transform(df_clean[[columna_pais]])

        # Guardamos
        output_file = f"{output_folder}/opsd_{codigo_pais}_preprocesado.csv"
        df_clean.to_csv(output_file, index=False)

        print(f"\n✅ Preprocesamiento de {nombre_pais} completado. Archivo en: {output_file}")

    except Exception as e:
        print(f"Error en procesamiento OPSD: {str(e)}")
