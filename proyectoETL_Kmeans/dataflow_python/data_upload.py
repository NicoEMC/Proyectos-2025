import os
import datetime
from google.cloud import storage, bigquery

# Configuración
PROJECT_ID = "tu-proyecto-id"
BUCKET_NAME = f"{PROJECT_ID}-bucket"
DATASET_NAME = "flujo_cluster"
TABLE_NAME = "resultados"

# Función para subir a Cloud Storage
def upload_to_gcs(source_file):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(source_file)
    blob.upload_from_filename(source_file)
    print(f"Archivo subido a GCS: gs://{BUCKET_NAME}/{source_file}")

# Función para subir a BigQuery
def upload_to_bigquery(source_file):
    client = bigquery.Client()
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.{TABLE_NAME}"
    
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1
    )
    
    with open(source_file, "rb") as file:
        job = client.load_table_from_file(file, table_id, job_config=job_config)
        job.result()
    
    print(f"Datos subidos a BigQuery: {table_id}")

# Subir datos procesados
def upload_data():
    fecha = datetime.date.today().strftime("%d-%m-%Y")
    output_file = f"clustered_data_{fecha}.csv"

    upload_to_gcs(output_file)
    upload_to_bigquery(output_file)

if __name__ == "__main__":
    upload_data()