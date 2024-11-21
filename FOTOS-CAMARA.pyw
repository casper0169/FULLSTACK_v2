import cv2
import os
import sys
import time
from datetime import datetime
import ctypes
import threading

# Ruta base del directorio donde se encuentra el script
base_path = os.path.abspath(os.path.dirname(__file__))

# Cambiar al directorio del script
os.chdir(base_path)

# Nombre de la carpeta para guardar capturas
folder_name = "FOTOS-CAMARA-5seg"

# Crear la carpeta FOTOS-CAMARA-5seg en modo oculto si no existe
folder_path = os.path.join(base_path, folder_name)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    # Establece el atributo de la carpeta como oculta (solo en Windows)
    if os.name == 'nt':  # Solo se aplica en Windows
        ctypes.windll.kernel32.SetFileAttributesW(folder_path, 0x02)

# Comprobar si hay cámaras disponibles
def check_camera():
    # Intentar acceder a la primera cámara
    temp_cap = cv2.VideoCapture(0)
    if not temp_cap.isOpened():
        return False
    temp_cap.release()
    return True

# Si no hay cámaras disponibles, el script no se ejecuta
if not check_camera():
    sys.exit(0)

# Función para capturar imágenes
def capture_images():
    # Abre la cámara (0 es el índice por defecto de la primera cámara)
    cap = cv2.VideoCapture(0)

    # Verifica si la cámara se ha abierto correctamente
    if not cap.isOpened():
        sys.exit(0)

    # Inicia la captura de fotogramas
    while True:
        # Captura un fotograma de la cámara
        ret, frame = cap.read()

        # Si no se captura correctamente, termina el script
        if not ret:
            break

        # Obtiene la fecha y hora actual
        now = datetime.now()
        # Formato de la fecha y hora
        timestamp = now.strftime("%d-%m-%Y-%H-%M-%S")
        
        # Define el nombre del archivo para guardar la foto
        screenshot_filename = os.path.join(folder_path, f"fc-{timestamp}.jpg")
        
        # Guarda la imagen en la carpeta FOTOS-CAMARA-5seg
        cv2.imwrite(screenshot_filename, frame)

        # Espera 5 segundos antes de capturar otra imagen
        time.sleep(5)

    # Libera la cámara
    cap.release()

# Ejecutar la captura en un hilo para que el script se ejecute en segundo plano
capture_thread = threading.Thread(target=capture_images)
capture_thread.daemon = True  # Esto permite que el hilo se cierre automáticamente cuando termine el script
capture_thread.start()

# Dejar que el script se ejecute sin necesidad de mostrar nada en pantalla
capture_thread.join()
