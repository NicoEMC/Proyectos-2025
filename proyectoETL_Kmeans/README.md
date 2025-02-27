# Proyecto ETL Apache Beam + Google Cloud

📅 Fecha de inicio: 25-02-2025.

🔍 Descripción: Este proyecto implementa un pipeline ETL utilizando Apache Beam en Google Cloud Dataflow, almacenando los resultados en BigQuery y gestionando archivos en Cloud Storage.

📂 Estructura del Proyecto

    proyectoETL_Kmeans/
    │── dataflow_python/
    │   ├── data_generation.py  # Generar datos
    │   ├── data_transformation.py  # Transformaciones logarítmicas y limpieza
    │   ├── data_clustering.py  # Aplicación de K-Means
    │   ├── data_upload.py  # Subir a BigQuery y Cloud Storage
    │── scripts/
    │   ├── proyectoetl1.sh  # Script para ejecutar en la nube
    │── README.md  # Documentación del proyecto


⚙️ Scripts 

    data_generation.py → Genera datos aleatorios.
    data_transformation.py → Aplica transformaciones logarítmicas y limpieza de outliers.
    data_clustering.py → Aplica K-Means para clasificar en 4 clusters.
    data_upload.py → Sube los datos a Google Cloud Storage y BigQuery.

🔹 Gráfico 3D Interactivo

![Ver Gráfico 3D Interactivo](https://github.com/NicoEMC/Proyectos-2025/blob/main/proyectoETL_Kmeans/dataflow_python/clustering_3D.gif)

## Configuración Google Cloud para el Proyecto

### Crear un Nuevo Proyecto en Google Cloud:

1.- Accede a la consola de Google Cloud en https://cloud.google.com/

2.- Crea un nuevo proyecto:

*   Nombre: proyectoETLKmeans
*   Guarda el ID del proyecto (lo usaremos después).

3.- Selecciona el nuevo proyecto en la parte superior de la consola o con el comando:

    gcloud config set project proyectoetlkmeans

    
### Habilitar Servicios Necesarios
Para ejecutar el ETL en Google Cloud, habilita los siguientes servicios:

    gcloud services enable dataflow.googleapis.com \
    bigquery.googleapis.com \
    storage.googleapis.com \
    artifactregistry.googleapis.com

Esto permitirá usar:

* Cloud Dataflow para ejecutar Apache Beam.

* BigQuery para almacenar los resultados.

* Cloud Storage para archivos intermedios.


### Clonar el Repositorio en Google Cloud Shell

Abre Google Cloud Shell y clona el repositorio:

    git clone https://github.com/NicoEMC/Proyectos-2025.git
    cd Proyectos-2025/proyectoETL_Kmeans

### Crear un Bucket en Google Cloud Storage

Vamos a crear un bucket para almacenar los datos:

    export PROJECT_ID=$(gcloud config get-value project)
    export BUCKET_NAME=$PROJECT_ID-dataflow
    gcloud storage buckets create gs://$BUCKET_NAME --location=us-central1

### Crear el Dataset en BigQuery

    bq --location=US mk --dataset $PROJECT_ID:flujo_cluster



## Ejecución del Pipeline ETL

Crear Entorno Virtual e Instalar Dependencias

    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel cython
    pip install numpy pandas scikit-learn google-cloud-storage google-cloud-bigquery

Ejecutar el Script de Automatización

    chmod +x scripts/proyectoetl1.sh
    ./scripts/proyectoetl1.sh

Verificar la Carga de Datos en BigQuery

    bq ls --project_id=proyectoetlkmeans
    bq query --nouse_legacy_sql 'SELECT * FROM `proyectoetlkmeans.flujo_cluster.resultados` LIMIT 10'


## Ejecución Paso a Paso si deseas ejecutar los scripts de forma manual:

1. Generar Datos

        python dataflow_python/data_generation.py

2. Subir los Archivos CSV a Cloud Storage

        gsutil cp dataflow_python/data_*.csv gs://$BUCKET_NAME/data_files/

3. Ejecutar la Transformación de Datos en Dataflow    

        python dataflow_python/data_transformation.py \
            --project=$PROJECT_ID \
            --region=us-central1 \
            --runner=DataflowRunner \
            --staging_location=gs://$BUCKET_NAME/test \
            --temp_location=gs://$BUCKET_NAME/test \
            --input=gs://$BUCKET_NAME/data_files/data_*.csv \
            --save_main_session

4. Ejecutar el Modelo de Clustering K-Means

        python dataflow_python/data_clustering.py

5. Subir los Resultados a Cloud Storage y BigQuery

        python dataflow_python/data_upload.py

