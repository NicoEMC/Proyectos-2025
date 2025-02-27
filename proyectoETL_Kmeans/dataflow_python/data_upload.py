import os
import datetime
from google.cloud import storage, bigquery

# 🔹 Leer configuración desde variables de entorno
PROJECT_ID = os.getenv("PROJECT_ID", "tu-proyecto-id")
BUCKET_NAME = os.getenv("BUCKET_NAME", f"{PROJECT_ID}-dataflow")
DATASET_NAME = os.getenv("DATASET_NAME", "flujo_cluster")
TABLE_NAME = os.getenv("TABLE_NAME", "resultados")

# 🔹 Directorio base de trabajo (evita rutas fijas)
BASE_DIR = os.getenv("BASE_DIR", os.getcwd())
DATA_DIR = os.path.join(BASE_DIR, "dataflow_python")

# ✅ Verificar si el dataset existe y crearlo si no
def ensure_dataset_exists():
    client = bigquery.Client()
    dataset_id = f"{PROJECT_ID}.{DATASET_NAME}"
    
    datasets = [dataset.dataset_id for dataset in client.list_datasets()]
    
    if DATASET_NAME not in datasets:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        client.create_dataset(dataset, exists_ok=True)
        print(f"✅ Dataset creado en BigQuery: {dataset_id}")
    else:
        print(f"✅ Dataset ya existente en BigQuery: {dataset_id}")

# ✅ Función para subir a Cloud Storage
def upload_to_gcs(source_file):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(os.path.basename(source_file))  
    blob.upload_from_filename(source_file)
    print(f"✅ Archivo subido a GCS: gs://{BUCKET_NAME}/{os.path.basename(source_file)}")

# ✅ Función para subir a BigQuery
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
    
    print(f"✅ Datos subidos a BigQuery: {table_id}")

# ✅ Subir datos procesados
def upload_data():
    fecha = datetime.date.today().strftime("%d-%m-%Y")
    output_file = os.path.join(DATA_DIR, f"clustered_data_{fecha}.csv")

    if not os.path.exists(output_file):
        print(f"❌ Error: No se encontró el archivo {output_file}")
        return

    ensure_dataset_exists()  # 🔹 Verificar y crear dataset antes de subir datos
    upload_to_gcs(output_file)
    upload_to_bigquery(output_file)

if __name__ == "__main__":
    upload_data()