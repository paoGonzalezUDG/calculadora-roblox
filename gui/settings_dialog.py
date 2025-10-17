import json
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton, QHBoxLayout, QMessageBox, QFrame, QWidget, QGroupBox, QRadioButton
from PyQt6.QtCore import Qt

SETTINGS_FILE = 'settings.json'

class SettingsDialog(QDialog):
    """Una ventana emergente para las configuraciones de la aplicación."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuraciones")
        self.setModal(True)
        self.setMinimumSize(450, 280) # Aumentamos el tamaño mínimo para la nueva sección

        try:
            with open(SETTINGS_FILE, 'r') as f:
                self.settings = json.load(f)
        except (IOError, json.JSONDecodeError):
            self.settings = {}

        # Layout principal
        main_layout = QVBoxLayout(self)

        # Layout de contenido (dividido en izquierda y derecha)
        content_layout = QHBoxLayout()

        # --- Panel Izquierdo ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.about_button = QPushButton("Acerca de")
        self.about_button.clicked.connect(self._show_about_dialog)

        self.history_button = QPushButton("Historial")
        self.history_button.clicked.connect(self._show_history_dialog)

        # Nuevo GroupBox para métodos de aprendizaje
        self.multiplication_method_group = QGroupBox("Métodos de Multiplicación")
        self.multiplication_method_group.setObjectName("MultiplicationMethodGroup")
        method_layout = QVBoxLayout()

        self.traditional_radio = QRadioButton("Tradicional (Grupos)")
        self.traditional_radio.setObjectName("TraditionalRadio")
        self.japanese_radio = QRadioButton("Japonés (Líneas)")
        self.japanese_radio.setObjectName("JapaneseRadio")

        method_layout.addWidget(self.traditional_radio)
        method_layout.addWidget(self.japanese_radio)
        self.multiplication_method_group.setLayout(method_layout)

        # Establecer selección inicial
        current_method = self.settings.get('multiplication_method', 'traditional')
        if current_method == 'japanese':
            self.japanese_radio.setChecked(True)
        else:
            self.traditional_radio.setChecked(True)

        left_layout.addWidget(self.about_button)
        left_layout.addWidget(self.history_button)
        left_layout.addWidget(self.multiplication_method_group) # Añadir el nuevo grupo

        # --- Separador Vertical ---
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        # --- Panel Derecho ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.mute_checkbox = QCheckBox("Silenciar todos los sonidos")
        is_muted = self.settings.get('sound_muted', False)
        self.mute_checkbox.setChecked(is_muted)

        right_layout.addWidget(self.mute_checkbox)

        # Añadir paneles al layout de contenido
        content_layout.addWidget(left_panel)
        content_layout.addWidget(separator)
        content_layout.addWidget(right_panel)

        # --- Layout de botones inferiores ---
        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.addStretch() # Empuja los botones a la derecha

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_and_accept)

        bottom_buttons_layout.addWidget(self.cancel_button)
        bottom_buttons_layout.addWidget(self.save_button)

        # Añadir todo al layout principal
        main_layout.addLayout(content_layout)
        main_layout.addStretch()
        main_layout.addLayout(bottom_buttons_layout)

        if parent:
            self.setStyleSheet(parent.styleSheet())

        # Ajustes de estilo adicionales si son necesarios
        self.about_button.setMinimumHeight(35)
        self.history_button.setMinimumHeight(35)
        self.multiplication_method_group.setMinimumHeight(100) # Ajustar altura del grupo
        self.traditional_radio.setStyleSheet("QRadioButton { color: white; }")
        self.japanese_radio.setStyleSheet("QRadioButton { color: white; }")

    def _show_history_dialog(self):
        """Crea y muestra el diálogo del historial."""
        from gui.history_dialog import HistoryDialog # Importación local para evitar circular
        history_dialog = HistoryDialog(self)
        history_dialog.exec()

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
        if self.japanese_radio.isChecked():
            self.settings['multiplication_method'] = 'japanese'
        else:
            self.settings['multiplication_method'] = 'traditional'

        try:
            if 'handedness' not in self.settings:
                 self.settings['handedness'] = 'right'
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
            print("Configuración guardada.")
        except IOError as e:
            print(f"Error al guardar la configuración: {e}")

        self.accept()

