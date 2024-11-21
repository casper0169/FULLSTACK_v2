import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import os
from datetime import datetime

# Obtener el directorio donde está guardado el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Diccionario para almacenar los subprocesos de scripts en ejecución
running_processes = {}

# Función para ejecutar un script y mostrar el resultado
def run_script(script_name):
    try:
        subprocess.run(['pythonw', script_name], check=True)
        log_message(f"{script_name} se ejecutó correctamente.")
    except subprocess.CalledProcessError as e:
        log_message(f"Error al ejecutar {script_name}: {e}")

# Función para iniciar un script y guardarlo en los procesos en ejecución
def start_script(script_name):
    if script_name in running_processes:
        log_message(f"{script_name} ya está en ejecucion.")
    else:
        process = subprocess.Popen(['pythonw', script_name])
        running_processes[script_name] = process
        log_message(f"{script_name} se ha iniciado correctamente.")

# Función para detener un script en ejecución
def stop_script(script_name):
    process = running_processes.pop(script_name, None)
    if process and process.poll() is None:
        process.terminate()
        log_message(f"{script_name} se ha detenido.")
    else:
        log_message(f"{script_name} no está en ejecucion.")

# Función para cerrar el programa
def close_program():
    root.destroy()

# Función para mostrar el menú de scripts después de la pantalla de bienvenida
def show_menu():
    welcome_frame.pack_forget()
    menu_frame.pack(fill="both", expand=True)

# Función para regresar a la pantalla de bienvenida desde el menú
def go_back_to_welcome():
    menu_frame.pack_forget()
    welcome_frame.pack(fill="both", expand=True)

# Función para actualizar la fecha y hora en la cabecera
def update_datetime(label):
    current_datetime = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    label.config(text=f"Directorio: {script_dir} | {current_datetime}")
    label.after(1000, update_datetime, label)  # Actualizar cada segundo

# Función para registrar los avisos en la segunda mitad de la pantalla
def log_message(message):
    current_datetime = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    log_text.insert(tk.END, f"{current_datetime} - {message}\n")
    log_text.see(tk.END)

# Función para mostrar las instrucciones
def show_instructions():
    try:
        with open("INSTRUCCIONES.txt", "r") as f:
            instructions = f.read()
        instructions_window = tk.Toplevel(root)
        instructions_window.title("Instrucciones")
        instructions_window.geometry("600x400")
        instructions_text = tk.Text(instructions_window, font=("Courier", 10), fg="white", bg="black", wrap="word", height=15, width=70)
        instructions_text.insert(tk.END, instructions)
        instructions_text.config(state=tk.DISABLED)  # Hacer que el texto sea solo de lectura
        instructions_text.pack(padx=10, pady=10, fill="both", expand=True)
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo INSTRUCCIONES.txt no se encuentra.")

# Función para mostrar la ventana emergente al pulsar SALIR
def show_exit_popup():
    exit_popup = tk.Toplevel(root)
    exit_popup.title("¡Esperamos que vuelvas pronto!")
    exit_popup.geometry("400x200")  # Tamaño de la ventana emergente
    exit_popup.configure(bg="black")

    exit_message = tk.Label(exit_popup, text="¡Esperamos que vuelvas pronto!", font=("Courier", 14, "bold"), fg="lime", bg="black")
    exit_message.pack(pady=50)

    accept_button = tk.Button(exit_popup, text="ACEPTAR", font=("Courier", 12), fg="black", bg="yellow", command=close_program)
    accept_button.pack()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Menú de Scripts - Hacker Mode")
root.geometry("950x500")  # Tamaño inicial de la ventana
root.configure(bg="black")

# Maximizar ventana al iniciar
root.state('zoomed')

# Estilo de hacker
text_color = "lime"
bg_color = "black"
font_style = ("Courier", 10, "bold")

# Pantalla de bienvenida
welcome_frame = tk.Frame(root, bg=bg_color)
welcome_frame.pack(fill="both", expand=True)

# Cabecera de bienvenida con el directorio y fecha/hora
welcome_header = tk.Label(welcome_frame, font=("Courier", 12, "italic"), fg="white", bg=bg_color)
welcome_header.pack(pady=30)  # Espacio de 2 cm desde la parte superior
update_datetime(welcome_header)  # Actualizar la fecha y hora en la cabecera de bienvenida

