## Como configurar el Storage en GCP

1. Entrar en la consola de Google Cloud
https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts?supportedpurview=project&pli=1

2. Crear Proyecto. Lo llamamos EvenTITO.

3. Create Service Account
https://console.cloud.google.com/iam-admin/serviceaccounts/create?project=eventito&supportedpurview=project

Elegir el rol Storage Admin.

4. Add Key -> JSON KEY.


Se pueden usar distintos tipos de Bucket: STANDARD, NEARLINE, COLDLINE y ARCHIVE. Las ultimas 3 se utilizan para datos que se acceden muy esporadicamente (1 vez por mes, 1 vez por trimestre, 1 vez por año). Standard es la solución más común para datos que se acceden frecuentemente.

Decidimos usar una única región (us-central1), para tener consistencia y no necesitamos replicación de datos entre regiones (no vamos a tener requests de otras partes del mundo).


Con esto ya se tiene una cuenta de servicio con acceso a Google Storage. Para crear todos los buckets que se necesitan, correremos una serie de scripts ubicados en `/scripts/storage-setup`.

## Scripts

1. Agregar el JSON descargado en la misma carpeta que `/scripts/storage-setup` con el nombre `eventito-key.json`.

2. Desde la terminal correr:

```shell
~/scripts/storage-setup$ python3 json-to-dict.py
```

Este script imprimirá tu json como un string. Este string es el que usamos en el .env del proyecto bajo la variable `GCP_CREDENTIALS`.

3. Correr el script que crea los buckets en Googel Storage.

```shell
~/scripts/storage-setup$ python3 storage.py
```

4. Recuerda agregar en el .env los nombres de los buckets correspondientes. En el script `storage.py` veras los nombres de los buckets elegidos.


## Buckets cors policy

Para configurar la politica CORS a cada bucket seguiremos los siguientes pasos desde la consola de gcp:

1) Crear un archivo de configuracion de cors en formato json:
   ```touch cors_config.json```

2) Editar dicho archivo con la configuración deseada:
   ```edit cors_config.json```

3) Verificar la configuración
   ```cat cors_config.json```

```
[
    {
        "origin": ["http://localhost:5173"],
        "method": ["PUT"],
        "responseHeader": ["*"],
        "maxAgeSeconds": 3600
    }
]
```
4) Actualizar cada uno de los buckets con la configuracion de cors

   ```gcloud storage buckets update gs://eventito-payments_and_certificates --cors-file=cors_config.json```

   ```gcloud storage buckets update gs://eventito-profile_images --cors-file=cors_config.json```
   
   ```gcloud storage buckets update gs://eventito-static_event_content --cors-file=cors_config.json```
   
   ```gcloud storage buckets update gs://eventito-submissions_and_reviews --cors-file=cors_config.json```


5) Por último verificar que los buckets tenga aplicada la nueva configuracion de CORS
   
   ```gcloud storage buckets describe gs://eventito-payments_and_certificates```
