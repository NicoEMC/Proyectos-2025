import random
import pandas as pd
import datetime
import os

# Generar número de identificador único (9 dígitos)
def generar_identificador(numero_identificador):
    while True:
        identificador = random.randint(100000000, 999999999)  # identificador de 9 dígitos
        if identificador not in numero_identificador:  # Asegurar que sea único
            numero_identificador.add(identificador)
            return identificador

# Generar datos aleatorios
def generar_random_data(num_samples=100):
    numero_identificador = set()
    data = []

    for _ in range(num_samples):
        idn = generar_identificador(numero_identificador)
        cantidad_empleados = random.randint(5, 500)  
        contribucion_anual = random.randint(80000, 1000000) + (cantidad_empleados * random.randint(1000, 20000))
        total_voluntarios = random.randint(100, 100000)

        data.append([idn, contribucion_anual, cantidad_empleados, total_voluntarios])

    return pd.DataFrame(data, columns=["Identificador_Comuna", "Contribucion_Anual", "Cantidad_Empleados", "Total_Voluntarios"])

# Guardar el archivo CSV
def guardar_csv():
    df = generar_random_data()
    fecha = datetime.date.today().strftime("%d-%m-%Y")
    output_path = f"data_{fecha}.csv"
    df.to_csv(output_path, index=False)
    print(f"Archivo CSV guardado: {output_path}")

if __name__ == "__main__":
    guardar_csv()