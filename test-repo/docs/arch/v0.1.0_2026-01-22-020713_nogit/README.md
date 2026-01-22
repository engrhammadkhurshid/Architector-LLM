## Architecture Documentation (Markdown)

### Codebase Overview
The codebase is composed of three main modules: `utils`, `calculator`, and `main`. The `utils` module contains utility functions for logging errors and the history of calculations. The `calculator` module includes two classes, `Calculator` and `ScientificCalculator`, which perform basic arithmetic operations like addition, subtraction, multiplication, and division. Finally, the `main` module is responsible for handling user input and displaying results to the console.

### Modules Breakdown

#### utils Module
This module contains a single function `log_error` that logs errors in a human-readable format. It also includes a history dictionary that keeps track of all calculations performed by the application.

#### calculator Module
The `Calculator` class is responsible for performing basic arithmetic operations like addition, subtraction, multiplication, and division. The `ScientificCalculator` class extends this functionality to include power and square root operations.

#### main Module
This module contains a single function `main` that handles user input and displays results to the console. It imports the necessary classes from the calculator module for calculations.

## Mermaid Diagram Code

This Mermaid graph shows the relationships between different components in the codebase. The `utils` module contains two elements: a function for logging errors and a dictionary for keeping track of calculations. The `calculator` module includes two classes, `Calculator` and `ScientificCalculator`. Finally, the `main` module imports these classes to perform calculations in its main function.

---

Please note that this is a basic representation of the codebase structure. Depending on the complexity of your project, you might need more detailed documentation or diagrams.