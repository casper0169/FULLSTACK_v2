import os
import requests
import tkinter as tk
import time
import platform

# Función para crear la carpeta oculta
def crear_carpeta_oculta():
    carpeta = "CambiosIP"
    
    # Crear la carpeta en el directorio actual si no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
        
        # Hacerla oculta según el sistema operativo
        if platform.system() == "Windows":
            os.system(f"attrib +h {carpeta}")  # Hacerla oculta en Windows
        elif platform.system() in ["Linux", "Darwin"]:  # Linux/macOS
            os.rename(carpeta, f".{carpeta}")  # Añadir punto al inicio para ocultarla
    
    return carpeta

# Función para obtener la IP pública
def obtener_ip_publica():
    url = "https://httpbin.org/ip"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            ip_publica = response.json()['origin']
            return ip_publica
        else:
            return None
    except requests.RequestException:
        return None

# Crear la ventana emergente con estilo de consola
def mostrar_ventana_ip():
    ip_anterior = None
    
    # Crear la ventana
    ventana = tk.Tk()
    ventana.title("Hacker Terminal")
    
    # Configurar la ventana
    ventana.geometry("500x300")
    ventana.configure(bg="black")
    
    # Crear los widgets de texto para mostrar el estado, la IP y la ubicación
    estado_label = tk.Label(ventana, text="Conectando...", font=("Courier", 16), fg="lime", bg="black")
    estado_label.pack(pady=10)
    
    ip_label = tk.Label(ventana, text="Esperando IP...", font=("Courier", 14), fg="lime", bg="black")
    ip_label.pack(pady=10)
    
    ubicacion_label = tk.Label(ventana, text="", font=("Courier", 12), fg="lime", bg="black", wraplength=480, justify="left")
    ubicacion_label.pack(pady=10)
    
    # Función para obtener la ubicación basada en la IP pública
    def obtener_ubicacion(ip):
        url = f"http://ip-api.com/json/{ip}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                datos = response.json()
                if datos["status"] == "success":
                    return {
                        "país": datos["country"],
                        "región": datos["regionName"],
                        "ciudad": datos["city"],
                        "proveedor": datos["isp"]
                    }
                else:
                    return None
            else:
                return None
        except requests.RequestException:
            return None
    
    # Función para actualizar la ventana cada 2 segundos
    def actualizar_ip():
        nonlocal ip_anterior
        
        ip_actual = obtener_ip_publica()
        carpeta = crear_carpeta_oculta()
        archivo_path = os.path.join(carpeta, "CambiosIP.txt")
        
        if ip_actual:
            estado_label.config(text="Conectado", fg="green")
            if ip_actual != ip_anterior:  # Solo actualizar si la IP es diferente
                ip_label.config(text=f"IP Pública: {ip_actual}")
                ip_anterior = ip_actual  # Actualizar la IP anterior
                
                # Obtener la ubicación y mostrarla
                ubicacion = obtener_ubicacion(ip_actual)
                if ubicacion:
                    ubicacion_texto = (f"Ubicación:\n"
                                       f"  País: {ubicacion['país']}\n"
                                       f"  Región: {ubicacion['región']}\n"
                                       f"  Ciudad: {ubicacion['ciudad']}\n"
                                       f"  Proveedor: {ubicacion['proveedor']}")
                    ubicacion_label.config(text=ubicacion_texto)
                else:
                    ubicacion_label.config(text="No se pudo determinar la ubicación")
                
                # Guardar la IP y ubicación en el archivo
                with open(archivo_path, "a") as archivo:
                    archivo.write(f"IP pública: {ip_actual} - Detectada a las: {time.ctime()}\n")
                    if ubicacion:
                        archivo.write(f"  Ubicación: {ubicacion_texto}\n")
        else:
            estado_label.config(text="No conectado", fg="red")
        
        ventana.after(2000, actualizar_ip)  # Volver a llamar a esta función después de 2 segundos
    
    # Iniciar la actualización de la IP
    actualizar_ip()
    
    # Mostrar la ventana
    ventana.mainloop()

# Mostrar la ventana
mostrar_ventana_ip()
