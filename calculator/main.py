from calculator.pkg.calculator import Calculator

calculator = Calculator()
expression = "3 + 7 * 2"
result = calculator.evaluate(expression)
print(f"{expression} = {result}")