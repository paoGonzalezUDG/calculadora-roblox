import json
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

SETTINGS_FILE = 'settings.json'

class SettingsDialog(QDialog):
    """Una ventana emergente para las configuraciones de la aplicación."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuraciones")
        self.setModal(True)
        self.setFixedSize(350, 180) # Tamaño ajustado para el nuevo botón

        try:
            with open(SETTINGS_FILE, 'r') as f:
                self.settings = json.load(f)
        except (IOError, json.JSONDecodeError):
            self.settings = {}

        layout = QVBoxLayout(self)
        
        # Opción para silenciar sonidos
        self.mute_checkbox = QCheckBox("Silenciar todos los sonidos")
        is_muted = self.settings.get('sound_muted', False)
        self.mute_checkbox.setChecked(is_muted)
        layout.addWidget(self.mute_checkbox)
        
        layout.addStretch()

        buttons_layout = QHBoxLayout()
        
        self.about_button = QPushButton("Acerca de")
        self.about_button.clicked.connect(self._show_about_dialog)
        buttons_layout.addWidget(self.about_button)

        buttons_layout.addStretch() # Empuja los botones de guardar/cancelar a la derecha
        
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_and_accept)
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)
        
        layout.addLayout(buttons_layout)
        
        self.setStyleSheet(parent.styleSheet())

    def _show_about_dialog(self):
        """Muestra una ventana emergente con la información 'Acerca de'."""
        about_text = """
        <h3>Acerca de Sofia calc</h3>
        <p>Esta calculadora con temática Roblox ha sido diseñada especialmente para niños y niñas de 8 a 13 años, buscando hacer del aprendizaje matemático una experiencia divertida e interactiva. Cuenta con misiones, minijuegos y un diseño accesible tanto para personas diestras como zurdas.</p>
        <p>El objetivo principal es fomentar la práctica de las operaciones básicas mientras se mantiene la motivación mediante recompensas virtuales y un entorno visual inspirado en Roblox.</p>
        <p><b>Desarrollada por:</b> Paola González Delgado<br>
        <b>Año:</b> 2025</p>
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Acerca de")
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(about_text)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Estilos para que combine con la app
        msg_box.setStyleSheet("""
            QMessageBox {
                font-family: "Gill Sans Ultra Bold";
            }
            QMessageBox QLabel {
                color: #FFFFFF;
                font-size: 11pt;
            }
            QMessageBox QPushButton {
                background-color: #00A2FF;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 12pt;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #33B5FF;
            }
        """)
        msg_box.exec()

    def save_and_accept(self):
        """Guarda la configuración y cierra el diálogo."""
        self.settings['sound_muted'] = self.mute_checkbox.isChecked()
        try:
            if 'handedness' not in self.settings:
                 self.settings['handedness'] = 'right'
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
            print("Configuración guardada.")
        except IOError as e:
            print(f"Error al guardar la configuración: {e}")
        
        self.accept()

