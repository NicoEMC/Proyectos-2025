import pandas as pd
import numpy as np
import datetime
import os
import time

# Obtener ruta del script actual
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

def aplicar_transformaciones(df):
    df["log_Contribucion_Anual"] = np.log(df["Contribucion_Anual"] + 1)
    df["log_Cantidad_Empleados"] = np.log(df["Cantidad_Empleados"] + 1)
    df["log_Total_Voluntarios"] = np.log(df["Total_Voluntarios"] + 1)
    return df

def eliminar_outliers(df, columnas):
    bounds = {c: dict(zip(["q1", "q3"], np.percentile(df[c], [25, 75]))) for c in columnas}
    for c in bounds:
        iqr = bounds[c]['q3'] - bounds[c]['q1']
        lower_bound = bounds[c]['q1'] - (1.5 * iqr)
        upper_bound = bounds[c]['q3'] + (1.5 * iqr)
        df = df[(df[c] >= lower_bound) & (df[c] <= upper_bound)]
    return df

def procesar_datos():
    fecha = datetime.date.today().strftime("%d-%m-%Y")
    input_file = os.path.join(SCRIPT_DIR, f"data_{fecha}.csv")
    output_file = os.path.join(SCRIPT_DIR, f"transformed_data_{fecha}.csv")

    esperar_archivo(input_file)

    df = pd.read_csv(input_file)
    df = aplicar_transformaciones(df)
    df = eliminar_outliers(df, ["log_Contribucion_Anual", "log_Cantidad_Empleados", "log_Total_Voluntarios"])
    df.to_csv(output_file, index=False)

    print(f"✅ Archivo transformado guardado: {output_file}")

if __name__ == "__main__":
    procesar_datos()