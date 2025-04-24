import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
        df_monthly = df[col_carga].resample('ME').mean()

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

        print(f"Gráfico generado: {output_file}")
    except Exception as e:
        print(f"Error generando gráfico: {str(e)}")

def graficar_temp_vs_consumo(pais_codigo):
    ciudad = 'londres' if pais_codigo == 'GB' else 'estocolmo' if pais_codigo == 'SE' else 'berlin'
    clima_file = f"output/{ciudad}/nasa_power_{ciudad}_preprocesado.csv"
    energia_file = f"output/opsd/opsd_{pais_codigo}_preprocesado.csv"

    clima = pd.read_csv(clima_file, parse_dates=['Date'])
    energia = pd.read_csv(energia_file, parse_dates=['utc_timestamp'])
    
    energia['Date'] = energia['utc_timestamp'].dt.date
    energia_diario = energia.groupby('Date').mean().reset_index()

    clima['Date'] = pd.to_datetime(clima['Date']).dt.date
    merged = pd.merge(clima, energia_diario, on='Date')
    
    if not merged.empty:
        #Gráfico de líneas
        plt.figure(figsize=(10, 5))
        plt.plot(merged['Date'], merged['T2M'], label='Temp')
        plt.plot(merged['Date'], merged.iloc[:, -1], label='Carga')
        plt.title('Evolución diaria de temperatura y consumo energético')
        plt.xlabel('Fecha')
        plt.ylabel('Valor normalizado')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'output/grafico_temporal_temp_carga_{ciudad}.png')
        plt.show()

        merged['Mes'] = pd.to_datetime(merged['Date']).dt.month

        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=merged, x='T2M', y=merged.columns[-2], hue='Mes', palette='viridis')
        plt.xlabel('Temperatura Normalizada (T2M)')
        plt.ylabel('Carga Energética Normalizada')
        plt.title('Temperatura vs Consumo Energético (Coloreado por Mes)')
        plt.legend(title='Mes')
        plt.tight_layout()
        plt.savefig(f'output/grafico_temp_vs_consumo_coloreado_{ciudad}.png')
        plt.close()

        corr = merged['T2M'].corr(merged.iloc[:, -1])
        print(f"Correlación T2M vs Carga: {corr:.3f}")
    else:
        print("No se encontraron fechas comunes entre clima y energía.")


def analisis_descriptivo_opsd(pais_codigo):
    input_file = f"output/opsd/opsd_{pais_codigo}_preprocesado.csv"
    output_folder = "output/opsd/"

    print(f"\nGenerando análisis descriptivo avanzado de {pais_codigo}...")

    try:
        df = pd.read_csv(input_file, parse_dates=['utc_timestamp'])
        df.set_index('utc_timestamp', inplace=True)
        col_carga = [col for col in df.columns if col != 'utc_timestamp'][0]

        df['mes'] = df.index.month
        df['dia_semana'] = df.index.dayofweek

        resumen_mensual = df.groupby('mes')[col_carga].agg(['mean', 'std'])
        resumen_mensual.to_csv(f"{output_folder}/resumen_mensual_{pais_codigo}.csv")

        resumen_semanal = df.groupby('dia_semana')[col_carga].agg(['mean', 'std'])
        resumen_semanal.to_csv(f"{output_folder}/resumen_semanal_{pais_codigo}.csv")

        # Boxplot mensual
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='mes', y=col_carga, data=df)
        plt.title(f'Boxplot mensual de consumo - {pais_codigo}')
        plt.xlabel('Mes')
        plt.ylabel('Carga normalizada')
        plt.tight_layout()
        plt.savefig(f"{output_folder}/boxplot_mensual_{pais_codigo}.png")
        plt.close()

        # Gráfico de barras por día de semana
        plt.figure(figsize=(10, 5))
        sns.barplot(x=resumen_semanal.index, y=resumen_semanal['mean'], palette="Blues_d")
        plt.title(f'Consumo promedio por día de la semana - {pais_codigo}')
        plt.xlabel('Día de la semana (0=Lunes, 6=Domingo)')
        plt.ylabel('Carga energética (normalizada)')
        plt.tight_layout()
        plt.savefig(f"{output_folder}/barras_dia_semana_{pais_codigo}.png")
        plt.close()

        print(f"✅ Análisis descriptivo generado para {pais_codigo}.")

    except Exception as e:
        print(f"❌ Error generando análisis descriptivo: {str(e)}")
