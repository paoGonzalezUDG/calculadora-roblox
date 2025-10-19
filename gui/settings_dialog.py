import json
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QCheckBox, QLabel, QGroupBox, QRadioButton,
                             QDialogButtonBox, QWidget, QFrame)
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QFont, QMovie
from .evaluation_dialog import EvaluationDialog

SETTINGS_FILE = 'settings.json'

class CustomSettingsTitleBar(QWidget):
    """Una barra de título personalizada para el diálogo de configuraciones."""
    def __init__(self, title, parent_dialog=None):
        super().__init__(parent_dialog)
        self.parent_dialog = parent_dialog
        self.setObjectName("CustomSettingsTitleBar")
        self.setFixedHeight(45)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)

        self.icon_label = QLabel(self)
        self.icon_movie = QMovie("assets/images/settings_cog.gif")
        if self.icon_movie.isValid():
            self.icon_movie.setScaledSize(QSize(35, 35))
            self.icon_label.setMovie(self.icon_movie)
            self.icon_movie.start()

        self.title_label = QLabel(title, self)
        self.title_label.setFont(QFont("Gill Sans Ultra Bold", 12))
        self.title_label.setObjectName("TitleBarLabel")

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setObjectName("TitleBarButtonClose")
        if self.parent_dialog:
            self.close_button.clicked.connect(self.parent_dialog.reject)

        layout.addWidget(self.close_button)

