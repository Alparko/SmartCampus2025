import os
import requests
import json

def upload_entities(folder_path, orion_url, link_header, fiware_service):
    # Verifica que la carpeta existe
    if not os.path.isdir(folder_path):
        print(f"El directorio {folder_path} no existe.")
        return

    # Lista todos los archivos .jsonld en la carpeta
    files = [f for f in os.listdir(folder_path) if f.endswith('.jsonld')]

    if not files:
        print("No se encontraron archivos .jsonld en el directorio.")
        return

    headers = {
        #'Link': link_header,
        'NGSILD-Tenant': fiware_service,
        'Content-Type': 'application/ld+json'
    }

    for file in files:
        file_path = os.path.join(folder_path, file)

        try:
            with open(file_path, 'r') as f:
                entity_data = json.load(f)

            response = requests.post(orion_url, headers=headers, json=entity_data)

            if response.status_code == 201:
                print(f"Entidad del archivo {file} subida correctamente.")
            else:
                print(f"Error al subir el archivo {file}: {response.status_code} - {response.text}")

        except json.JSONDecodeError:
            print(f"Error al leer el archivo {file}. Asegúrate de que esté en formato JSON válido.")
        except Exception as e:
            print(f"Error inesperado al procesar el archivo {file}: {str(e)}")

# Parámetros del servidor y directorio de archivos
folder_path = './entidades_orion'  # Cambia esto a tu ruta
orion_url = 'http://apr.inf.um.es:1026/ngsi-ld/v1/entities'
link_header = '<http://nodered:1880/context>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
fiware_service = 'campus-service'

upload_entities(folder_path, orion_url, link_header, fiware_service)