# Texto principal de bienvenida
title_label = tk.Label(welcome_frame, text="""¡Hola, mundo!
Existen numerosas leyes nacionales e internacionales en las que se penan los delitos informáticos. Si tienes dudas consulta las leyes y regulaciones de tu país para evitar cometer un delito. Esta suite de programas se ha desarrollado de manera independiente sin fines lucrativos y en un entorno controlado. Si tienes cualquier duda antes de empezar se recomienda leer las -> INSTRUCCIONES <-

© Propiedad de I HACK, YOU WIN creado por el usuario c@$p€r ©""",
                       font=("Courier", 12), fg=text_color, bg=bg_color, wraplength=650, justify="center")
title_label.pack(pady=20)

# Botón de Instrucciones en la pantalla de bienvenida
instructions_button = tk.Button(welcome_frame, text="INSTRUCCIONES", font=font_style, fg="black", bg="yellow", command=show_instructions)
instructions_button.pack(pady=10)

continue_button = tk.Button(welcome_frame, text="CONTINUAR", font=font_style, fg="white", bg="green", command=show_menu)
continue_button.pack(pady=10)

exit_button = tk.Button(welcome_frame, text="SALIR", font=font_style, fg="white", bg="red", command=show_exit_popup)
exit_button.pack(pady=10)

# Frame del menú de scripts
menu_frame = tk.Frame(root, bg=bg_color)

# Cabecera con el directorio y la fecha/hora en el menú
header_label = tk.Label(menu_frame, font=("Courier", 12, "italic"), fg="white", bg=bg_color)
header_label.pack(pady=30)  # Espacio de 2 cm desde la parte superior
update_datetime(header_label)

# Texto introductorio en el menú de opciones
intro_label = tk.Label(menu_frame, text="¿Que quieres hacer?", font=("Courier", 12, "bold"), fg="white", bg=bg_color)
intro_label.pack(pady=10)

# Crear contenedor para los botones de ejecución simple con botón INICIAR
frame_simple = tk.Frame(menu_frame, bg=bg_color)
frame_simple.pack(pady=20)

# Crear opciones de ejecución simple con botón INICIAR
scripts = [
    ("1", "Instalacion COTS previos", "COTS.pyw"),
    ("2", "Modo Sigilo", "SIGILO.pyw"),
    ("3", "Obtencion de claves wifi", "CLAVES-WIFI.pyw"),
    ("4", "Recoleccion de directorios", "DIRECTORIOS.pyw"),
]

for idx, description, script in scripts:
    label = tk.Label(frame_simple, text=f"{idx} - {description}", font=font_style, fg=text_color, bg=bg_color)
    label.grid(row=int(idx)-1, column=0, sticky="w", padx=5, pady=3)

    btn_start = tk.Button(frame_simple, text="INICIAR", font=font_style, fg="black", bg="yellow",
                          command=lambda s=script: threading.Thread(target=run_script, args=(s,)).start())
    btn_start.grid(row=int(idx)-1, column=1, padx=10, pady=3, sticky="w")

# Crear contenedor para los botones de INICIAR y DETENER de las opciones avanzadas
frame_control = tk.Frame(menu_frame, bg=bg_color)
frame_control.pack(pady=20)

# Crear opciones de ejecución con INICIAR y DETENER
start_stop_scripts = [
    ("5", "Capturas de la pantalla", "CAPTURAS-PANTALLA.pyw"),
    ("6", "Video de la pantalla", "CAPTURAS-PANTALLA.pyw"),
    ("7", "Fotos de la camara", "FOTOS-CAMARA.pyw"),
    ("8", "Video de la camara", "VIDEOS-CAMARA.pyw"),
    ("9", "Grabacion de audio", "AUDIO.pyw"),
    ("10", "Registro de teclas", "PULSACION-TECLADO.pyw"),
    ("11", "Ubicacion segun IPv4 publica", "UBICACION-IPV4-PUBLICA.pyw"),
]

