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


### Test

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