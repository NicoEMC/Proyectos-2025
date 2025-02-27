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
rm -rf Proyectos-2025
git clone https://github.com/NicoEMC/Proyectos-2025.git
cd Proyectos-2025/proyectoETL_Kmeans

# Subir archivos de datos al bucket
echo "📂 Subiendo archivos CSV al bucket..."
gsutil cp dataflow_python/*.csv gs://$BUCKET_NAME/data_files/ || echo "⚠️ No se encontraron archivos CSV, revisa la generación."

# Instalar dependencias necesarias
echo "📦 Instalando dependencias..."
pip install --upgrade pip setuptools wheel cython
pip install --upgrade numpy
pip install pandas
pip install apache-beam[gcp]==2.48.0

# Ejecutar scripts del ETL en Google Cloud
echo "▶️ Ejecutando generación de datos..."
python dataflow_python/data_generation.py

echo "▶️ Ejecutando transformación de datos en Dataflow..."
python dataflow_python/data_transformation.py \
  --project=$PROJECT_ID \
  --region=$REGION \
  --runner=DataflowRunner \
  --staging_location=gs://$BUCKET_NAME/staging \
  --temp_location=gs://$BUCKET_NAME/temp \
  --input=gs://$BUCKET_NAME/data_files/*.csv \
  --save_main_session

echo "✅ ETL completado en Dataflow."