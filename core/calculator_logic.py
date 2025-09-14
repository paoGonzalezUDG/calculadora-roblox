# core/calculator_logic.py

from decimal import Decimal, InvalidOperation

class CalculatorLogic:
    """Maneja todas las operaciones y el estado de la calculadora."""
    
    def __init__(self):
        self.current_expression = ""

    def add_to_expression(self, value):
        """Añade un número u operador a la expresión actual."""
        self.current_expression += str(value)

    def clear_expression(self):
        """Limpia la expresión actual."""
        self.current_expression = ""

    def delete_last(self):
        """Borra el último caracter de la expresión."""
        self.current_expression = self.current_expression[:-1]

    def evaluate_expression(self):
        """
        Evalúa la expresión matemática actual de forma segura.
        Retorna el resultado o un mensaje de error.
        """
        if not self.current_expression:
            return ""
            
        try:
            # Reemplazamos símbolos para que Python los entienda
            # Puedes expandir esto para más operaciones (ej. ^ para potencia)
            expression_to_eval = self.current_expression.replace('x', '*').replace('÷', '/')
            
            # Usar Decimal para precisión financiera y evitar errores de punto flotante
            result = Decimal(eval(expression_to_eval))
            
            # Formatear el resultado para quitar ceros innecesarios al final
            self.current_expression = str(result.normalize())
            return self.current_expression
        except (SyntaxError, ZeroDivisionError, InvalidOperation):
            self.current_expression = "" # Limpiar en caso de error
            return "Error"