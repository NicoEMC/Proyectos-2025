#!/bin/bash

# Habilitar modo estricto para capturar errores
set -e

# Configuración de variables
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"
export BUCKET_NAME="${PROJECT_ID}-dataflow"
export REPO_URL="https://github.com/NicoEMC/Proyectos-2025.git"
export PROJECT_DIR="$HOME/proyectoETL_Kmeans"

# Habilitar APIs necesarias
echo "Habilitando APIs necesarias..."
gcloud services enable dataflow.googleapis.com \
    bigquery.googleapis.com \
    storage.googleapis.com \
    artifactregistry.googleapis.com

# Crear el bucket en Cloud Storage si no existe
echo "Creando bucket en Cloud Storage..."
gcloud storage buckets create gs://$BUCKET_NAME --location=$REGION || echo "El bucket ya existe"

# Clonar el repositorio desde GitHub
echo "Clonando el repositorio..."
rm -rf $PROJECT_DIR
git clone --depth 1 --filter=blob:none --sparse $REPO_URL
cd $PROJECT_DIR

# Crear entorno virtual
echo "Creando entorno virtual..."
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias necesarias
echo "Instalando dependencias..."
pip install --upgrade pip setuptools wheel cython
pip install --upgrade numpy pandas scikit-learn
pip install --no-cache-dir --force-reinstall apache-beam[gcp]==2.48.0 || pip install --no-cache-dir apache-beam[gcp]==2.45.0
pip install google-cloud-storage google-cloud-bigquery

# Ejecutar generación de datos
echo "Ejecutando generación de datos..."
python dataflow_python/data_generation.py
sleep 5

# Subir archivos generados a Cloud Storage
echo "Subiendo archivos CSV a Cloud Storage..."
gsutil cp dataflow_python/data_*.csv gs://$BUCKET_NAME/data_files/

# Ejecutar transformación de datos en Dataflow
echo "Ejecutando transformación de datos en Dataflow..."
python dataflow_python/data_transformation.py \
  --project=$PROJECT_ID \
  --region=$REGION \
  --runner=DataflowRunner \
  --staging_location=gs://$BUCKET_NAME/staging \
  --temp_location=gs://$BUCKET_NAME/temp \
  --input=gs://$BUCKET_NAME/data_files/*.csv \
  --save_main_session

sleep 5

# Ejecutar modelo de clustering K-Means
echo "Ejecutando modelo de clustering..."
python dataflow_python/data_clustering.py

# Subir resultados a Cloud Storage y BigQuery
echo "Subiendo resultados a Cloud Storage y BigQuery..."
python dataflow_python/data_upload.py

echo "ETL completado con éxito."