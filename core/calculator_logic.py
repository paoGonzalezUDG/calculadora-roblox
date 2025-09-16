from decimal import Decimal, InvalidOperation
from fractions import Fraction
import re

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
        
        expression_to_eval = self.current_expression.replace('x', '*').replace('÷', '/')

        # --- LÓGICA DE FRACCIONES ---
        if '/' in expression_to_eval and '÷' not in self.current_expression:
            try:
                # Convierte "1/2" a "Fraction(1, 2)"
                expression_with_fractions = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', expression_to_eval)
                
                result = eval(expression_with_fractions, {"Fraction": Fraction})

                if result.denominator == 1:
                    formatted_result = str(result.numerator)
                else:
                    formatted_result = f"{result.numerator}/{result.denominator}"
                
                self.current_expression = formatted_result
                return self.current_expression
            except Exception as e:
                print(f"Error en el cálculo de fracciones: {e}")
                self.current_expression = ""
                return "Error"
        # --- FIN DE LÓGICA DE FRACCIONES ---

        try:
            result = Decimal(eval(expression_to_eval))
            formatted_result = f'{result.normalize():f}'

            self.current_expression = formatted_result
            return self.current_expression
        except (SyntaxError, ZeroDivisionError, InvalidOperation):
            self.current_expression = ""
            return "Error"