for idx, description, script in start_stop_scripts:
    label = tk.Label(frame_control, text=f"{idx} - {description}", font=font_style, fg=text_color, bg=bg_color)
    label.grid(row=int(idx)-4, column=0, sticky="w", padx=5, pady=3)
    
    btn_start = tk.Button(frame_control, text="INICIAR", font=font_style, fg="black", bg="yellow",
                          command=lambda s=script: start_script(s))
    btn_start.grid(row=int(idx)-4, column=1, padx=10, pady=3, sticky="w")
    
    btn_stop = tk.Button(frame_control, text="DETENER", font=font_style, fg="white", bg="red",
                         command=lambda s=script: stop_script(s))
    btn_stop.grid(row=int(idx)-4, column=2, padx=10, pady=3, sticky="w")

# Título de la sección de registros de avisos
log_title = tk.Label(menu_frame, text="Registro de los avisos", font=("Courier", 12, "bold"), fg="white", bg=bg_color)
log_title.pack(pady=5)

# Área de registros de avisos con barra de desplazamiento
log_frame = tk.Frame(menu_frame, bg=bg_color)
log_frame.pack(fill="both", expand=True, padx=20)

scrollbar = tk.Scrollbar(log_frame)
scrollbar.pack(side="right", fill="y")

log_text = tk.Text(log_frame, font=("Courier", 10), fg="white", bg="black", wrap="word", height=16, yscrollcommand=scrollbar.set)
log_text.pack(pady=10, padx=10, fill="both", expand=True)
scrollbar.config(command=log_text.yview)

# Botones "ATRÁS" y "FINALIZAR" al pie de la pantalla
bottom_frame = tk.Frame(menu_frame, bg=bg_color)
bottom_frame.pack(side="bottom", fill="x", pady=20)

back_button = tk.Button(bottom_frame, text="ATRÁS", font=font_style, fg="white", bg="red", command=go_back_to_welcome)
back_button.pack(side="left", padx=10)

finish_button = tk.Button(bottom_frame, text="FINALIZAR", font=font_style, fg="white", bg="green")
finish_button.pack(side="right", padx=10)

from tkinter import ttk
import time

# Función para ejecutar el script con barra de progreso opción 3
def run_script_with_progress(script_name):
    start_time = time.time()
    try:
        # Iniciar el script
        process = subprocess.Popen(['pythonw', script_name])

        # Crear barra de progreso en el registrador de eventos
        progress_bar = ttk.Progressbar(log_frame, orient="horizontal", length=300, mode="indeterminate")
        progress_bar.pack(pady=10)
        log_text.insert(tk.END, "Iniciando ejecución... Espere...\n")
        log_text.see(tk.END)

        # Comenzar la barra de progreso
        progress_bar.start()

        # Chequear el tiempo de ejecución y mostrar la barra de progreso si pasa 2 segundos
        while process.poll() is None:
            elapsed_time = time.time() - start_time
            if elapsed_time > 2:  # Si pasa más de 2 segundos
                log_text.insert(tk.END, "Ejecutando...\n")
                log_text.see(tk.END)
            time.sleep(0.5)  # Esperar medio segundo para no sobrecargar el proceso

        # Esperar a que termine el proceso
        process.wait()

        # Finalizar la barra de progreso y mostrar el resultado
        progress_bar.stop()
        progress_bar.pack_forget()  # Eliminar la barra de progreso cuando termine

        if process.returncode == 0:
            log_message(f"{script_name} se ejecutó correctamente.")
        else:
            log_message(f"Error al ejecutar {script_name}.")

    except subprocess.CalledProcessError as e:
        log_message(f"Error al ejecutar {script_name}: {e}")

# Función para mostrar los mensajes en el log
def log_message(message):
    current_datetime = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    log_text.insert(tk.END, f"{current_datetime} - {message}\n")
    log_text.see(tk.END)

# Modificar la llamada al script para usar la nueva función
for idx, description, script in scripts:
    label = tk.Label(frame_simple, text=f"{idx} - {description}", font=font_style, fg=text_color, bg=bg_color)
    label.grid(row=int(idx)-1, column=0, sticky="w", padx=5, pady=3)

    btn_start = tk.Button(frame_simple, text="INICIAR", font=font_style, fg="black", bg="yellow",
                          command=lambda s=script: threading.Thread(target=run_script_with_progress, args=(s,)).start())
    btn_start.grid(row=int(idx)-1, column=1, padx=10, pady=3, sticky="w")

