[![Linter](https://github.com/DeustoTech/IDR-IIsim/actions/workflows/linter.yml/badge.svg)]()
[![Tests](https://github.com/DeustoTech/IDR-IIsim/actions/workflows/unit-tests.yaml/badge.svg)]()
[![Integration](https://github.com/DeustoTech/IDR-IIsim/actions/workflows/integration-test.yaml/badge.svg)]()
![Coverage Status](<https://img.shields.io/badge/coverage-${{> env.COVERAGE_PERCENTAGE }}%25-brightgreen)

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

### Configure environment

Create a `.env` file in the root directory and define the path to your
industry sources:

```bash
INDUSTRIES_PATH=Sources
```

If INDUSTRIES_PATH is not provided, the default value will be `Sources/`.

### Run the Compiler

```bash
python src/main.py

This will:
 Scan the specified industry directory for YAML files.
 Validate them against the schema.
 Generate Python scripts inside the `industries/` folder.
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
python main.py
```

Will generate a file:

```bash
industries/cement.py
```

containing all processes as Python classes, ready to be used in your simulation
framework.

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
value: [20, 25]

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
git clone https://github.com/your-org/idr-iisim.git
git checkout -b feature/new-process
```

Please submit pull requests following conventional commit messages and ensure new
models include unit tests and documentation.
