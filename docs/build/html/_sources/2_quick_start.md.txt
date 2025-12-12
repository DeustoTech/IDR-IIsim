# Quick Start Guide

## Prerequisites

To run IDR-IIsim, you need:
- **Python 3.8+** installed on your system.
- **Graphviz** (required for generating process flow diagrams).

## Installation

### Step 1: Clone the repository
Open your terminal and run the following code to clone this repository
```bash
git clone https://github.com/your-org/idr-iisim.git
```

### Step 2: Install Python dependencies
To install the required dependencies, just go to the downloaded project and run `pip`:

```bash
cd idr-iisim
pip install -r requirements.txt
```
### Step 3: Install Graphviz
Ensure you have Graphviz installed in your system for diagram generation.
- On Ubuntu/Debian:
  ```bash
  sudo apt install graphviz
  ```
- On macOS (Homebrew):
  ```bash
  brew install graphviz
  ```
- On Windows:
  1. you should go the webpage of the GraphViz (<https://graphviz.org/download/#windows>)
  2. download the proper installer for your Windows Version (e.g., 64-bit EXE)
  3. Run the installer and ensure you check the option "Add Graphviz to the
system PATH" during installation.

## Configure environment

Create a `.env` file in the root directory and define the path to your
industry sources:

```bash
INDUSTRIES_PATH=Sources
```

If INDUSTRIES_PATH is not provided or if this file does not exit, the default value will be `Sources/`.

## Run the Compiler

When the compiler runs, it will scan the specified industry directory for YAML
files and validate them against the defined schema. If everything is correct
and the YAML files are properly formatted, it will generate Python classes in
the industries/ folder.

In order to run the compiler, just execute:

```bash
python src/main.py
```
