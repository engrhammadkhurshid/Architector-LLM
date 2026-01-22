"""
Main entry point for calculator application
"""

from calculator import Calculator, ScientificCalculator, format_result, validate_input


def main():
    """Main function to run the calculator"""
    calc = Calculator()
    
    # Perform some calculations
    result1 = calc.add(10, 5)
    print(format_result(result1))
    
    result2 = calc.multiply(3, 4)
    print(format_result(result2))
    
    # Use scientific calculator
    sci_calc = ScientificCalculator()
    result3 = sci_calc.power(2, 3)
    print(format_result(result3))
    
    print("Calculator operations completed successfully!")


if __name__ == "__main__":
    main()
