import pandas as pd
import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Función para aplicar K-Means
def aplicar_kmeans(df, k=4):
    features = ["log_Contribucion_Anual", "log_Cantidad_Empleados", "log_Total_Voluntarios"]
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[features])

    kmeans = KMeans(n_clusters=k, random_state=1)
    df["Cluster"] = kmeans.fit_predict(df_scaled)

    return df

# Cargar datos, aplicar K-Means y guardar resultados
def procesar_cluster():
    fecha = datetime.date.today().strftime("%d-%m-%Y")
    input_file = f"transformed_data_{fecha}.csv"
    df = pd.read_csv(input_file)

    df = aplicar_kmeans(df)

    output_file = f"clustered_data_{fecha}.csv"
    df.to_csv(output_file, index=False)
    print(f"Archivo con clusters guardado: {output_file}")

if __name__ == "__main__":
    procesar_cluster()