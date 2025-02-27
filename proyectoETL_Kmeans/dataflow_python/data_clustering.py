import pandas as pd
import datetime
import os
import time
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def esperar_archivo(file_path, timeout=60):
    wait_time = 0
    while not os.path.exists(file_path) and wait_time < timeout:
        print(f"⏳ Esperando el archivo {file_path}... ({wait_time}/{timeout} seg)")
        time.sleep(2)
        wait_time += 2

    if not os.path.exists(file_path):
        print(f"❌ Error: No se encontró el archivo después de {timeout} segundos.")
        exit(1)

def aplicar_kmeans(df, k=4):
    features = ["log_Contribucion_Anual", "log_Cantidad_Empleados", "log_Total_Voluntarios"]
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[features])

    kmeans = KMeans(n_clusters=k, random_state=1)
    df["Cluster"] = kmeans.fit_predict(df_scaled)

    return df

def procesar_cluster():
    fecha = datetime.date.today().strftime("%d-%m-%Y")
    input_file = os.path.join(SCRIPT_DIR, f"transformed_data_{fecha}.csv")
    output_file = os.path.join(SCRIPT_DIR, f"clustered_data_{fecha}.csv")

    esperar_archivo(input_file)

    df = pd.read_csv(input_file)
    df = aplicar_kmeans(df)
    df.to_csv(output_file, index=False)

    print(f"✅ Archivo con clusters guardado: {output_file}")

if __name__ == "__main__":
    procesar_cluster()