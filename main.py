import sys
import os
import json
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase
from gui.main_window import MainWindow
from gui.handedness_dialog import HandednessDialog

SETTINGS_FILE = 'settings.json'

def get_user_settings():
    """Carga las configuraciones del usuario. Si no existen, las solicita."""
    if not os.path.exists(SETTINGS_FILE):
        # El archivo no existe, hay que preguntar al usuario
        dialog = HandednessDialog()
        if dialog.exec():
            handedness = dialog.selection
            settings = {'handedness': handedness}
            try:
                with open(SETTINGS_FILE, 'w') as f:
                    json.dump(settings, f)
            except IOError as e:
                print(f"Error al guardar las configuraciones: {e}")
            return settings
        else:
            # Si el usuario cierra el diálogo, usar el valor por defecto
            return {'handedness': 'right'}
    else:
        # El archivo existe, cargar la configuración
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            # Si el archivo está corrupto, empezar de nuevo
            return {'handedness': 'right'}

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    font_path = 'assets/fonts/roblox_font.ttf'
    font_id = QFontDatabase.addApplicationFont(font_path)
    
    if font_id < 0:
        print(f"Error: No se pudo cargar la fuente en {font_path}")
    else:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        print(f"Fuente '{font_families[0]}' cargada exitosamente.")

    # Obtener la preferencia del usuario
    user_settings = get_user_settings()
    handedness_preference = user_settings.get('handedness', 'right')

    # Pasar la preferencia a la ventana principal
    window = MainWindow(handedness=handedness_preference)
    window.show()
    sys.exit(app.exec())

