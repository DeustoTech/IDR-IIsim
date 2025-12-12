## Usage Guide

### Running the Compiler
To process the YAML files and generate the code: `python src/main.py`

*Output*: This will generate a file `industries/cement.py`.

### Using the Generated Model in Python
Once compiled, the model can be imported and used in any Python script or Jupyter
Notebook.


we can view an example to illustrate how to use the models in a terminal:

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
