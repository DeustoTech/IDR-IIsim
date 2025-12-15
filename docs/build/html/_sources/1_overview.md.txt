# Model Aim and Value Proposition

IDR-IIsim is an open-source compiler designed to bridge the gap between process-level industrial data and large-scale energy system or circular economy models. Its primary aim is to process declarative, data-driven industrial models described in YAML format and automatically generate validated, executable Python classes.

This development facilitates the flow of information among industry experts, programmers, and public policy makers. The industrial process is described declaratively in a structured YAML format and translated into production-ready Python code. This resulting class can process production data to accurately estimate energy and material demands and emissions. This capability aids in quantifying material requirements, identifying circular economy initiatives, and evaluating future policy scenarios.

## Why use IDR-IIsim?

The core advantage of this framework, compared to ad-hoc solutions like custom scripts or spreadsheets, is the guarantee of reproducibility and traceability.

* **Reproducibility**: Models are defined entirely by structured YAML data, not hard-coded logic. Any model instance can be instantly recreated or validated by processing its source YAML files.  
* **Interoperability**: The compiler’s output is a standard Python object, allowing for seamless integration into large-scale energy and economic simulation frameworks (such as potential EMX modules).  
* **Traceability**: Every constant, input, and material flow are explicitly documented within the YAML structure, including its source, units, and citation where applicable, ensuring transparent data processing.

## Scope and Future Dynamics

Currently, a fully validated model for Cement production is included. We are actively working on expanding the model library to include other high-impact industries, such as steel and the food industry.

The framework is structurally capable of modelling both material and energy flows. While the current implementation is static, the goal is to assess the potential for demand response mechanisms. To this end, the implementation of dynamics (time-series) is planned for a near-future release, leveraging the structure of the generated Python objects. The current version can successfully process CSV files with production data at various geographical levels and years and output a CSV containing all calculated demands and emissions.
