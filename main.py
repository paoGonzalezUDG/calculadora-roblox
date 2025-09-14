# main.py

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase  # Importar QFontDatabase
from gui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # --- INICIO DE CÓDIGO NUEVO ---
    # Ruta al archivo de la fuente
    font_path = 'assets/fonts/roblox_font.ttf'
    
    # Cargar la fuente en la base de datos de la aplicación
    font_id = QFontDatabase.addApplicationFont(font_path)
    
    # Comprobar si la fuente se cargó correctamente
    if font_id < 0:
        print(f"Error: No se pudo cargar la fuente en {font_path}")
    else:
        # Opcional: imprimir el nombre de la familia de la fuente cargada para verificar
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        print(f"Fuente '{font_families[0]}' cargada exitosamente.")
    # --- FIN DE CÓDIGO NUEVO ---

    window = MainWindow()
    window.show()
    sys.exit(app.exec())