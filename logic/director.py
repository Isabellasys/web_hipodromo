import paho.mqtt.client as mqtt
import time
import random
import json

BROKER = "localhost"
TOPIC = "carrera/caballos"
# Nombres exactos de tu HTML
CABALLOS = ["TRUENO", "RELÁMPAGO", "PEGASO", "TORNADO", "CENTELLA", "COMETA"]

client = mqtt.Client()

def ejecutar():
    try:
        client.connect(BROKER, 1883, 60)
        while True:
            print("⏳ Sincronizando... Salida en 20 segundos.")
            for nombre in CABALLOS:
                client.publish(TOPIC, json.dumps({"caballo": nombre, "pos": 0}))
            time.sleep(20)

            print("🚀 ¡CARRERA EN CURSO!")
            posiciones = {n: 0 for n in CABALLOS}
            activa = True
            while activa:
                for n in CABALLOS:
                    posiciones[n] += random.uniform(1, 4)
                    client.publish(TOPIC, json.dumps({"caballo": n, "pos": posiciones[n]}))
                    if posiciones[n] >= 100:
                        print(f"🏆 Ganó {n}")
                        client.publish(TOPIC, json.dumps({"caballo": n, "pos": 100}))
                        activa = False
                        break
                time.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejecutar()
