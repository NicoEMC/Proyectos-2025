#!/bin/bash

echo "🚀 Iniciando ejecución del ETL en Google Cloud..."

# Variables del proyecto
export PROJECT_ID=$(gcloud config get-value project)
export BUCKET_NAME=$PROJECT_ID-dataflow
export REGION="us-central1"

# Habilitar APIs necesarias
gcloud services enable dataflow.googleapis.com \
    bigquery.googleapis.com \
    storage.googleapis.com \
    artifactregistry.googleapis.com

# Crear el bucket en Cloud Storage (si no existe)
gcloud storage buckets create gs://$BUCKET_NAME --location=$REGION || echo "El bucket ya existe"

# Clonar el repositorio desde GitHub
git clone https://github.com/NicoEMC/Proyectos-2025.git
cd Proyectos-2025/proyectoETL_Kmeans

# Generar datos antes de copiarlos
python dataflow_python/data_generation.py 

# Subir archivos de datos al bucket
gsutil cp dataflow_python/*.csv gs://$BUCKET_NAME/data_files/

# Instalar dependencias
pip install --upgrade pip setuptools wheel
pip install "numpy<2"
pip install pandas
pip install apache-beam[gcp]==2.24.0

# Ejecutar ETL en Dataflow
python dataflow_python/data_transformation.py \
  --project=$PROJECT_ID \
  --region=$REGION \
  --runner=DataflowRunner \
  --staging_location=gs://$BUCKET_NAME/test \
  --temp_location=gs://$BUCKET_NAME/test \
  --input=gs://$BUCKET_NAME/data_files/*.csv \
  --save_main_session

echo "✅ ETL completado en Dataflow."