import os
import requests
import json

def delete_entities(orion_url, link_header, fiware_service, entity_ids):
    """
    Borra entidades NGSI-LD del servidor Orion-LD.

    :param orion_url: URL del servidor Orion-LD
    :param link_header: Cabecera "Link" requerida para las solicitudes
    :param fiware_service: Cabecera "Fiware-Service" requerida para las solicitudes
    :param entity_ids: Lista de IDs de entidades a eliminar
    """
    headers = {
        'Link': link_header,
        'Fiware-Service': fiware_service
    }

    for entity_id in entity_ids:
        entity_url = f"{orion_url}/{entity_id}"

        try:
            response = requests.delete(entity_url, headers=headers)

            if response.status_code == 204:
                print(f"Entidad {entity_id} eliminada correctamente.")
            else:
                print(f"Error al eliminar la entidad {entity_id}: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Error inesperado al intentar eliminar la entidad {entity_id}: {str(e)}")

def load_entity_ids(folder_path):
    """
    Carga los IDs de entidades desde archivos JSON-LD en una carpeta.

    :param folder_path: Ruta de la carpeta que contiene los archivos .jsonld
    :return: Lista de IDs de entidades
    """
    entity_ids = []

    if not os.path.isdir(folder_path):
        print(f"El directorio {folder_path} no existe.")
        return entity_ids

    files = [f for f in os.listdir(folder_path) if f.endswith('.jsonld')]

    for file in files:
        file_path = os.path.join(folder_path, file)

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if 'id' in data:
                    entity_ids.append(data['id'])
                else:
                    print(f"El archivo {file} no contiene un ID de entidad válido.")

        except json.JSONDecodeError:
            print(f"Error al leer el archivo {file}. Asegúrate de que esté en formato JSON válido.")
        except Exception as e:
            print(f"Error inesperado al procesar el archivo {file}: {str(e)}")

    return entity_ids

# Parámetros
folder_path = './entidades_orion'  # Cambia esto a tu ruta
orion_url = 'http://apr.inf.um.es:1026/ngsi-ld/v1/entities'
link_header = '<http://nodered:1880/context>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
fiware_service = 'campus-service'

# Obtener IDs de entidades desde archivos JSON-LD
entity_ids = load_entity_ids(folder_path)

if entity_ids:
    # Eliminar entidades del servidor
    delete_entities(orion_url, link_header, fiware_service, entity_ids)
else:
    print("No se encontraron entidades para eliminar.")
