import pandas as pd
import matplotlib.pyplot as plt
import os

def graficar_opsd_preprocesado(pais_codigo):
    input_file = f"output/opsd/opsd_{pais_codigo}_preprocesado.csv"
    output_folder = "output/opsd/"

    print(f"\nGenerando gráfico desde el preprocesado de {pais_codigo}...")

    try:
        df = pd.read_csv(input_file, parse_dates=['utc_timestamp'])
        df.set_index('utc_timestamp', inplace=True)

        # Extraemos la única columna de carga disponible
        col_carga = [col for col in df.columns if col != 'utc_timestamp'][0]

        # Resample mensual de la serie normalizada
        df_monthly = df[col_carga].resample('M').mean()

        # Graficamos
        plt.figure(figsize=(14, 6))
        plt.plot(df_monthly.index, df_monthly.values, label=pais_codigo)
        plt.title(f'Consumo eléctrico mensual normalizado - {pais_codigo}')
        plt.xlabel('Fecha')
        plt.ylabel('Carga (normalizada)')
        plt.legend()
        plt.tight_layout()

        os.makedirs(output_folder, exist_ok=True)
        output_file = f"{output_folder}grafico_{pais_codigo}_preprocesado.png"
        plt.savefig(output_file)
        plt.close()

        print(f"✅ Gráfico generado: {output_file}")
    except Exception as e:
        print(f"❌ Error generando gráfico: {str(e)}")
