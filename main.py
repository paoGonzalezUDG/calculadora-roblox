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
    default_settings = {'handedness': 'right', 'sound_muted': False}
    
    if not os.path.exists(SETTINGS_FILE):
        dialog = HandednessDialog()
        if dialog.exec():
            handedness = dialog.selection
            settings = {'handedness': handedness, 'sound_muted': False}
            try:
                with open(SETTINGS_FILE, 'w') as f:
                    json.dump(settings, f, indent=4)
                return settings
            except IOError as e:
                print(f"Error al guardar las configuraciones: {e}")
                return default_settings
        else:
            return default_settings
    else:
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                if 'handedness' not in settings:
                    settings['handedness'] = 'right'
                if 'sound_muted' not in settings:
                    settings['sound_muted'] = False
                return settings
        except (IOError, json.JSONDecodeError):
            return default_settings

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    font_path = 'assets/fonts/roblox_font.ttf'
    font_id = QFontDatabase.addApplicationFont(font_path)
    
    if font_id < 0:
        print(f"Error: No se pudo cargar la fuente en {font_path}")
    else:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        print(f"Fuente '{font_families[0]}' cargada exitosamente.")

    user_settings = get_user_settings()
    
    window = MainWindow(settings=user_settings)
    window.show()
    sys.exit(app.exec())

