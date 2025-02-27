# Proyecto ETL Apache Beam + Google Cloud

Info del proyecto Iniciado el 25-02-2025 a las 2 am

    proyectoETL/
    │── dataflow_python_examples/
    │   ├── data_generation.py  # Generar datos
    │   ├── data_transformation.py  # Transformaciones logarítmicas y limpieza
    │   ├── data_clustering.py  # Aplicación de K-Means
    │   ├── data_upload.py  # Subir a BigQuery y Cloud Storage
    │── scripts/
    │   ├── proyectoetl1.sh  # Script para ejecutar en la nube
    │── README.md  # Documentación del proyecto


## Scripts 

    data_generation.py → Genera datos aleatorios.
    data_transformation.py → Aplica transformaciones logarítmicas y limpieza de outliers.
    data_clustering.py → Aplica K-Means para clasificar en 4 clusters.
    data_upload.py → Sube los datos a Google Cloud Storage y BigQuery.


### Configuración Google Cloud para el Proyecto

#### Crear un Nuevo Proyecto en Google Cloud:

1.- Accede a la consola de Google Cloud en https://cloud.google.com/

2.- Crea un nuevo proyecto:

*   Nombre: proyectoETLKmeans
*   Guarda el ID del proyecto (lo usaremos después).

3.- Selecciona el nuevo proyecto en la parte superior de la consola o con el comando:

    gcloud config set project proyectoetlkmeans
    
    
#### Habilitar Servicios Necesarios
Para ejecutar el ETL en Google Cloud, habilita los siguientes servicios:

    gcloud services enable dataflow.googleapis.com \
    bigquery.googleapis.com \
    storage.googleapis.com \
    artifactregistry.googleapis.com

Esto permitirá usar:

* Cloud Dataflow para ejecutar Apache Beam.

* BigQuery para almacenar los resultados.

* Cloud Storage para archivos intermedios.


#### Clonar el Repositorio en Google Cloud Shell

Abre Google Cloud Shell en la consola y clona el repositorio:

    git clone https://github.com/NicoEMC/Proyectos-2025.git
    cd Proyectos-2025/proyectoETL_Kmeans/dataflow_python

#### Crear un Bucket en Google Cloud Storage

Vamos a crear un bucket para almacenar los datos:

    export PROJECT_ID=$(gcloud config get-value project)
    export BUCKET_NAME=$PROJECT_ID-dataflow
    gcloud storage buckets create gs://$BUCKET_NAME --location=us-central1

#### Subir los Archivos CSV a Cloud Storage

Esto subirá los archivos de datos generados a Cloud Storage:

    gsutil cp data_*.csv gs://$BUCKET_NAME/data_files/

#### Ejecutar el Pipeline en Apache Beam con Dataflow

<b> Instalar Apache Beam </b>, ejecutar en Google Cloud Shell:

    pip install apache-beam[gcp]==2.24.0

<b> Ejecutar data_ingestion.py en Dataflow </b>

    python data_generation.py  # Generar datos

    python data_transformation.py \
    --project=$PROJECT_ID \
    --region=us-central1 \
    --runner=DataflowRunner \
    --staging_location=gs://$BUCKET_NAME/test \
    --temp_location=gs://$BUCKET_NAME/test \
    --input=gs://$BUCKET_NAME/data_files/data_*.csv \
    --save_main_session





#### Test

Si quieres probar el codigo, te recomiendo crear un entorno virtual desde la carpeta y en la terminal digitar lo siguente: 

    $ python -m venv env

    $ env\Scripts\activate

Luego, debemos instalar las Dependencias en el Entorno Virtual 

    $ pip install pandas numpy scikit-learn google-cloud-storage google-cloud-bigquery

Finalmente debemos probar los Scripts

    $ python data_generation.py
    $ python data_transformation.py
    $ python data_clustering.py
    $ python data_upload.py


#### Link para guardar 

https://github.com/QUICK-GCP-LAB/2-Minutes-Labs-Solutions/blob/main/ETL%20Processing%20on%20Google%20Cloud%20Using%20Dataflow%20and%20BigQuery%20Python/gsp290.sh

https://www.cloudskillsboost.google/focuses/3460?parent=catalog


https://github.com/Niangmohamed/ETL-processing-on-Google-Cloud-using-Dataflow-and-BigQuery

https://github.com/Niangmohamed/ETL-processing-on-Google-Cloud-using-Dataflow-and-BigQuery/blob/main/dataflow_python_examples/data_lake_to_mart_cogroupbykey.py


https://github.com/NicoEMC/Proyectos-2025