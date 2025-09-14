import sys
import pygame

from PyQt6.QtCore import Qt, QThread
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout, 
                             QPushButton, QLineEdit, QHBoxLayout, QLabel,
                             QMessageBox)
from PyQt6.QtGui import QFont

from core.calculator_logic import CalculatorLogic
from core.audio_listener import AudioListener
from core.mission_engine import MissionEngine
from core.reward_manager import RewardManager

import re
from gui.visualizer_widget import VisualizerWidget

sys.path.append('..')

class MainWindow(QMainWindow):
    """Ventana principal de la calculadora."""
    
    def __init__(self):
        super().__init__()
        
        self.mission_engine = MissionEngine()
        self.reward_manager = RewardManager()
        self.current_mission = None

        pygame.mixer.init()
        try:
            self.oof_sound = pygame.mixer.Sound('assets/sounds/oof.wav')
        except pygame.error as e:
            print(f"Error al cargar el sonido 'oof': {e}")
            self.oof_sound = None

        self.logic = CalculatorLogic()
        self.setWindowTitle("Sofi calc")        
        self.resize(800, 600) # Reactivado
        
        self.current_theme = 'roblox_dark' 

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_h_layout = QHBoxLayout(self.central_widget)
        self.left_v_layout = QVBoxLayout()
        
        top_layout = self._create_display_and_theme_button()

        self.mission_label = QLabel("¡Presiona 'Nueva Misión' para empezar un desafío!")
        self.mission_label.setObjectName("MissionLabel")
        self.mission_label.setWordWrap(True)
        self.mission_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.new_mission_button = QPushButton("🚀 Nueva Misión")
        self.new_mission_button.setObjectName("NewMissionButton")
        self.new_mission_button.clicked.connect(self._start_new_mission)

        buttons_layout = self._create_buttons()

        self.left_v_layout.addLayout(top_layout)
        self.left_v_layout.addWidget(self.mission_label)
        self.left_v_layout.addWidget(self.new_mission_button)
        self.left_v_layout.addLayout(buttons_layout)

        left_container = QWidget()
        left_container.setLayout(self.left_v_layout)

        self.visualizer = VisualizerWidget()
        self.visualizer.setObjectName("VisualizerPanel")
        self.main_h_layout.addWidget(left_container)
        self.main_h_layout.addWidget(self.visualizer)

        self._apply_base_styles()
        self.load_stylesheet(f'gui/themes/{self.current_theme}_theme.qss') # Corregida extensión
        self._setup_audio_listener() # Reactivado
        
    def _play_activation_sound(self):
        """Reproduce el sonido 'OOF' cuando se detecta la frase clave."""
        print("-> INTENTO DE REPRODUCCIÓN: La función '_play_activation_sound' fue llamada.")
        
        if self.oof_sound:
            print("--> ÉXITO: El archivo de sonido 'oof_sound' está cargado. Reproduciendo...")
            self.oof_sound.play()
        else:
            print("--> ERROR: La variable 'self.oof_sound' es None. Revisa la ruta del archivo 'assets/sounds/oof.wav' o si hay un error al cargarlo.")

    def _setup_audio_listener(self):
        """Configura e inicia el listener de audio en un hilo separado."""
        self.audio_thread = QThread()
        self.audio_worker = AudioListener(activation_phrase="sofi activate") 
        self.audio_worker.moveToThread(self.audio_thread)
        
        self.audio_thread.started.connect(self.audio_worker.run)
        
        # Conectar la señal de tronido de dedos (si aún la quieres)
        self.audio_worker.snap_detected.connect(self._toggle_theme)
        
        # ¡Conectar la nueva señal al nuevo slot (función)!
        self.audio_worker.activation_phrase_detected.connect(self._play_activation_sound)
        
        self.audio_thread.finished.connect(self.audio_thread.deleteLater)
        self.destroyed.connect(self.stop_audio_thread)
        
        self.audio_thread.start()
    
    def stop_audio_thread(self):
        """Detiene de forma segura el hilo de audio."""
        if hasattr(self, 'audio_worker'):
            self.audio_worker.stop()
        if hasattr(self, 'audio_thread'):
            self.audio_thread.quit()
            self.audio_thread.wait()
            
    def _start_new_mission(self):
        self.current_mission = self.mission_engine.get_random_mission()
        self.mission_label.setText(self.current_mission["text"])
        self.logic.clear_expression()
        self.display.setText("")
        self.visualizer.update_visualization(None, None, None, None)

    def _create_display_and_theme_button(self):
        top_layout = QHBoxLayout()
        # ... (el resto del código de esta función no cambia)
        self.display = QLineEdit()
        self.display.setFixedHeight(70)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Gill Sans Ultra Bold", 28))
        self.theme_button = QPushButton("🧱☀️")
        self.theme_button.setFixedSize(50, 50)
        self.theme_button.setFont(QFont("Arial", 18))
        self.theme_button.clicked.connect(self._toggle_theme)
        top_layout.addWidget(self.display)
        top_layout.addWidget(self.theme_button)
        return top_layout # DEBE RETORNAR EL LAYOUT

    def _toggle_theme(self):
        """Cambia entre los temas: Oscuro, Claro, Roblox Oscuro y Roblox Claro."""
        
        # El sonido lo dejamos para después
        # if self.snap_sound:
        #     self.snap_sound.play()

        if self.current_theme == 'dark':
            # De Oscuro pasa a Claro
            self.current_theme = 'light'
            self.theme_button.setText("🌙")
        elif self.current_theme == 'light':
            # De Claro pasa a Roblox Oscuro
            self.current_theme = 'roblox_dark'
            self.theme_button.setText("🧱") # Emoji de bloque para Roblox
        elif self.current_theme == 'roblox_dark':
            # De Roblox Oscuro pasa a Roblox Claro
            self.current_theme = 'roblox_light'
            self.theme_button.setText("🧱☀️") # Icono combinado
        else: # si es roblox_light
            # De Roblox Claro vuelve al inicio (Oscuro)
            self.current_theme = 'dark'
            self.theme_button.setText("☀️")
            
        stylesheet_path = f'gui/themes/{self.current_theme}_theme.qss'
        self.load_stylesheet(stylesheet_path)
        print(f"Tema cambiado a: {self.current_theme}")

    def _create_buttons(self):
        """Crea y posiciona los botones de la calculadora."""
        buttons_layout = QGridLayout()
        self.buttons = {} 
        button_map = {
            'C': (0, 0, 1, 1), '%': (0, 1, 1, 1), '⌫': (0, 2, 1, 1), '÷': (0, 3, 1, 1),
            '7': (1, 0, 1, 1), '8': (1, 1, 1, 1), '9': (1, 2, 1, 1), 'x': (1, 3, 1, 1),
            '4': (2, 0, 1, 1), '5': (2, 1, 1, 1), '6': (2, 2, 1, 1), '-': (2, 3, 1, 1),
            '1': (3, 0, 1, 1), '2': (3, 1, 1, 1), '3': (3, 2, 1, 1), '+': (3, 3, 1, 1),
            '0': (4, 0, 1, 2), '.': (4, 2, 1, 1), '=': (4, 3, 1, 1),
        }
        for text, pos in button_map.items():
            button = QPushButton(text)
            button.setFont(QFont("Gill Sans Ultra Bold", 14))
            button.clicked.connect(self._on_button_click)
            buttons_layout.addWidget(button, pos[0], pos[1], pos[2], pos[3])
            self.buttons[text] = button
        return buttons_layout

    def _apply_base_styles(self):
        for button in self.buttons.values():
            button.setMinimumSize(80, 70)
        self.theme_button.setObjectName("ThemeButton")

    def _on_button_click(self):
        button = self.sender()
        text = button.text()

        if text == '=':
            if self.current_mission:
                user_answer = self.display.text()
                if user_answer == self.current_mission["answer"]:
                    if self.oof_sound:
                        self.oof_sound.play()
                    
                    reward_id = self.current_mission["reward"]
                    just_unlocked = self.reward_manager.unlock_reward(reward_id)
                    
                    msg_box = QMessageBox()
                    # ... estilos y configuración del msg_box ...
                    msg_box.exec()
                    
                    self.current_mission = None
                    self.mission_label.setText("¡Misión completada! Presiona 'Nueva Misión' para otra.")
                else:
                    if self.oof_sound:
                        self.oof_sound.play()
                    msg_box = QMessageBox()
                    # ... estilos y configuración del msg_box ...
                    msg_box.exec()
            else:
                expression = self.logic.current_expression
                result = self.logic.evaluate_expression()
                self.display.setText(result)

                if result != "Error":
                    match = re.search(r'(\d+\.?\d*)([+\-x÷])(\d+\.?\d*)', expression)
                    if match:
                        num1, op, num2 = match.groups()
                        self.visualizer.update_visualization(float(num1), op, float(num2), float(result))
                    else:
                        self.visualizer.update_visualization(None, None, None, None)
                else:
                    self.visualizer.update_visualization(None, None, None, None)
        
        elif text == '⌫':
            if self.reward_manager.is_unlocked("oof_sound") and self.oof_sound:
                self.oof_sound.play()
            
            self.logic.delete_last()
            self.display.setText(self.logic.current_expression)
            self.visualizer.update_visualization(None, None, None, None)
        
        elif text == 'C':
            self.logic.clear_expression()
            self.display.setText("")
            self.visualizer.update_visualization(None, None, None, None)
            self.current_mission = None
            self.mission_label.setText("¡Presiona 'Nueva Misión' para empezar un desafío!")
        
        else: # Si es un número o un operador
            # --- INICIO DE LA CORRECCIÓN DEL BUG ---
            # Si hay una misión activa y el usuario pulsa un operador,
            # cancelamos la misión para permitir el cálculo normal.
            if self.current_mission and text in "+-x÷":
                self.current_mission = None
                self.mission_label.setText("Misión cancelada. ¡Calculadora lista!")
            
            if self.current_mission:
                # Si AÚN estamos en misión, solo aceptamos números.
                if text in "0123456789.":
                    self.logic.add_to_expression(text)
                    self.display.setText(self.logic.current_expression)
            else:
                # Modo calculadora normal
                self.logic.add_to_expression(text)
                self.display.setText(self.logic.current_expression)
            # --- FIN DE LA CORRECCIÓN DEL BUG ---
    
    def load_stylesheet(self, file_path):
        try:
            with open(file_path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de tema en {file_path}")