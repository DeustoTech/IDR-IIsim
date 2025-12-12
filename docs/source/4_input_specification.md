## Input Data Specification

*(YAML Schema)*

The model is built entirely from YAML files. To define a complete industry (e.g.,
Cement), you need a hierarchical structure consisting of Process Files (sub-units) and a
Meta File (the industry aggregator). In this chapter the cement industry is used as an
example.

### Common Structure (Process & Industry)

All files share a common header for identification and versioning.

```yaml
id: Cemento-process2-Oven # Unique ID
name: Oven # Human-readable name
type: process # 'process' or 'industry'
version: 1.0.0
```

### The *Process* Model

A Process file describes a single physical unit (e.g., a Oven, a Grinder).
It transforms inputs into outputs.

#### Constants *(constants)*

Fixed parameters of the physics or chemistry (e.g., loss factors, heating values).

- **name**: A name of the constant is necessary. A strategy to name the constant is
recommended.
- **description**: A brief description of the constant is optional.
- **value**: Must be a number.
- **units**: Must be a streamlined.
- **source**: Required for traceability (URL or text citation).

YAML example:

```yaml
constants:
  - name: FUEL_HC
    description: Heat Capacity of the fuel
    value: 0.02693
    units: MJ/kg
    source: https://www.google.com
```

#### Inputs *(inputs)*

External variables needed to run the process.

- value:
  - `null`: Indicates this is a variable provided by the user at runtime (e.g.,
the amount of production).
  - `[Array]`: A list of numbers. This allows the model to handle vectors
    (e.g., time-series data or sensitivity analysis scenarios).
- from: Indicates where this input comes from (e.g., the output of a previous
process).

```yaml
inputs:
  - name: raw_mix
    value: null # Calculated from previous step
    from: Cemento-process1-Pre
    units: kt
```

#### Outputs *(outputs)*

The results calculated by this process.

- **operation**: A SymPy-compatible mathematical string.
- **args**: A critical list that maps the variables used in the operation to their type
(inputs or constants). This ensures no undefined variables are used.

```yaml
outputs:
  - name: heat_losses_oven
    # The mathematical logic:
    operation: fuel_demand * FUEL_HC * ENERGY_LOSSES
    args:
      - name: fuel_demand
        type: inputs
      - name: FUEL_HC
        type: constants
      - name: ENERGY_LOSSES
        type: constants
    units: GJ
```

### The *Industry* Model *(Meta-file)*

The Industry file (type: industry) aggregates multiple processes. It contains specific
sections to define system-level results.

#### Outcome *(outcome)*

The main product of the industry (e.g., "Total Cement Production"). This is the "driver"
variable that initiates the calculation chain.

#### Demands *(demands)*

Aggregates resources required by specific sub-processes.

- **used**: Specifies which sub-process consumes this resource.
- **meta**: (Optional) A tag used to group similar demands (e.g., tagging electricity
usage in the kiln and the grinder both as mechanical_energy).

```yaml
demands:
  - name: mechanical_energy_oven
    operation: total_cement_production * MECHANICAL_ENERGY_OVEN_PROPORTION
    used: Cemento-process2-Oven
    meta: mechanical_energy # Groups this into total energy
    units: GJ
```

#### Meta-Demands *(meta)*

Calculates totals based on the meta tags defined in demands.

- Example: Summing up mechanical energy from the Pre-processor, Oven, and
Grinder.

```yaml
meta:
  - name: mechanical_energy
    operation: mechanical_energy_pre + mechanical_energy_oven + mechanical_energy_milling
    description: Total mechanical energy consumption of the plant
```
