# core/audio_listener.py

import speech_recognition as sr
from PyQt6.QtCore import QObject, pyqtSignal

class AudioListener(QObject):
    """
    Escucha el micrófono en segundo plano, convierte la voz a texto y
    emite señales cuando detecta frases clave.
    """
    # Nueva señal para la frase de activación
    activation_phrase_detected = pyqtSignal()
    
    # Mantenemos la señal anterior por si la quieres usar para otra cosa
    snap_detected = pyqtSignal() 

    def __init__(self, activation_phrase="sofi activate"):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.ACTIVATION_PHRASE = activation_phrase.lower()
        self.running = True

    def run(self):
        print("Ajustando para ruido ambiental...")
        with self.microphone as source:
            # NUEVO: Ajusta el umbral de energía automáticamente
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            # NUEVO: Imprime el umbral para saber qué tan sensible está
            print(f"Umbral de energía ajustado a: {self.recognizer.energy_threshold:.2f}")

        print(f"¡Listo! Escuchando la frase de activación: '{self.ACTIVATION_PHRASE}'...")

        # El método listen se detiene automáticamente, así que lo ponemos en un bucle
        # para que escuche de forma continua.
        while self.running:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=4)
                
                # Usar la API de Google para reconocer el audio
                text = self.recognizer.recognize_google(audio, language="es-MX") # Cambia a "es-MX" para español
                text = text.lower()
                
                print(f"Texto reconocido: '{text}'")
                
                # CAMBIO CLAVE: Condición mucho más flexible
                if "sofi" in text and "activate" in text:
                    print("¡Palabras clave de activación ('Sofi') detectadas!")
                    self.activation_phrase_detected.emit()

            except sr.WaitTimeoutError:
                # No se dijo nada, simplemente continuamos escuchando.
                pass
            except sr.UnknownValueError:
                # La API no pudo entender el audio.
                pass
            except sr.RequestError as e:
                print(f"Error de servicio de Google Speech Recognition; {e}")
                self.stop() # Detener si hay un error de red
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")

    def stop(self):
        """Detiene la escucha."""
        print("Deteniendo escucha de voz.")
        self.running = False