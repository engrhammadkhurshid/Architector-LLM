"""
Sample calculator module for testing Architector-LLM
This is a test module with classes and functions
"""

class Calculator:
    """A simple calculator class"""
    
    def __init__(self):
        self.result = 0
    
    def add(self, a, b):
        """Add two numbers"""
        self.result = a + b
        return self.result
    
    def subtract(self, a, b):
        """Subtract b from a"""
        self.result = a - b
        return self.result
    
    def multiply(self, a, b):
        """Multiply two numbers"""
        self.result = a * b
        return self.result
    
    def divide(self, a, b):
        """Divide a by b"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        self.result = a / b
        return self.result


class ScientificCalculator(Calculator):
    """Extended calculator with scientific operations"""
    
    def power(self, base, exponent):
        """Calculate base raised to exponent"""
        self.result = base ** exponent
        return self.result
    
    def square_root(self, n):
        """Calculate square root"""
        import math
        self.result = math.sqrt(n)
        return self.result


def format_result(value):
    """Format a numeric result for display"""
    return f"Result: {value:.2f}"


def validate_input(value):
    """Validate numeric input"""
    if not isinstance(value, (int, float)):
        raise TypeError("Input must be a number")
    return True
