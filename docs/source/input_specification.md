## Input Data Specification

*(YAML Schema)*

The input data for any industrial model is provided via YAML files that adhere to the established IISim-Schema. The system implements a modular, two-tiered structure to separate process logic from system aggregation:

1. Process Model (Sub-unit): YAML files (e.g., grinding.yaml) define a single sub-unit's physics and logic. They focus purely on constants, inputs, and outputs.  
2. Industry Model (Aggregation): The main meta.yaml file defines the entire industry, aggregates the sub-processes, and is responsible for defining the system-level outcome and calculating total demands and meta demands.

### Core Data Fields (Common to both Process and Industry)

| Section | Purpose | Key Fields | Data Type Notes |
| :---: | :---: | :---: | :---: |
| **constants** | Fixed parameters (e.g., efficiency, ratios, material fractions). | name, value (number), units, source | Static numerical values, providing traceability. |
| **inputs** | External variables required to run the process, such as production targets or boundary conditions. | name, value (array or null), units, from (source) | value can be null (if it’s the target production) or an **array** to define a range for sampling or a list of values. |
| **outputs** | Internal process results or intermediate material/energy flows. | name, operation (SymPy string), args, range | Calculated results, which can be used as inputs for subsequent process steps. |

### Industry-Specific Sections (Aggregation and System Outputs)

These sections are only present in the Industry-level (e.g., meta.yaml) file:

| Section | Purpose | Key Fields | Notes |
| :---: | :---: | :---: | :---: |
| **demands** | External elements required by the aggregated industry (e.g., total energy, total raw materials). | name, operation, args, meta | Energy and material streams calculated for the entire technology. |
| **meta** | Meta-demands, which are aggregated values of several demands (e.g., "Total Energy Demand"). | name, operation, args | Allows for high-level variable aggregation. |
| **outcome** | The final product of the industry (i.e., the target for which the demand is calculated). | name, test | The variable the final class is built to produce. |

### Input Robustness and Checks

The model includes automatic input checks to catch errors such as unit inconsistency. However, due to the flexibility of the SymPy-based approach, it is possible for users to define models that result in physically infeasible values (e.g., process loss values above 100%).

Warning: We will add explicit print warnings to notify the user immediately when calculated outputs are negative or otherwise questionable. We advise users to complement these warnings by adding input boundary checks within their YAML files or external scripts.
