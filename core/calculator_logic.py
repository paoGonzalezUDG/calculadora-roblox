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
        Evalúa la expresión matemática actual de forma segura, manejando
        correctamente las operaciones con fracciones.
        """
        if not self.current_expression:
            return ""

        expression_to_eval = self.current_expression.replace('x', '*')

        # Si hay fracciones en la expresión, usar el motor de fracciones.
        if '/' in expression_to_eval:
            try:
                # 1. Convertir todas las partes "num/den" en objetos Fraction
                #    Ej: "1/2+3/4" -> "Fraction(1, 2)+Fraction(3, 4)"
                expression_with_fractions = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', expression_to_eval)

                # 2. Ahora que las fracciones son objetos, reemplazar el símbolo de división
                #    Ej: "Fraction(1, 2)÷Fraction(1, 2)" -> "Fraction(1, 2)/Fraction(1, 2)"
                final_expression = expression_with_fractions.replace('÷', '/')

                # 3. Evaluar la expresión final
                # El contexto de eval necesita saber qué es "Fraction"
                result = eval(final_expression, {"Fraction": Fraction})

                # Formatear el resultado
                if isinstance(result, Fraction):
                    if result.denominator == 1:
                        formatted_result = str(result.numerator)
                    else:
                        formatted_result = f"{result.numerator}/{result.denominator}"
                else: # Si el resultado es un número flotante o entero
                    formatted_result = str(result)

                self.current_expression = formatted_result
                return self.current_expression
            except Exception as e:
                print(f"Error en el cálculo de fracciones: {e}")
                self.current_expression = ""
                return "Error"

        # Si no hay fracciones, proceder con la evaluación decimal normal.
        else:
            try:
                expression_to_eval = expression_to_eval.replace('÷', '/')
                result = Decimal(eval(expression_to_eval))
                formatted_result = f'{result.normalize():f}'

                self.current_expression = formatted_result
                return self.current_expression
            except (SyntaxError, ZeroDivisionError, InvalidOperation, TypeError):
                self.current_expression = ""
                return "Error"

