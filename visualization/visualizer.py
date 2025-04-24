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
        df_monthly = df[col_carga].resample('M').mean()

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

def graficar_temp_vs_consumo():
    clima = pd.read_csv('output/londres/nasa_power_londres_2024_preprocesado.csv', parse_dates=['Date'])
    energia = pd.read_csv('output/opsd/opsd_GB_preprocesado.csv', parse_dates=['utc_timestamp'])

    energia['Date'] = energia['utc_timestamp'].dt.date
    energia_diario = energia.groupby('Date').mean().reset_index()

    clima['Date'] = pd.to_datetime(clima['Date']).dt.date
    merged = pd.merge(clima, energia_diario, on='Date')

    plt.figure(figsize=(8, 6))
    plt.scatter(merged['T2M'], merged.iloc[:, -1], alpha=0.6)
    plt.xlabel('Temperatura Normalizada (T2M)')
    plt.ylabel('Carga Energética Normalizada')
    plt.title('Relación entre Temperatura y Consumo Energético - Londres')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('output/grafico_temp_vs_consumo.png')
    plt.close()

    corr = merged['T2M'].corr(merged.iloc[:, -1])
    print(f"Correlación T2M vs Carga: {corr:.3f}")

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
