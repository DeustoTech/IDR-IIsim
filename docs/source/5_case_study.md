## Case Study: Cement Production

To illustrate the capabilities of IDR-IIsim, a complete model for the Cement Industry is
included in the `Sources/cement/` directory.

### Process Overview

The model follows a standard generic cement production process, divided into three
main stages (Sub-processes):

1. **Pre-homogenization and Grinding (Process 1)**: Handling of raw materials
like Limestone and Clay.
   - *Key Physics*: Mass balance of limestone/clay and electrical consumption
for crushing.
   - *Emissions*: PM10 dust from crushing.
2. **Oven / Clinkerization (Process 2)**: The core chemical reaction.
   - *Key Physics*: Calcination at 1,500°C. High thermal energy demand
(fuels) and water consumption for cooling.
   - *Emissions*: Significant CO2 emissions from chemical reactions and
combustion.

3. **Milling (Process 3)**: Final grinding of Clinker with Gypsum.
o Key Physics: Electrical energy for fine grinding.

### Implementation in IDR-IIsim

The theoretical model is mapped to files as follows:

- **Sources/cement/process2-oven.yaml**: Corresponds to Stage 2. It defines
constants like `CLINKER_LOSSES` (0.38) and `FUEL_HC` (0.02693 MJ/kg). It
calculates `clinker_production` and `heat_losses` based on the input mix.

- **Sources/cement/meta.yaml**: Represents the entire plant. It defines the
`outcome` (Total Cement Production) and aggregates the energy demands from
the oven and milling stages into a total `mechanical_energy` variable (approx.
115 MJ/ton for pre-processing, 69.5 MJ/ton for the oven, etc.).
