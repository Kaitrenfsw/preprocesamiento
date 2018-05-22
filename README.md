# Preprocesamiento
Repositorio que contiene al servicio y script de preprocesamiento de texto.

# Lenguaje utilizado:
Python 3.6.5

# Librerías necesarias:
* nltk
* contractions
* pymongo

Listados en el archivo requirements.txt para ser instalados con pip.

# nltk:
Luego de la instalación con pip se debe ejecutar comando de descarga de contenido:
* python -m nltk.downloader all

# Base de conocimiento (knowledge_base) en MongoDB:
Para pruebas iniciales (PMV) se importó la base de conocimientos a partir de archivos JSON a una base de datos en MongoDB.
Total de documentos importados: 41.476

* Nombre de la bd: knowledge_base
* Nombre de la colección: raw_data

En la/s carpeta/s contenedora de los documentos JSON:
* for filename in * ; do mongoimport --db knowledge_base --collection raw_data --file $filename ; done
