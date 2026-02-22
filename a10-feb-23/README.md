# Clase práctica: Plataforma de inspección con drones

## 1. Contexto narrativo

Imagina que trabajas para **InfraDron S.L.**, una empresa de inspección de infraestructuras (puentes, torres eléctricas, edificios) mediante drones. La empresa recibe diariamente cientos de imágenes capturadas por diferentes operadores de drones. Cada operador tiene su propio identificador (id usuario).

Actualmente, las imágenes se almacenan en discos locales sin estructura y los metadatos no está centralizados. La empresa necesita una **mini plataforma** que permita:

- Subir imágenes de forma organizada por usuario
- Almacenar metadatos de cada imagen en una base de datos
- Exportar datos de todos los operafdores para análisis
- Procesar imágenes (ajustes básicos como brillo) cuando sea necesario

Tu misión es diseñar e implementar esta plataforma usando tecnologías modernas de contenedores, APIs y almacenamiento object storage compatible con S3.

---

## 2. Arquitectura

- **api**: Aplicación FastAPI que expone los endpoints REST. Se comunica con MinIO y PostgreSQL.
- **minio**: Almacenamiento de objetos compatible con S3. Un bucket por usuario.
- **postgres**: Base de datos relacional para metadata de imágenes.

---

## 3. Requisitos funcionales

- **`/upload-image`**  
  Recibe imagen (form-data). Sube a MinIO en bucket por usuario, extrae metadata y la guarda en PostgreSQL.

- **`/images`**  
  Lista todas las imágenes con su metadata.

- **`/export-csv`**  
  Exporta un CSV global con todas las imágenes y sus columnas de metadata.

- **`/process-image/{image_id}`**  
  Ajusta brillo de una imagen (factor 1.2 o 0.8) con numpy y guarda la imagen procesada en MinIO.


### Metadata de cada imagen

- `image_name`
- `bucket` (usuario)
- `height`
- `width`
- `size_bytes`
- `format`
- `upload_date`
- `s3_link`

---

## 4. Ciencia de datos

Una vez desplegada la plataforma y subidas algunas imágenes:

1. **Obtener el CSV global** usando el endpoint `GET /export-csv`.
2. **Leer el CSV con pandas.**
3. **Agrupar por bucket (usuario).**
4. **Calcular las siguientes métricas** (usando **pandas** y **numpy** según corresponda):
   - Media del ancho (`width`) por usuario
   - Media del alto (`height`) por usuario
   - Desviación estándar del tamaño (`size_bytes`) por usuario
   - Número de imágenes con ancho > 1000 por usuario

---

## 5. Requisitos técnicos

- **Docker Compose** con red interna definida entre los servicios.
- **Volúmenes persistentes** para MinIO y PostgreSQL.
- **Variables de entorno** en archivo `.env` (ej: `MINIO_HOST`, `POSTGRES_HOST`, etc.).
- Librería **boto3** para MinIO (compatible S3).
- Librería **psycopg2** para PostgreSQL.
- **FastAPI** con manejo correcto de subida de archivos (`UploadFile`).
- Extracción de **metadatos reales** de la imagen (dimensiones, formato, tamaño).
- **numpy** para el ajuste de brillo (multiplicación del array de píxeles por factor). Permitir valor global o valor por filas (vector de brillos)


**¡No dudes en investigar y consultar toda la documentación oficial de las librerías y tecnologías usadas en este proyecto!**  
Buscar información por tu cuenta es parte fundamental del aprendizaje.  
Si alguna parte no te queda clara o tienes dudas concretas, **pregunta al profesor** sin problema.