# calculator/pkg/calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        # Insert spaces around parentheses to ensure they become separate tokens
        expression = expression.replace("(", " ( ").replace(")", " ) ")
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[token] <= self.precedence[operators[-1]]
                ):
                    op = operators.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    values.append(self.operators[op](val1, val2))
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    op = operators.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    values.append(self.operators[op](val1, val2))
                operators.pop()  # Remove '('
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    return "Invalid input: Non-numeric token"

        while operators:
            op = operators.pop()
            val2 = values.pop()
            val1 = values.pop()
            values.append(self.operators[op](val1, val2))

        return values[0] if values else None
