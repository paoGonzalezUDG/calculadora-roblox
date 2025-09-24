import sys
import pygame
import time
import json 

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout, 
                             QPushButton, QLineEdit, QHBoxLayout, QLabel,
                             QStackedWidget)
from PyQt6.QtGui import QFont, QKeyEvent

from core.calculator_logic import CalculatorLogic
from core.mission_engine import MissionEngine
from core.reward_manager import RewardManager
from core.history_logger import HistoryLogger

import re

from gui.visualizer_widget import VisualizerWidget
from gui.interactive_idle_widget import InteractiveIdleWidget
from gui.custom_dialog import CustomVictoryDialog, CustomDefeatDialog
from gui.animated_button import AnimatedButton
from gui.settings_dialog import SettingsDialog

sys.path.append('..')

SETTINGS_FILE = 'settings.json'

class MainWindow(QMainWindow):
    """Ventana principal de la calculadora."""
    
    def __init__(self, settings):
        super().__init__()
        
        self.handedness = settings.get('handedness', 'right')
        self.sound_muted = settings.get('sound_muted', False)
        
        self.mission_engine = MissionEngine()
        self.reward_manager = RewardManager()
        self.history_logger = HistoryLogger()
        self.current_mission = None

        pygame.mixer.init()

        try:
            self.oof_sound = pygame.mixer.Sound('assets/sounds/oof.wav')
            self.fnaf_sound = pygame.mixer.Sound('assets/sounds/fnaf.wav')
            self.bye_sound = pygame.mixer.Sound('assets/sounds/bye.wav')
            self.mission_complete_sound = pygame.mixer.Sound('assets/sounds/mission_complete.wav')
            self.startup_sound = pygame.mixer.Sound('assets/sounds/startup.wav')
            self.jump_sound = pygame.mixer.Sound('assets/sounds/jump.wav')
            self.pop_sound = pygame.mixer.Sound('assets/sounds/pop.wav')
            self.defeat_sound = pygame.mixer.Sound('assets/sounds/defeat.wav')
        except pygame.error as e:
            print(f"Error al cargar un sonido: {e}")
            self.oof_sound, self.fnaf_sound, self.bye_sound, self.mission_complete_sound, self.startup_sound, self.jump_sound, self.pop_sound, self.defeat_sound = [None]*8

        self.logic = CalculatorLogic()
        self.setWindowTitle("Sofia calc")        
        self.resize(800, 600)
        
        self.current_theme = 'roblox_dark' 

        self._rebuild_ui()

    def _rebuild_ui(self):
        """Construye o reconstruye la interfaz de usuario completa."""
        if self.centralWidget():
            self.centralWidget().deleteLater()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_h_layout = QHBoxLayout(self.central_widget)
        
        self.calculator_panel = self._create_calculator_panel()
        self.visualizer = VisualizerWidget()
        self.visualizer.setObjectName("VisualizerPanel")

        if self.handedness == 'left':
            self.main_h_layout.addWidget(self.visualizer)
            self.main_h_layout.addWidget(self.calculator_panel)
        else:
            self.main_h_layout.addWidget(self.calculator_panel)
            self.main_h_layout.addWidget(self.visualizer)

        self.load_stylesheet(f'gui/themes/{self.current_theme}_theme.qss')

    def _create_calculator_panel(self):
        container = QWidget()
        self.left_v_layout = QVBoxLayout(container)
        
        top_section_layout = self._create_display_and_control_buttons()

        self.game_mission_stack = QStackedWidget()
        self.mission_widget = InteractiveIdleWidget(
            oof_sound=self.oof_sound, 
            reward_manager=self.reward_manager,
            mission_complete_sound=self.mission_complete_sound,
            jump_sound=self.jump_sound
        )
        self.mission_widget.set_sound_muted(self.sound_muted)
        
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

        self.left_v_layout.addLayout(top_section_layout)
        self.left_v_layout.addWidget(self.game_mission_stack)
        self.left_v_layout.addLayout(mode_buttons_layout)
        self.left_v_layout.addLayout(buttons_layout)
        
        self._apply_base_styles()
        return container

    def _open_settings_dialog(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    settings = json.load(f)
                    self.sound_muted = settings.get('sound_muted', False)
                    self.mission_widget.set_sound_muted(self.sound_muted)
                    print(f"Configuración de sonido actualizada: {'Silenciado' if self.sound_muted else 'Activado'}")
            except (IOError, json.JSONDecodeError):
                print("No se pudo recargar la configuración.")

    def _toggle_handedness(self):
        self.handedness = 'left' if self.handedness == 'right' else 'right'
        
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
            settings['handedness'] = self.handedness
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=4)
        except (IOError, json.JSONDecodeError):
             with open(SETTINGS_FILE, 'w') as f:
                json.dump({'handedness': self.handedness, 'sound_muted': self.sound_muted}, f, indent=4)
        self._rebuild_ui()
    
    def showEvent(self, event):
        if not self.sound_muted and self.startup_sound:
            self.startup_sound.play(maxtime=1500)
        super().showEvent(event)

    def closeEvent(self, event):
        if not self.sound_muted and self.bye_sound:
            self.bye_sound.play()
            time.sleep(0.9)
        event.accept()

    def keyPressEvent(self, event: QKeyEvent):
        if self.game_mission_stack.currentWidget() == self.mission_widget:
            if event.key() == Qt.Key.Key_Space or event.key() == Qt.Key.Key_Return:
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
        self.setFocus()

    def _return_to_paused_game(self, message):
        if self.current_mission:
            self.current_mission = None
        self.game_mission_stack.setCurrentWidget(self.mission_widget)
        self.mission_widget.stop_game()
        self.mission_widget.setText(message)
        self.setFocus()

    def _on_button_click(self, text=None):
        button = self.sender()
        if not text:
            text = button.text()

        if not self.sound_muted and self.pop_sound and text != '⌫' and text != 'C':
            self.pop_sound.play()

        """if isinstance(button, AnimatedButton):
            button.start_animation()"""

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
                is_correct = user_answer == self.current_mission["answer"]
                
                self.history_logger.log_mission_attempt(self.current_mission, user_answer, is_correct)

                if is_correct:
                    self.reward_manager.add_robux(1)
                    if not self.sound_muted and self.fnaf_sound: self.fnaf_sound.play()
                    message = f"¡Has ganado 1 Robux!"
                    dialog = CustomVictoryDialog(message, self)
                    dialog.exec()
                    if not self.sound_muted: pygame.mixer.stop()
                    self.logic.clear_expression()
                    self.display.setText("")
                    self._return_to_paused_game("¡Misión completada! Presiona 'Jugar Minijuego'.")
                else:
                    self.reward_manager.add_robux(-1)
                    if not self.sound_muted and self.defeat_sound: self.defeat_sound.play()
                    dialog = CustomDefeatDialog("Esa no es la respuesta. ¡Inténtalo de nuevo!", self)
                    dialog.exec()
                    if not self.sound_muted: pygame.mixer.stop()
                    self.logic.clear_expression()
                    self.display.setText("")
                    self._return_to_paused_game("Inténtalo de nuevo. Presiona 'Nueva Misión'.")
                self.mission_widget.update()
                return

            result = self.logic.evaluate_expression()
            self.display.setText(result)
            self._update_visualizer(expression, result)
        
        elif text == '⌫':
            if not self.sound_muted and self.reward_manager.is_unlocked("oof_sound") and self.oof_sound:
                self.oof_sound.play()
            self.logic.delete_last()
            self.display.setText(self.logic.current_expression)
            self.visualizer.clear_all()
        
        elif text == 'C':
            if not self.sound_muted and self.reward_manager.is_unlocked("oof_sound") and self.oof_sound:
                self.oof_sound.play()
            self.logic.clear_expression()
            self.display.setText("")
            self.visualizer.clear_all()
            if self.current_mission:
                self._return_to_paused_game("¡Presiona 'Jugar Minijuego' para empezar!")
        
        else:
            if self.current_mission:
                if text in "0123456789.":
                    self.logic.add_to_expression(text)
                    self.display.setText(self.logic.current_expression)
            else:
                self.logic.add_to_expression(text)
                self.display.setText(self.logic.current_expression)

    def _update_visualizer(self, expression, result):
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
        
        if self.handedness == 'left':
            button_map = {
                '÷':(0,0,1,1),'a/b':(0,1,1,1),'C':(0,2,1,1),'⌫':(0,3,1,1),
                'x':(1,0,1,1),'7':(1,1,1,1),'8':(1,2,1,1),'9':(1,3,1,1),
                '-':(2,0,1,1),'4':(2,1,1,1),'5':(2,2,1,1),'6':(2,3,1,1),
                '+':(3,0,1,1),'1':(3,1,1,1),'2':(3,2,1,1),'3':(3,3,1,1),
                '=':(4,0,1,1),'0':(4,1,1,2),'.':(4,3,1,1),
            }
        else:
            button_map = {
                'C':(0,0,1,1),'⌫':(0,1,1,1),'a/b':(0,2,1,1),'÷':(0,3,1,1),
                '7':(1,0,1,1),'8':(1,1,1,1),'9':(1,2,1,1),'x':(1,3,1,1),
                '4':(2,0,1,1),'5':(2,1,1,1),'6':(2,2,1,1),'-':(2,3,1,1),
                '1':(3,0,1,1),'2':(3,1,1,1),'3':(3,2,1,1),'+':(3,3,1,1),
                '0':(4,0,1,2),'.':(4,2,1,1),'=':(4,3,1,1),
            }

        numeric_buttons = "0123456789."
        operator_buttons = {"÷", "x", "-", "+", "=", "a/b"}

        for text, pos in button_map.items():
            if text in numeric_buttons:
                button = AnimatedButton(text)
            else:
                button = QPushButton(text)
            
            button.setFont(QFont("Gill Sans Ultra Bold", 14))
            button.clicked.connect(self._on_button_click)

            # Asignar propiedad para estilos QSS
            if text in operator_buttons:
                button.setProperty("role", "operator")
            elif text in {"C", "⌫"}:
                button.setProperty("role", "function")
            else:
                button.setProperty("role", "number")

            buttons_layout.addWidget(button, pos[0], pos[1], pos[2], pos[3])
            self.buttons[text] = button

        return buttons_layout
    
    def _create_display_and_control_buttons(self):
        """Crea la pantalla y los botones de control en layouts separados."""
        # Layout principal de esta sección es vertical
        top_section_layout = QVBoxLayout()
        top_section_layout.setSpacing(5) # Espacio reducido entre botones y pantalla
        
        # 1. Layout horizontal para los botones de control (ANTES de la pantalla)
        control_buttons_layout = QHBoxLayout()
        
        self.handedness_button = QPushButton("↔️")
        self.handedness_button.setFixedSize(40, 40) # Tamaño reducido
        self.handedness_button.setObjectName("HandednessButton")
        self.handedness_button.setFont(QFont("Arial", 16))
        self.handedness_button.clicked.connect(self._toggle_handedness)

        self.settings_button = QPushButton("⚙️")
        self.settings_button.setFixedSize(40, 40) # Tamaño reducido
        self.settings_button.setObjectName("SettingsButton")
        self.settings_button.setFont(QFont("Arial", 16))
        self.settings_button.clicked.connect(self._open_settings_dialog)

        self.theme_button = QPushButton("🧱☀️")
        self.theme_button.setFixedSize(40, 40) # Tamaño reducido
        self.theme_button.setObjectName("ThemeButton")
        self.theme_button.setFont(QFont("Arial", 16))
        self.theme_button.clicked.connect(self._toggle_theme)

        # Añadir un espacio flexible para empujar los botones a la derecha
        control_buttons_layout.addStretch()
        control_buttons_layout.addWidget(self.handedness_button)
        control_buttons_layout.addWidget(self.settings_button)
        control_buttons_layout.addWidget(self.theme_button)
        
        # 2. Añadir el layout de botones al layout principal de la sección
        top_section_layout.addLayout(control_buttons_layout)

        # 3. La pantalla de la calculadora (DESPUÉS de los botones)
        self.display = QLineEdit()
        self.display.setFixedHeight(70)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Gill Sans Ultra Bold", 28))
        top_section_layout.addWidget(self.display)
        
        return top_section_layout

    def _toggle_theme(self):        
        if self.current_theme == 'roblox_dark':
            self.current_theme = 'roblox_light'
            self.theme_button.setText("🧱☀️")
        elif self.current_theme == 'roblox_light':
            self.current_theme = 'roblox_dark'
            self.theme_button.setText("🧱")
        else:
            self.current_theme = 'roblox_dark'
            self.theme_button.setText("🧱")
            
        stylesheet_path = f'gui/themes/{self.current_theme}_theme.qss'
        self.load_stylesheet(stylesheet_path)
    
    def _apply_base_styles(self):
        """Aplica estilos base a los botones que deben existir antes de llamar a esta función."""
        for button in self.buttons.values():
            button.setMinimumSize(80, 70)
        if hasattr(self, 'theme_button'):
            self.theme_button.setObjectName("ThemeButton")
        if hasattr(self, 'handedness_button'):
            self.handedness_button.setObjectName("HandednessButton")
        if hasattr(self, 'settings_button'):
            self.settings_button.setObjectName("SettingsButton")
    
    def load_stylesheet(self, file_path):
        try:
            with open(file_path, "r") as f: self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de tema en {file_path}")

