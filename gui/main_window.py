import sys
import pygame
import time

from PyQt6.QtCore import Qt, QThread
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout, 
                             QPushButton, QLineEdit, QHBoxLayout, QLabel,
                             QMessageBox, QStackedWidget)
from PyQt6.QtGui import QFont, QKeyEvent

from core.calculator_logic import CalculatorLogic
from core.audio_listener import AudioListener
from core.mission_engine import MissionEngine
from core.reward_manager import RewardManager

import re

from gui.visualizer_widget import VisualizerWidget
from gui.interactive_idle_widget import InteractiveIdleWidget
from gui.custom_dialog import CustomVictoryDialog, CustomDefeatDialog

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
            self.fnaf_sound = pygame.mixer.Sound('assets/sounds/fnaf.wav')
            self.bye_sound = pygame.mixer.Sound('assets/sounds/bye.wav')
        except pygame.error as e:
            print(f"Error al cargar un sonido: {e}")

            self.oof_sound = None
            self.fnaf_sound = None
            self.bye_sound = None

        self.logic = CalculatorLogic()
        self.setWindowTitle("Sofi calc")        
        self.resize(800, 600)
        
        self.current_theme = 'roblox_dark' 

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_h_layout = QHBoxLayout(self.central_widget)
        self.left_v_layout = QVBoxLayout()
        
        top_layout = self._create_display_and_theme_button()

        self.game_mission_stack = QStackedWidget()
        
        self.mission_widget = InteractiveIdleWidget(oof_sound=self.oof_sound)
        
        self.mission_display_label = QLabel("¡Presiona 'Nueva Misión' o 'Jugar Minijuego'!")
        self.mission_display_label.setObjectName("MissionLabel")
        self.mission_display_label.setWordWrap(True)
        self.mission_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.game_mission_stack.addWidget(self.mission_widget)
        self.game_mission_stack.addWidget(self.mission_display_label)
        self.game_mission_stack.setCurrentWidget(self.mission_widget)

        mode_buttons_layout = QHBoxLayout()
        self.new_mission_button = QPushButton("🚀 Nueva Misión")
        self.new_mission_button.setObjectName("NewMissionButton")
        self.new_mission_button.clicked.connect(self._activate_mission_mode)

        self.play_game_button = QPushButton("🕹️ Jugar Minijuego")
        self.play_game_button.setObjectName("PlayGameButton")
        self.play_game_button.clicked.connect(self._activate_game_mode)
        
        mode_buttons_layout.addWidget(self.new_mission_button)
        mode_buttons_layout.addWidget(self.play_game_button)

        buttons_layout = self._create_buttons()

        self.left_v_layout.addLayout(top_layout)
        self.left_v_layout.addWidget(self.game_mission_stack)
        self.left_v_layout.addLayout(mode_buttons_layout)
        self.left_v_layout.addLayout(buttons_layout)

        left_container = QWidget()
        left_container.setLayout(self.left_v_layout)

        self.visualizer = VisualizerWidget()
        self.visualizer.setObjectName("VisualizerPanel")

        self.main_h_layout.addWidget(left_container)
        self.main_h_layout.addWidget(self.visualizer)

        self._apply_base_styles()
        self.load_stylesheet(f'gui/themes/{self.current_theme}_theme.qss')
        # self._setup_audio_listener()

    def closeEvent(self, event):
        """
        Se ejecuta cuando el usuario cierra la ventana.
        Reproduce un sonido de despedida y cierra rápidamente.
        """
        if self.bye_sound:
            self.bye_sound.play()
            
            time.sleep(0.9) # 900 milisegundos de pausa
        
        event.accept() # Permite que la ventana se cierre

    def keyPressEvent(self, event: QKeyEvent):
        """Maneja las pulsaciones de teclas para el salto del personaje."""
        if self.game_mission_stack.currentWidget() == self.mission_widget:
            if event.key() == Qt.Key.Key_Space or event.key() == Qt.Key.Key_Return:
                if not self.mission_widget.is_active:
                    self.mission_widget.start_game()
                else:
                    self.mission_widget.jump()

    def _activate_mission_mode(self):
        self.mission_widget.stop_game()
        self.game_mission_stack.setCurrentWidget(self.mission_display_label)
        
        self.current_mission = self.mission_engine.get_random_mission()
        self.mission_display_label.setText(self.current_mission["text"])
        self.logic.clear_expression()
        self.display.setText("")
        self.visualizer.clear_all()

    def _activate_game_mode(self):
        if self.current_mission:
            self.current_mission = None

        self.game_mission_stack.setCurrentWidget(self.mission_widget)
        self.mission_widget.start_game()

    def _return_to_paused_game(self, message):
        if self.current_mission:
            self.current_mission = None

        self.game_mission_stack.setCurrentWidget(self.mission_widget)
        self.mission_widget.stop_game()
        self.mission_widget.setText(message)

    def _on_button_click(self, text=None):
        if not text:
            button = self.sender()
            text = button.text()

        if self.current_mission and text in "a/b+-x÷":
            self._return_to_paused_game("Misión cancelada. ¡Calculadora lista!")
        
        if text == 'a/b':
            self.logic.add_to_expression('/')
            self.display.setText(self.logic.current_expression)
            return

        if text == '=':
            expression = self.logic.current_expression
            if self.current_mission:
                user_answer = self.display.text()
                if user_answer == self.current_mission["answer"]:
                    if self.fnaf_sound: self.fnaf_sound.play()
                    reward_id = self.current_mission["reward"]
                    just_unlocked = self.reward_manager.unlock_reward(reward_id)
                    
                    message = f"¡Has desbloqueado '{reward_id}'!" if just_unlocked else "¡Misión completada!"
                    dialog = CustomVictoryDialog(message, self)
                    dialog.exec()
                    
                    pygame.mixer.stop()

                    # Limpia la pantalla después de la misión.
                    self.logic.clear_expression()
                    self.display.setText("")
                    
                    self._return_to_paused_game("¡Misión completada! Presiona 'Jugar' o una tecla.")
                else:
                    if self.oof_sound: self.oof_sound.play()
                    dialog = CustomDefeatDialog("Esa no es la respuesta. ¡Inténtalo de nuevo!", self)
                    dialog.exec()

                    pygame.mixer.stop()

                    # Limpia la pantalla después de la misión.
                    self.logic.clear_expression()
                    self.display.setText("")

                return

            result = self.logic.evaluate_expression()

            self.display.setText(result)
            self._update_visualizer(expression, result)
        
        elif text == '⌫':
            if self.reward_manager.is_unlocked("oof_sound") and self.oof_sound: self.oof_sound.play()

            self.logic.delete_last()
            self.display.setText(self.logic.current_expression)
            self.visualizer.clear_all()
        
        elif text == 'C':
            self.logic.clear_expression()
            self.display.setText("")
            self.visualizer.clear_all()

            if self.current_mission:
                self._return_to_paused_game("¡Presiona 'Jugar' o una tecla para empezar!")
        
        else:
            if self.current_mission:
                if text in "0123456789.":
                    self.logic.add_to_expression(text)
                    self.display.setText(self.logic.current_expression)
            else:
                self.logic.add_to_expression(text)
                self.display.setText(self.logic.current_expression)

    def _update_visualizer(self, expression, result):
        """Actualiza el visualizador según el tipo de operación."""
        fraction_match = re.search(r'(\d+)/(\d+)\s*([+\-x])\s*(\d+)/(\d+)', expression)
        if fraction_match:
            f1_num, f1_den, op, f2_num, f2_den = fraction_match.groups()
            res_num, res_den = result.split('/') if '/' in result else (result, '1')
            self.visualizer.update_fraction_visualization(op, (f1_num, f1_den), (f2_num, f2_den), (res_num, res_den))
        elif result != "Error":
            match = re.search(r'(\d+\.?\d*)([+\-x÷])(\d+\.?\d*)', expression)
            if match:
                num1, op, num2 = match.groups()
                self.visualizer.update_visualization(float(num1), op, float(num2), float(result))
            else: self.visualizer.clear_all()
        else: self.visualizer.clear_all()

    def _create_buttons(self):
        buttons_layout = QGridLayout()
        self.buttons = {} 

        button_map = {
            'C': (0, 0, 1, 1), 'a/b': (0, 1, 1, 1), '⌫': (0, 2, 1, 1), '÷': (0, 3, 1, 1),
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
    
    def _create_display_and_theme_button(self):
        top_layout = QHBoxLayout()

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

        return top_layout

    def _toggle_theme(self):        
        if self.current_theme == 'dark':
            self.current_theme = 'light'
            self.theme_button.setText("🌙")
        elif self.current_theme == 'light':
            self.current_theme = 'roblox_dark'
            self.theme_button.setText("🧱")
        elif self.current_theme == 'roblox_dark':
            self.current_theme = 'roblox_light'
            self.theme_button.setText("🧱☀️")
        else:
            self.current_theme = 'dark'
            self.theme_button.setText("☀️")
            
        stylesheet_path = f'gui/themes/{self.current_theme}_theme.qss'
        self.load_stylesheet(stylesheet_path)
    
    def _apply_base_styles(self):
        for button in self.buttons.values():
            button.setMinimumSize(80, 70)

        self.theme_button.setObjectName("ThemeButton")
    
    def load_stylesheet(self, file_path):
        try:
            with open(file_path, "r") as f: self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de tema en {file_path}")
            
    def _setup_audio_listener(self): pass
    def stop_audio_thread(self): pass