from tkinter import ttk
import time

# Función para ejecutar el script con barra de progreso de las opciones: 4,5,6,7,8 y 9
def run_script_with_progress(script_name):
    start_time = time.time()
    try:
        # Iniciar el script
        process = subprocess.Popen(['pythonw', script_name])

        # Crear barra de progreso en el registrador de eventos
        progress_bar = ttk.Progressbar(log_frame, orient="horizontal", length=300, mode="indeterminate")
        progress_bar.pack(pady=10)
        log_text.insert(tk.END, "Iniciando ejecución... Espere...\n")
        log_text.see(tk.END)

        # Comenzar la barra de progreso
        progress_bar.start()

        # Chequear el tiempo de ejecución y mostrar la barra de progreso si pasa 2 segundos
        while process.poll() is None:
            elapsed_time = time.time() - start_time
            if elapsed_time > 2:  # Si pasa más de 2 segundos
                log_text.insert(tk.END, "Ejecutando...\n")
                log_text.see(tk.END)
            time.sleep(0.5)  # Esperar medio segundo para no sobrecargar el proceso

        # Esperar a que termine el proceso
        process.wait()

        # Finalizar la barra de progreso y mostrar el resultado
        progress_bar.stop()
        progress_bar.pack_forget()  # Eliminar la barra de progreso cuando termine

        if process.returncode == 0:
            log_message(f"{script_name} se ejecutó correctamente.")
        else:
            log_message(f"Error al ejecutar {script_name}.")

    except subprocess.CalledProcessError as e:
        log_message(f"Error al ejecutar {script_name}: {e}")

# Función para iniciar el script y mostrar la barra de progreso
def start_script_with_progress(script_name):
    # Crear barra de progreso
    progress_bar = ttk.Progressbar(log_frame, orient="horizontal", length=300, mode="indeterminate")
    progress_bar.pack(pady=10)
    progress_bar.start()

    # Almacenamos la barra de progreso y el proceso en ejecución para detenerlos posteriormente
    running_processes[script_name] = {'process': subprocess.Popen(['pythonw', script_name]), 'progress_bar': progress_bar}

    log_text.insert(tk.END, f"{script_name} se ha iniciado... Espere...\n")
    log_text.see(tk.END)

# Función para detener el script y la barra de progreso
def stop_script_with_progress(script_name):
    if script_name in running_processes:
        process_info = running_processes[script_name]
        process = process_info['process']
        progress_bar = process_info['progress_bar']

        # Detener el proceso si está en ejecución
        if process.poll() is None:
            process.terminate()
            log_message(f"{script_name} se ha detenido.")
            progress_bar.stop()  # Detener la barra de progreso
            progress_bar.pack_forget()  # Eliminar la barra de progreso
        else:
            log_message(f"{script_name} no estaba en ejecución.")

        # Eliminar del diccionario de procesos en ejecución
        del running_processes[script_name]
    else:
        log_message(f"{script_name} no está en ejecución.")

# Función para registrar los mensajes en el log
def log_message(message):
    current_datetime = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    log_text.insert(tk.END, f"{current_datetime} - {message}\n")
    log_text.see(tk.END)

# Modificar el comportamiento de las opciones 5-11
start_stop_scripts = [
    ("5", "Capturas de la pantalla", "CAPTURAS-PANTALLA.pyw"),
    ("6", "Video de la pantalla", "CAPTURAS-PANTALLA.pyw"),
    ("7", "Fotos de la camara", "FOTOS-CAMARA.pyw"),
    ("8", "Video de la camara", "VIDEOS-CAMARA.pyw"),
    ("9", "Grabacion de audio", "AUDIO.pyw"),
    ("10", "Registro de teclas", "PULSACION-TECLADO.pyw"),
    ("11", "Ubicacion segun IPv4 publica", "UBICACION-IPV4-PUBLICA.pyw"),
]

