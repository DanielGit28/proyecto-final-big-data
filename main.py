import ingestion.nasa_ingestion as nasa
import ingestion.opsd_ingestion as opsd
import processing.preprocess_nasa as preprocess_nasa
import processing.preprocess_opsd as preprocess_opsd
import visualization.visualizer as visualizer

def menu_principal():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Descargar datos de NASA POWER API")
        print("2. Descargar y filtrar datos de Open Power System Data (OPSD)")
        print("3. Procesar datos de NASA (limpieza y normalización por ciudad)")
        print("4. Procesar datos de OPSD (selección de país y preprocesamiento)")
        print("5. Generar gráfico de consumo eléctrico OPSD por país")
        print("6. Salir")

        opcion = input("\nSelecciona una opción (1-6): ")

        if opcion == '1':
            menu_nasa()
        elif opcion == '2':
            opsd.descargar_opsd()
        elif opcion == '3':
            menu_procesamiento_nasa()
        elif opcion == '4':
            preprocess_opsd.procesar_opsd_por_pais()
        elif opcion == '5':
            menu_graficos_opsd()
        elif opcion == '6':
            print("\n Proceso finalizado. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, elige nuevamente.")

def menu_graficos_opsd():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Gráfico de consumo eléctrico OPSD por país")
        print("2. Grafic temperatura vs consumo Londres")
        print("3. Analisis descriptivo por pais")
        print("4. Salir")

        opcion = input("\nSelecciona una opción (1-6): ")

        if opcion == '1':
            pais_codigo = input("Ingresa el código del país procesado (Berlin (DE), Londres (GB), Estocolmo (SE), etc.): ").strip().upper()
            visualizer.graficar_opsd_preprocesado(pais_codigo)
        elif opcion == '2':
            pais_codigo = input("Ingresa el código del país procesado (Berlin (DE), Londres (GB), Estocolmo (SE), etc.): ").strip().upper()
            visualizer.graficar_temp_vs_consumo(pais_codigo)
        elif opcion == '3':
            pais_codigo = input("Ingresa el código del país procesado (Berlin (DE), Londres (GB), Estocolmo (SE), etc.): ").strip().upper()
            visualizer.analisis_descriptivo_opsd(pais_codigo)
        elif opcion == '4':
            break
        else:
            print("Opción inválida. Por favor, elige nuevamente.")
    

def menu_nasa():
    ciudades = {
        '1': ('Estocolmo', 59.3293, 18.0686),
        '2': ('Londres', 51.5074, -0.1278),
        '3': ('Berlín', 52.5200, 13.4050)
    }

    print("\n--- NASA POWER API ---")
    for key, (ciudad, lat, lon) in ciudades.items():
        print(f"{key}. {ciudad} (Lat: {lat}, Lon: {lon})")

    eleccion = input("\nSelecciona la ciudad: ")

    if eleccion in ciudades:
        ciudad, lat, lon = ciudades[eleccion]
        print(f"Descargando datos para {ciudad}...")
        nasa.descargar_datos_nasa(ciudad, lat, lon)
    else:
        print("Opción no válida.")

def menu_procesamiento_nasa():
    print("\n--- PROCESAMIENTO NASA ---")
    ciudad = input("Escribe el nombre de la ciudad (estocolmo, londres, berlin): ").strip().lower()
    archivo = f"output/{ciudad}/nasa_power_{ciudad}.csv"
    
    try:
        preprocess_nasa.procesar_datos(archivo, ciudad)
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}. Descarga los datos primero.")

if __name__ == "__main__":
    menu_principal()
