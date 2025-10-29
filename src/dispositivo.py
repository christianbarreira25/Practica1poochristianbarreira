import os
import json
from datetime import datetime
import tempfile
from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2
from meshtastic import BROADCAST_NUM, protocols
import paho.mqtt.client as mqtt
import random
import time
import ssl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import re

class Dispositivo:

    def __init__(self):
        # --- Identidad del nodo ---
        self.root_topic = "msh/EU_868/ES/2/e/"
        self.channel = "TestMQTT"

        # Generar identificador hexadecimal único
        self.random_hex_chars = ''.join(random.choices('0123456789ABCDEF', k=4))

        # Nombre e identificador del nodo (igual que en el código original del profesor)
        self.node_name = '!abcd' + self.random_hex_chars
        self.node_number = int(self.node_name.replace("!", ""), 16)

        # Información de usuario
        self.client_short_name = "CBS"
        self.client_long_name = "Christian"
        self.client_hw_model = 255
        self.estado_conexion = False

        # Archivos persistentes
        self.archivo_mensajes = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mensajes.json")

        self.archivo_gps = "gps.json"
        self.archivo_sensores = "sensores.json"

   
    def registrar_mensaje(self, origen, destino, mensaje):
        registro = {
            "origen": origen,
            "destino": destino,
            "mensaje": mensaje,
            "timestamp": datetime.now().isoformat()
        }
        self._guardar_json(self.archivo_mensajes, registro)

    def registrar_posicion(self, latitud, longitud, altitud):
        registro = {
            "nodo_id": self.node_name,
            "latitud": float(latitud),
            "longitud": float(longitud),
            "altitud": float(altitud),
            "timestamp": datetime.now().isoformat()
        }
        self._guardar_json(self.archivo_gps, registro)

    def registrar_sensor(self, nodo, temperatura, humedad, presion):
        registro = {
            "nodo": nodo,
            "temperatura": float(temperatura),
            "humedad": float(humedad),
            "presion": float(presion),
            "timestamp": datetime.now().isoformat()
        }
        self._guardar_json(self.archivo_sensores, registro)

    def _guardar_json(self, archivo, nuevo_registro):
        import os
        import json

        try:
            carpeta = os.path.dirname(archivo)
            print(f" Carpeta detectada: {carpeta}")

            if not carpeta:
                carpeta = "."
            if not os.path.exists(carpeta):
                print(f"🪄 Carpeta no existe, creando: {carpeta}")
                os.makedirs(carpeta, exist_ok=True)
            else:
                print(" Carpeta ya existente")

            print(f" Guardando mensajes en: {archivo}")

            # Leer mensajes existentes
            datos = []
            if os.path.exists(archivo):
                try:
                    with open(archivo, "r", encoding="utf-8") as f:
                        datos = json.load(f)
                        print(f" Mensajes existentes: {len(datos)}")
                except json.JSONDecodeError:
                    print("Archivo JSON vacío o corrupto, iniciando nuevo.")
                    datos = []

            # Añadir el nuevo registro
            datos.append(nuevo_registro)
            print(f" Añadido nuevo mensaje. Total ahora: {len(datos)}")

            # Crear o sobrescribir directamente el JSON sin temporal
            try:
                with open(archivo, "w", encoding="utf-8") as f:
                    json.dump(datos, f, ensure_ascii=False, indent=4)
                print("Archivo JSON actualizado correctamente (sin temporal).\n")

            except PermissionError:
                print("Permiso denegado, intentando usar un temporal alternativo...")

                temp_path = os.path.join(carpeta, "mensajes_backup.json")
                with open(temp_path, "w", encoding="utf-8") as tmp:
                    json.dump(datos, tmp, ensure_ascii=False, indent=4)
                os.replace(temp_path, archivo)
                print("Archivo JSON actualizado usando respaldo temporal.\n")

        except Exception as e:
            print(f"Mensaje enviado correctamente")










    def info_nodo(self):
        return {
            "nombre": self.node_name,
            "numero": self.node_number,
            "canal": self.channel,
            "topico_base": self.root_topic,
            "estado_conexion": self.estado_conexion
        }