for idx, description, script in start_stop_scripts:
    label = tk.Label(frame_control, text=f"{idx} - {description}", font=font_style, fg=text_color, bg=bg_color)
    label.grid(row=int(idx)-4, column=0, sticky="w", padx=5, pady=3)
    
    # Botón INICIAR
    btn_start = tk.Button(frame_control, text="INICIAR", font=font_style, fg="black", bg="yellow",
                          command=lambda s=script: start_script_with_progress(s))
    btn_start.grid(row=int(idx)-4, column=1, padx=10, pady=3, sticky="w")
    
    # Botón DETENER
    btn_stop = tk.Button(frame_control, text="DETENER", font=font_style, fg="white", bg="red",
                         command=lambda s=script: stop_script_with_progress(s))
    btn_stop.grid(row=int(idx)-4, column=2, padx=10, pady=3, sticky="w")

# Función para mostrar la ventana emergente al pulsar FINALIZAR
def show_finish_popup():
    # Crear ventana emergente con estilo hacker
    finish_popup = tk.Toplevel(root)
    finish_popup.title("Operación finalizada")
    finish_popup.geometry("400x200")  # Tamaño de la ventana emergente
    finish_popup.configure(bg="black")

    # Mensaje en estilo hacker
    finish_message = tk.Label(finish_popup, text="Se han guardado los registros.\n¡Esperamos que vuelva pronto!",
                              font=("Courier", 14, "bold"), fg="lime", bg="black")
    finish_message.pack(pady=50)

    # Botón para aceptar y cerrar la ventana
    accept_button = tk.Button(finish_popup, text="ACEPTAR", font=("Courier", 12), fg="black", bg="yellow", command=lambda: [save_and_hide_logs(), close_program()])
    accept_button.pack()

# Función para guardar los registros en una carpeta oculta
def save_and_hide_logs():
    # Crear la carpeta oculta
    hidden_folder_path = os.path.join(script_dir, ".Registros")
    os.makedirs(hidden_folder_path, exist_ok=True)  # Crear la carpeta si no existe
    
    # Crear el archivo de registros
    hidden_file_path = os.path.join(hidden_folder_path, "Registros.txt")
    
    # Obtener los registros del área de texto de log
    logs_content = log_text.get(1.0, tk.END)
    
    with open(hidden_file_path, "w") as file:
        # Guardar los registros en el archivo
        file.write("Registros de las actividades:\n")
        file.write(logs_content)  # Escribir el contenido completo del log
    
    # Hacer la carpeta oculta en Windows
    if os.name == "nt":  # Si es Windows
        subprocess.run(["attrib", "+h", hidden_folder_path], check=True)

# Función para mostrar la ventana emergente al pulsar FINALIZAR
def show_finish_popup():
    # Crear ventana emergente con estilo hacker
    finish_popup = tk.Toplevel(root)
    finish_popup.title("Operación finalizada")
    finish_popup.geometry("400x200")  # Tamaño de la ventana emergente
    finish_popup.configure(bg="black")

    # Mensaje en estilo hacker
    finish_message = tk.Label(finish_popup, text="Se han guardado los registros.\n¡Esperamos que vuelva pronto!",
                              font=("Courier", 14, "bold"), fg="lime", bg="black")
    finish_message.pack(pady=50)

    # Botón para aceptar y cerrar la ventana
    accept_button = tk.Button(finish_popup, text="ACEPTAR", font=("Courier", 12), fg="black", bg="yellow", command=lambda: [save_and_hide_logs(), close_program()])
    accept_button.pack()

# Asignar la función al botón FINALIZAR
finish_button.config(command=show_finish_popup)

