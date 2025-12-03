# Quick Start Guide

## Installation

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

## Configure environment

Create a `.env` file in the root directory and define the path to your
industry sources:

```bash
INDUSTRIES_PATH=Sources
```

If INDUSTRIES_PATH is not provided, the default value will be `Sources/`.

## Run the Compiler

When the compiler runs, it will scan the specified industry directory for YAML
files and validate them against the defined schema. If everything is correct
and the YAML files are properly formatted, it will generate Python classes in
the industries/ folder.

In order to run the compiler, just execute:

```bash
python src/main.py
```
