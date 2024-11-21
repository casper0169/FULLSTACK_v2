import os
import subprocess
import time
import socket
import getpass
from pathlib import Path

# Función para crear una carpeta oculta usando attrib +h
def create_hidden_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        # Aplicar atributo de ocultar la carpeta
        subprocess.run(f'attrib +h "{folder_path}"', shell=True)

# Función para obtener la información del sistema
def collect_system_info(output_file):
    with open(output_file, 'a') as f:
        # Nombre del ordenador
        f.write("Nombre del ordenador:\n")
        f.write(socket.gethostname() + "\n\n")

        # Información del sistema
        f.write("Información del sistema:\n")
        system_info = subprocess.run('systeminfo', capture_output=True, text=True, shell=True)
        f.write(system_info.stdout + "\n")

        # Tarjetas de red activas
        f.write("Tarjetas de red activas:\n")
        getmac_info = subprocess.run('getmac', capture_output=True, text=True, shell=True)
        f.write(getmac_info.stdout + "\n")

        # Configuración de red
        f.write("Configuración de red:\n")
        ipconfig_info = subprocess.run('ipconfig /all', capture_output=True, text=True, shell=True)
        f.write(ipconfig_info.stdout + "\n")

        # Nombres de usuarios y roles
        f.write("Nombres de usuarios y roles:\n")
        net_user_info = subprocess.run('net user', capture_output=True, text=True, shell=True)
        f.write(net_user_info.stdout + "\n")

        # Permisos de usuarios
        net_user_list = subprocess.run('net user', capture_output=True, text=True, shell=True)
        for line in net_user_list.stdout.splitlines():
            if line.strip():  # Filtra líneas vacías
                f.write(f"Permisos del usuario {line.strip()}:\n")
                user_info = subprocess.run(f'net user {line.strip()}', capture_output=True, text=True, shell=True)
                f.write(user_info.stdout + "\n")

# Función para obtener la letra de la unidad principal
def get_main_drive():
    # Buscar la unidad que contiene la carpeta "Windows" (suponiendo que es la unidad principal)
    for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        drive_path = f"{drive}:\\"
        if os.path.exists(os.path.join(drive_path, 'Windows')):
            return drive_path
    return None

# Función para generar el árbol de directorios de la unidad con formato adecuado
def generate_directory_tree(drive, output_file):
    tree_command = f'tree "{drive}" /f /a'  # /a es para usar caracteres ASCII (más adecuado para archivos)
    tree_info = subprocess.run(tree_command, capture_output=True, text=True, shell=True)
    
    with open(output_file, 'a') as f:
        f.write(f"Árbol de directorios de {drive}:\n")
        f.write(tree_info.stdout + "\n")

# Obtener la ruta actual del script
script_dir = os.path.dirname(os.path.realpath(__file__))
folder_name = f'informacion-{socket.gethostname()}'  # Carpeta oculta sin punto
folder_path = os.path.join(script_dir, folder_name)

# Archivo de salida
output_file = os.path.join(folder_path, f'informacion-{socket.gethostname()}.txt')

# Crear la carpeta oculta si no existe
create_hidden_folder(folder_path)

# Bucle para recopilar la información del sistema y guardarla en el archivo
while True:
    # Obtener la letra de la unidad principal (disco local)
    main_drive = get_main_drive()
    if main_drive:
        # Recolectar información y guardarla en el archivo
        collect_system_info(output_file)
        generate_directory_tree(main_drive, output_file)
        break  # Una vez completada la recolección, salir del bucle

    # Esperar 5 segundos antes de volver a comprobar
    time.sleep(5)
