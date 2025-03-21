#!/bin/bash

# Ruta del archivo local (ajustalo según tu ruta)
LOCAL_PATH="./data/nasa_power/nasa_power_london_2023-01-01_2023-12-31.csv"

# Ruta en HDFS
HDFS_PATH="/user/bigdata/raw/nasa_power"

# Comando para crear el directorio en HDFS si no existe
hdfs dfs -mkdir -p $HDFS_PATH

# Comando para subir el archivo
hdfs dfs -put -f $LOCAL_PATH $HDFS_PATH

echo "Archivo subido a HDFS en: $HDFS_PATH"
