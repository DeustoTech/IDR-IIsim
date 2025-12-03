# Mathematical Approach and Workflow

## Mathematical Formulation

Each industrial sub-process (e.g., grinder) is defined by its inputs, outputs, and an operation field. This operation is written as a SymPy-compatible symbolic expression (e.g., Output\_A \= Input\_B \+ Constant\_C \* f(x)).

The compiler utilizes the SymPy library for symbolic mathematics to parse and validate these equations before generating the final Python class method. This design allows the modeler to define non-linearities for individual subprocesses while maintaining a final aggregated object that is well-suited for integration into large-scale energy system models.

## General Work-Flow Diagram

The framework relies on a distinct flow of data validation and code generation:

* YAML Input: Declarative process and industry files are read from the Sources/ directory.  
* Validation: The Validator() class checks the YAML data against the schema for correct structure and unit consistency.  
* Object Creation: Core classes like Process() and Industry() translate the validated data into internal Python objects.  
* Code Generation: The script\_generator() method creates the final, executable Python class inside the industries/ folder.
