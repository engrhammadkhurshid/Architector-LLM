## Architecture Documentation (Markdown)
```markdown
# Codebase Overview
This codebase is designed around two main modules - `utils` for utility functions and `calculator` for the calculator functionality. The module structure follows a standard Python project layout, with each module having its own directory containing all related files. 

## Modules
### utils
The `utils` module contains helper functions that are used across different modules. It includes:
- **format_error**: A function to format error messages for the user.
- **log_operation**: A function to log operations performed by the calculator.
- **calculate**: The main calculation function, which takes an operation and two numbers as input and returns the result of that operation on those numbers.

### calculator
The `calculator` module contains all the classes and functions necessary for a basic arithmetic calculator. It includes:
- **Calculator**: A class representing a basic calculator, which can perform addition, subtraction, multiplication, and division operations.
- **ScientificCalculator**: A subclass of Calculator that adds support for exponentiation (power) and square root operations.
- **History**: A class to keep track of the history of calculations performed by the calculator. It includes methods to add new entries and retrieve them.
- **main**: The main function, which creates a new instance of Calculator or ScientificCalculator based on user input and performs calculations accordingly.

## Relationships
The `calculator` module depends on the `utils` module for its utility functions. It also uses an instance of History to keep track of past calculations. 
```

## Mermaid Diagram Code

This Mermaid graph shows the relationship between different components in the codebase. The `utils` module is at the top level of the diagram, and it provides utility functions that are used by other modules. The `calculator` module depends on these utilities for its functionality. It also includes a class representing the history of calculations performed by the calculator.
```
```

Please note: Mermaid diagrams require an active internet connection to render properly in GitHub Markdown, as they are essentially JavaScript-based visualizations. The provided code will work if you copy it into a local Mermaid renderer or use online Mermaid live editor.