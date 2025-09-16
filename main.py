import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase
from gui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    font_path = 'assets/fonts/roblox_font.ttf'
    
    # Fuente personalizada
    font_id = QFontDatabase.addApplicationFont(font_path)
    
    if font_id < 0:
        print(f"Error: No se pudo cargar la fuente en {font_path}")
    else:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        print(f"Fuente '{font_families[0]}' cargada exitosamente.")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())