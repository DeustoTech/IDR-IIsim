[![Linter](https://github.com/DeustoTech/IDR-IIsim/actions/workflows/linter.yml/badge.svg)]()
[![Tests](https://github.com/DeustoTech/IDR-IIsim/actions/workflows/unit-tests.yaml/badge.svg)]()
[![Integration](https://github.com/DeustoTech/IDR-IIsim/actions/workflows/integration-test.yaml/badge.svg)]()
<img src="https://raw.githubusercontent.com/DeustoTech/IDR-IIsim/refs/heads/badges/coverage/global.svg"/>
[![Documentation](https://img.shields.io/badge/Documentation-GitHub_Pages-blue?logoColor=white&labelColor=333a41)](https://deustotech.github.io/IDR-IIsim/)

# IDR-IIsim

**IDR-IISIM** is an open-source compiler designed to process industrial models described
in YAML format and generate Python scripts that can be integrated into large-scale
energy system models and circular economy assessments.

This repository provides a reproducible and modular framework for describing industrial
processes as data models, validating them, and generating executable scripts.

## License

This project is licensed under the MIT License. You are free to use, modify, and
distribute this software under the terms of the MIT license.

## Quick Start Guide

### Installation

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/your-org/idr-iisim.git
cd idr-iisim
pip install -r requirements.txt
```

Ensure you have Graphviz installed in your system for diagram generation.
On Ubuntu/Debian:

```bash
sudo apt install graphviz
```

On macOS (Homebrew):

```bash
brew install graphviz
```

On Windows, you should go the webpage of the GraphViz (<https://graphviz.org/download/#windows>)
and download the proper installer for your Windows Version.

### Configure environment

Create a `.env` file in the root directory and define the path to your
industry sources:

```bash
INDUSTRIES_PATH=Sources
```

If INDUSTRIES_PATH is not provided, the default value will be `Sources/`.

### Run the Compiler

When the compiler runs, it will scan the specified industry directory for YAML
files and validate them against the defined schema. If everything is correct
and the YAML files are properly formatted, it will generate Python classes in
the industries/ folder.

In order to run the compiler, just execute:

```bash
python src/main.py
```

## Example Usage

Suppose you have the following structure:

```bash
Sources/
└── cement/
├── meta.yaml # Industry-level metadata (type: industry)
├── kiln.yaml # Process description
└── grinding.yaml # Process description
```

Running:

```bash
python src/main.py
```

Will generate a file:

```bash
industries/cement.py
```

containing all processes as Python classes, ready to be used in your simulation
framework.

### Using the generated model

The models are intended to be integrated with other Python codes that use them
in other programs (for instance, energy planification at european and nut 3
levels as well as circular economy models).

However, we can view an example to illustrate how to use the models in a terminal:

```python
$ python
Python 3.13.7 (main, Aug 15 2025, 12:34:02) [GCC 15.2.1 20250813] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from industries.cement import Cement
>>> # We create a production of 5 units of Cement
>>> # (as stated in the YAML file, a unit of cement is a Kiloton)
>>> production = Cement(5)
>>> # Now, we can get the value of clay needed
>>> production.get_clay_demand()
1.875
>>> # Or, we can get a message summarizing all the results of the model
>>> print(production)
Cement industry
---------------
Total Cement Production: 5.00 kt
Limestone Demand: 5.17 kt
Clay Demand: 1.88 kt
Fuel Demand: 0.65 kt
Water Demand: 1.11 m3
Gypsum Demand: 0.17 kt
Mechanical Energy: 1.61 GJ
Co2 Overall Emissions: 2.55 kt
Heat Overall Losses: 0.00 GJ
Pm10 Overall Emission: 0.19 kt
```

## Data Model Description

Each process is defined by a `yaml` file describing constants, inputs, outputs, and
operations:

```yaml
name: method2
id: industry-process_a-method2
description: Example method description
version: 1.0.0
constants:
    - name: alpha
      value: 0.25
inputs:
    - name: a0
      value: 20

outputs:
    - name: Ao
      operation: a0 - b0
      args:
    - name: a0
      type: inputs
    - name: b0
      type: inputs
```

The compiler will:

1. Load and validate this YAML file.
2. Create an internal Process object.
3. Generate Python code implementing the mathematical operations.

## Mathematical Approach

Each `output` in the YAML file contains an `operation` written as a **SymPy-compatible
expression**, e.g.:

```python
Ao = a0 - b0
```

The compiler uses these expressions to generate reproducible and validated Python code.

This approach ensures:

- **Reproducibility**: Models are declarative, not hard-coded.
- **Interoperability**: Output scripts can be integrated into other Python workflows.
- **Traceability**: Each constant, input, and output is documented.

## Methodology &amp; References

This work is based on the concept of **data-driven process modeling**, leveraging:

- **YAML schemas** for robust validation _(Keleshev, 2020)_
- **SymPy** for symbolic mathematics _(Meurer et al., 2017)_
- Best practices in software engineering for **industrial energy systems modeling**
_(see: Connolly et al., 2010, Energy Policy, DOI:10.1016/j.enpol.2009.03.018)_

## Links to Data

Sample industry/process YAML files can be found in the [Sources/](./Sources/) folder of this
repository.

These files can be freely modified or extended to model different industrial processes.

## Version Control

This repository uses **Git** for version control.

To contribute or track changes:

```bash
git clone https://github.com/DeustoTech/IDR-IIsim.git
git checkout -b feature/new-process
```

Please submit pull requests following conventional commit messages and ensure new
models include unit tests and documentation.