class SettingsDialog(QDialog):
    """Ventana de configuraciones con barra de título personalizada."""
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.old_pos = None

        self.setModal(True)
        self.setMinimumWidth(500)

        self.settings = current_settings

        main_container = QFrame(self)
        main_container.setObjectName("SettingsDialogContainer")

        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)

        self.title_bar = CustomSettingsTitleBar("Configuraciones", self)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 10, 15, 15)

        # --- Grupo de Accesibilidad ---
        accessibility_group = QGroupBox("Accesibilidad")
        accessibility_layout = QVBoxLayout()
        self.dyslexia_mode_checkbox = QCheckBox("Activar modo para dislexia (requiere reiniciar)")
        self.dyslexia_mode_checkbox.setChecked(self.settings.get('dyslexia_mode', False))
        accessibility_layout.addWidget(self.dyslexia_mode_checkbox)
        accessibility_group.setLayout(accessibility_layout)

        # --- Grupo de Sonido ---
        sound_group = QGroupBox("Sonido")
        sound_layout = QVBoxLayout()
        self.mute_checkbox = QCheckBox("Silenciar todos los sonidos")
        self.mute_checkbox.setChecked(self.settings.get('sound_muted', False))
        sound_layout.addWidget(self.mute_checkbox)
        sound_group.setLayout(sound_layout)

        # --- Grupo de Visualización ---
        display_group = QGroupBox("Método de Visualización")
        display_layout = QVBoxLayout()
        multiplication_label = QLabel("Multiplicación:")
        self.mult_tradicional = QRadioButton("Tradicional (Grupos)")
        self.mult_japones = QRadioButton("Japonés (Líneas)")
        if self.settings.get('multiplication_method', 'traditional') == 'japanese':
            self.mult_japones.setChecked(True)
        else:
            self.mult_tradicional.setChecked(True)
        mult_layout = QHBoxLayout()
        mult_layout.addWidget(self.mult_tradicional)
        mult_layout.addWidget(self.mult_japones)
        division_label = QLabel("División:")
        self.div_tradicional = QRadioButton("Tradicional (Agrupación)")
        self.div_japones = QRadioButton("Japonés (Líneas)")
        if self.settings.get('division_method', 'traditional') == 'japanese':
            self.div_japones.setChecked(True)
        else:
            self.div_tradicional.setChecked(True)
        div_layout = QHBoxLayout()
        div_layout.addWidget(self.div_tradicional)
        div_layout.addWidget(self.div_japones)
        display_layout.addWidget(multiplication_label)
        display_layout.addLayout(mult_layout)
        display_layout.addWidget(division_label)
        display_layout.addLayout(div_layout)
        display_group.setLayout(display_layout)

        # --- Grupo de Progreso ---
        evaluation_group = QGroupBox("Seguimiento del Progreso")
        evaluation_layout = QVBoxLayout()
        self.evaluation_button = QPushButton("📊 Ver Evaluación de Dominio")
        self.evaluation_button.clicked.connect(self.show_evaluation)
        evaluation_layout.addWidget(self.evaluation_button)
        evaluation_group.setLayout(evaluation_layout)

        content_layout.addWidget(accessibility_group)
        content_layout.addWidget(sound_group)
        content_layout.addWidget(display_group)
        content_layout.addWidget(evaluation_group)

        # --- Botones de Acción ---
        button_box = QDialogButtonBox()
        self.about_button = button_box.addButton("Acerca de", QDialogButtonBox.ButtonRole.HelpRole)
        self.about_button.clicked.connect(self.show_about_dialog)
        button_box.addButton("Cancelar", QDialogButtonBox.ButtonRole.RejectRole).clicked.connect(self.reject)
        button_box.addButton("Guardar", QDialogButtonBox.ButtonRole.AcceptRole).clicked.connect(self.accept_settings)
        content_layout.addWidget(button_box, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(content_widget)

        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(main_container)

        # --- Lógica para aplicar el estilo correcto ---
        theme = 'dark' # Por defecto
        if parent:
            parent_bg_color = parent.palette().window().color()
            if parent_bg_color.lightness() > 128: # Detecta si el fondo es claro
                theme = 'light'
        self._apply_styles(theme)

    def _apply_styles(self, theme):
        """Aplica la hoja de estilos correcta según el tema."""
        light_stylesheet = """
            #SettingsDialogContainer {
                background-color: #FDFDFD;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
            }
            #CustomSettingsTitleBar {
                /* CORRECCIÓN: Usar el mismo color que el contenedor */
                background-color: #FDFDFD;
                border-bottom: 1px solid #E0E0E0;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            #TitleBarLabel { color: #000000; }
            QGroupBox { color: #000000; font-weight: bold; }
            QCheckBox, QRadioButton, QLabel { color: #000000; }
            #TitleBarButtonClose {
                font-family: "Arial"; font-size: 14pt; font-weight: bold;
                background-color: transparent; border: none; color: #555555;
            }
            #TitleBarButtonClose:hover { background-color: #E81123; color: white; }
        """

        dark_stylesheet = """
            #SettingsDialogContainer {
                background-color: #2A2C2E;
                border: 1px solid #111;
                border-radius: 8px;
            }
            #CustomSettingsTitleBar {
                background-color: #2A2C2E;
                border-bottom: 1px solid #3c3c3c;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            #TitleBarLabel { color: #CCCCCC; }
            QGroupBox { color: #EEEEEE; font-weight: bold; }
            QCheckBox, QRadioButton, QLabel { color: #DDDDDD; }
            #TitleBarButtonClose {
                font-family: "Arial"; font-size: 14pt; font-weight: bold;
                background-color: transparent; border: none; color: #AAA;
            }
            #TitleBarButtonClose:hover { background-color: #E81123; color: white; }
        """

        if theme == 'light':
            self.setStyleSheet(light_stylesheet)
        else: # dark
            self.setStyleSheet(dark_stylesheet)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.title_bar.underMouse():
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def show_evaluation(self):
        dialog = EvaluationDialog(self)
        dialog.exec()

    def show_about_dialog(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("Acerca de Sofía Calc")
        layout = QVBoxLayout()
        message = QLabel(
            "<b>Calculadora Sofía Calc</b><br><br>"
            "Diseñada para hacer del aprendizaje de las matemáticas una "
            "experiencia divertida e interactiva para niños de 8 a 13 años."
            "<br><br><b>Desarrollado por:</b> Paola González Delgado"
            "<br><b>Año:</b> 2025"
        )
        message.setWordWrap(True)
        layout.addWidget(message)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(about_dialog.accept)
        layout.addWidget(ok_button)
        about_dialog.setLayout(layout)
        about_dialog.exec()

    def accept_settings(self):
        self.settings['sound_muted'] = self.mute_checkbox.isChecked()
        self.settings['multiplication_method'] = 'japanese' if self.mult_japones.isChecked() else 'traditional'
        self.settings['division_method'] = 'japanese' if self.div_japones.isChecked() else 'traditional'
        self.settings['dyslexia_mode'] = self.dyslexia_mode_checkbox.isChecked()

        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error al guardar las configuraciones: {e}")
        self.accept()

