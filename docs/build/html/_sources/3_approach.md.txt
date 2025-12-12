# Mathematical Approach and Workflow

## General Work-Flow Overview

The framework relies on a distinct flow of data validation and code generation:

* YAML Input: Declarative process and industry files are read from the `Sources/` directory.  
* Validation: The `Validator()` class checks the YAML data against the schema for correct structure and unit consistency.  
* Object Creation: Core classes like `Process()` and `Industry()` translate the validated data into internal Python objects.  
* Code Generation: The `script_generator()` method creates the final, executable Python class inside the `industries/` folder.

## Mathematical Formulation

The core logic of any process in IDR-IIsim is defined using Symbolic Mathematics.
Instead of writing Python functions manually, the user defines an operation string in
the YAML file. The compiler uses the SymPy library to parse, validate, and convert this
string into optimized code.
* **Example**: `Output = Input_A * Efficiency_Factor`
* **Advantage**: This allows users to write non-linear equations or complex physical
relationships easily. The compiler handles the complexity of turning that string
into a callable function.
