import csv
import os
from datetime import datetime

class HistoryLogger:
    """Registra los intentos de misión en un archivo CSV."""
    
    def __init__(self, filename="mission_history.csv"):
        self.filename = filename
        self._initialize_file()

    def _initialize_file(self):
        """Crea el archivo CSV con encabezados si no existe."""
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Fecha y Hora", "Texto de la Mision", "Respuesta del Usuario", 
                    "Respuesta Correcta", "Resultado", "Tipo de Operacion"
                ])

    def log_mission_attempt(self, mission, user_answer, is_correct):
        """Añade una nueva fila al historial de misiones."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = "Correcto" if is_correct else "Incorrecto"
        
        with open(self.filename, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                now,
                mission['text'],
                user_answer,
                mission['answer'],
                result,
                mission.get('operation_type', 'No especificado')
            ])
        print(f"Intento de misión registrado en {self.filename}")

