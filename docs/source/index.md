# IDR-IIsim: Software Documentation


## **1\. Model Aim and Value Proposition**

IDR-IIsim is an open-source compiler designed to bridge the gap between process-level industrial data and large-scale energy system or circular economy models. Its primary aim is to process declarative, data-driven industrial models described in YAML format and automatically generate validated, executable Python classes.

This development facilitates the flow of information among industry experts, programmers, and public policy makers. The industrial process is described declaratively in a structured YAML format and translated into production-ready Python code. This resulting class can process production data to accurately estimate energy and material demands and emissions. This capability aids in quantifying material requirements, identifying circular economy initiatives, and evaluating future policy scenarios.

### **Why use IDR-IIsim?**

The core advantage of this framework, compared to ad-hoc solutions like custom scripts or spreadsheets, is the guarantee of reproducibility and traceability.

* Reproducibility: Models are defined entirely by structured YAML data, not hard-coded logic. Any model instance can be instantly recreated or validated by processing its source YAML files.  
* Interoperability: The compiler’s output is a standard Python object, allowing for seamless integration into large-scale energy and economic simulation frameworks (such as potential EMX modules).  
* Traceability: Every constant, input, and material flow are explicitly documented within the YAML structure, including its source, units, and citation where applicable, ensuring transparent data processing.

### **Scope and Future Dynamics**

Currently, a fully validated model for Cement production is included. We are actively working on expanding the model library to include other high-impact industries, such as steel and the food industry.

The framework is structurally capable of modelling both material and energy flows. While the current implementation is static, the goal is to assess the potential for demand response mechanisms. To this end, the implementation of dynamics (time-series) is planned for a near-future release, leveraging the structure of the generated Python objects. The current version can successfully process CSV files with production data at various geographical levels and years and output a CSV containing all calculated demands and emissions.

## **2\. Mathematical Approach and Workflow**

### **Mathematical Formulation**

Each industrial sub-process (e.g., grinder) is defined by its inputs, outputs, and an operation field. This operation is written as a SymPy-compatible symbolic expression (e.g., Output\_A \= Input\_B \+ Constant\_C \* f(x)).

The compiler utilizes the SymPy library for symbolic mathematics to parse and validate these equations before generating the final Python class method. This design allows the modeler to define non-linearities for individual subprocesses while maintaining a final aggregated object that is well-suited for integration into large-scale energy system models.

### **General Work-Flow Diagram**

The framework relies on a distinct flow of data validation and code generation:

* YAML Input: Declarative process and industry files are read from the Sources/ directory.  
* Validation: The Validator() class checks the YAML data against the schema for correct structure and unit consistency.  
* Object Creation: Core classes like Process() and Industry() translate the validated data into internal Python objects.  
* Code Generation: The script\_generator() method creates the final, executable Python class inside the industries/ folder.

## **3\. Input Data Specification (YAML Schema)**

The input data for any industrial model is provided via YAML files that adhere to the established IISim-Schema. The system implements a modular, two-tiered structure to separate process logic from system aggregation:

1. Process Model (Sub-unit): YAML files (e.g., grinding.yaml) define a single sub-unit's physics and logic. They focus purely on constants, inputs, and outputs.  
2. Industry Model (Aggregation): The main meta.yaml file defines the entire industry, aggregates the sub-processes, and is responsible for defining the system-level outcome and calculating total demands and meta demands.

### **Core Data Fields (Common to both Process and Industry)**

| Section | Purpose | Key Fields | Data Type Notes |
| :---: | :---: | :---: | :---: |
| **constants** | Fixed parameters (e.g., efficiency, ratios, material fractions). | name, value (number), units, source | Static numerical values, providing traceability. |
| **inputs** | External variables required to run the process, such as production targets or boundary conditions. | name, value (array or null), units, from (source) | value can be null (if it’s the target production) or an **array** to define a range for sampling or a list of values. |
| **outputs** | Internal process results or intermediate material/energy flows. | name, operation (SymPy string), args, range | Calculated results, which can be used as inputs for subsequent process steps. |

### **Industry-Specific Sections (Aggregation and System Outputs)**

These sections are only present in the Industry-level (e.g., meta.yaml) file:

| Section | Purpose | Key Fields | Notes |
| :---: | :---: | :---: | :---: |
| **demands** | External elements required by the aggregated industry (e.g., total energy, total raw materials). | name, operation, args, meta | Energy and material streams calculated for the entire technology. |
| **meta** | Meta-demands, which are aggregated values of several demands (e.g., "Total Energy Demand"). | name, operation, args | Allows for high-level variable aggregation. |
| **outcome** | The final product of the industry (i.e., the target for which the demand is calculated). | name, test | The variable the final class is built to produce. |

### **Input Robustness and Checks**

The model includes automatic input checks to catch errors such as unit inconsistency. However, due to the flexibility of the SymPy-based approach, it is possible for users to define models that result in physically infeasible values (e.g., process loss values above 100%).

Warning: We will add explicit print warnings to notify the user immediately when calculated outputs are negative or otherwise questionable. We advise users to complement these warnings by adding input boundary checks within their YAML files or external scripts.

## **4\. Testing and versioning**

**Automated Testing**

The model utilizes Continuous Integration (CI) with tests for units and integration using unittest, and it includes a minimum viable test case based on the cement example.

To improve robustness and transparency, we commit to the following:

* Code Coverage: A code coverage report will be generated and published with the CI results to clearly show the percentage of tested code.  
* Weird Input: The test suite will be expanded to include testing with "weird input" (e.g., boundary, zero, or highly improbable values) to ensure proper input checks are guaranteed.  
* Exception Handling: Tests for all ValueError exception handlings will be implemented to ensure that error paths are also correctly checked.

**Versioning**

The model uses versioning, and we commit to following Semantic Versioning (SemVer) for future releases to clearly denote breaking (major), feature (minor), and patch (patch) changes. Dependency compatibility is explicitly handled via requirements.txt.
```{toctree}
:maxdepth: 2
:caption: Contents:
```