# Modificar la función run_script_with_progress
def run_script_with_progress(script_name):
    start_time = time.time()
    try:
        # Iniciar el script
        process = subprocess.Popen(['pythonw', script_name])

        # Establecer el tiempo total estimado (en segundos) para el proceso
        total_estimated_time = 70  # Establece un valor de tiempo estimado (ejemplo: 70 segundos)

        # Crear barra de progreso en el registrador de eventos
        progress_bar = ttk.Progressbar(log_frame, orient="horizontal", length=300, mode="indeterminate")
        progress_bar.pack(pady=10)
        log_text.insert(tk.END, "Iniciando ejecución... Espere...\n")
        log_text.see(tk.END)

        # Comenzar la barra de progreso
        progress_bar.start()

        # Mostrar el tiempo restante de forma descendente
        while process.poll() is None:
            elapsed_time = time.time() - start_time
            remaining_time = total_estimated_time - elapsed_time

            if remaining_time > 0:  # Si aún queda tiempo
                log_text.insert(tk.END, f"Tiempo restante: {remaining_time:.1f} segundos...\n")
                log_text.see(tk.END)
            else:
                log_text.insert(tk.END, "Ejecutando...\n")
                log_text.see(tk.END)

            time.sleep(0.5)  # Esperar medio segundo para no sobrecargar el proceso

        # Esperar a que termine el proceso
        process.wait()

        # Finalizar la barra de progreso y mostrar el resultado
        progress_bar.stop()
        progress_bar.pack_forget()  # Eliminar la barra de progreso cuando termine

        if process.returncode == 0:
            log_message(f"{script_name} se ejecutó correctamente.")
        else:
            log_message(f"Error al ejecutar {script_name}.")

    except subprocess.CalledProcessError as e:
        log_message(f"Error al ejecutar {script_name}: {e}")

import os
import zipfile
import shutil
import platform
from datetime import datetime

# Función para obtener el nombre del archivo ZIP (incluir un punto al inicio para hacerlo oculto en Linux/macOS)
def obtener_nombre_zip():
    team_name = platform.node()  # Nombre del equipo
    current_date = datetime.now().strftime("%d-%m-%Y")  # Fecha en formato dia-mes-año
    zip_filename = f".PENTESTING-{team_name}-{current_date}.zip"  # Agregar un punto al inicio para hacerlo oculto
    return zip_filename

# Función para crear el archivo ZIP y comprimir las carpetas
def compress_folders():
    # Obtener el nombre del archivo zip con el nombre del equipo y la fecha
    zip_filename = os.path.join(script_dir, obtener_nombre_zip())  # Definir el nombre del archivo zip
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Recorrer todas las carpetas en el directorio
        for root, dirs, files in os.walk(script_dir):
            for dir in dirs:
                folder_path = os.path.join(root, dir)
                # Excluir la carpeta PENTESTING-<nombre-del-equipo>-<dia-mes-año>.zip de la compresión
                if folder_path != zip_filename:
                    # Agregar la carpeta al archivo zip
                    zipf.write(folder_path, os.path.relpath(folder_path, script_dir))
    log_message(f"Se han comprimido las carpetas en: {zip_filename}")
    
    # Si estamos en Windows, ocultar el archivo utilizando el comando 'attrib'
    if platform.system() == "Windows":
        os.system(f'attrib +h "{zip_filename}"')

# Función para eliminar todas las carpetas excepto la que acabamos de crear
def eliminar_carpetas_except_zip():
    zip_filename = obtener_nombre_zip()  # Obtener el nombre del archivo ZIP
    for root, dirs, files in os.walk(script_dir, topdown=False):
        for dir in dirs:
            # Excluir la carpeta con el nombre zip
            folder_path = os.path.join(root, dir)
            if folder_path != os.path.join(script_dir, zip_filename):
                try:
                    shutil.rmtree(folder_path)  # Eliminar la carpeta
                    log_message(f"Carpeta '{folder_path}' eliminada.")
                except Exception as e:
                    log_message(f"Error al eliminar la carpeta '{folder_path}': {e}")

# Función para cerrar el programa después de comprimir y eliminar carpetas
def close_program():
    compress_folders()  # Llamamos a la función para comprimir las carpetas
    eliminar_carpetas_except_zip()  # Llamamos a la función para eliminar carpetas
    root.quit()

# Actualización de la función para mostrar el popup de salida
def show_exit_popup():
    exit_popup = tk.Toplevel(root)
    exit_popup.title("¡Esperamos que vuelvas pronto!")
    exit_popup.geometry("400x200")
    exit_popup.configure(bg="black")

    exit_message = tk.Label(exit_popup, text="¡Esperamos que vuelvas pronto!", font=("Courier", 14, "bold"), fg="lime", bg="black")
    exit_message.pack(pady=50)

    accept_button = tk.Button(exit_popup, text="ACEPTAR", font=("Courier", 12), fg="black", bg="yellow", command=close_program)
    accept_button.pack()

# Ejecutar la aplicación
root.mainloop()
