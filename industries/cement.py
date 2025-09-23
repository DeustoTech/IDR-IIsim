""" Meta archivo de la industria del cemento """

# Constants
NAME = "Cement industry"
# Cement industry's constants
LIMESTONE_PROPORTION = 1.035  # limestone proportion
CLAY_PROPORTION = 0.375  # Clay proportion
MECHANICAL_ENERGY_PRE_PROPORTION = 0.11592  # Mechanical Energy pre proportion
WATER_PROPORTION = 0.222  # Water proportion
FUEL_PROPORTION = 0.13  # Fuel proportion
MECHANICAL_ENERGY_OVEN_PROPORTION = 0.069552  # Mechanical Energy oven proportion
GYPSUM_PROPORTION = 0.04  # Gypsum proportion
MECHANICAL_ENERGY_MILLING_PROPORTION = 0.135792  # Mechanical Energy used by the process
CO2_EMISSIONS_PROPORTION = 0.9  # CO2
# Pre-homogenization and grinding's constants
LIMESTONE_LOSSES = 0.01  # Limestone losses
CLAY_LOSSES = 0.01  # Loss clay
# Oven's constants
CLINKER_LOSSES = 0.38  # Loss Clinker
FUEL_HC = 0.02693  # Fuel HC
ENERGY_LOSSES = 0.1871  # Energy losses
# Milling's constants
CEMENT_LOSSES = 0.01  # Cement losses

# units
UNITS = {
    "total_cement_production": "kt",
    "limestone_demand": "kt",
    "clay_demand": "kt",
    "fuel_demand": "kt",
    "water_demand": "m3",
    "gypsum_demand": "kt",
    "mechanical_energy": "GJ",
    "co2_overall_emissions": "kt",
    "heat_overall_losses": "GJ",
    "pm10_overall_emission": "kt"
}

class Cement:
    """ Cement industry """

    def __init__(self, total_cement_production):
        """ constructor """
        self.__validate_total_production(total_cement_production)
        self.__total_cement_production = total_cement_production
        self.__limestone_demand = self.__total_cement_production * LIMESTONE_PROPORTION
        self.__clay_demand = self.__total_cement_production * CLAY_PROPORTION
        self.__mechanical_energy_pre = self.__total_cement_production * MECHANICAL_ENERGY_PRE_PROPORTION
        self.__pre_homogeneization_and_grinding(self.__limestone_demand, self.__clay_demand)
        self.__fuel_demand = self.__total_cement_production * FUEL_PROPORTION
        self.__water_demand = self.__total_cement_production * WATER_PROPORTION
        self.__mechanical_energy_oven = self.__total_cement_production * MECHANICAL_ENERGY_OVEN_PROPORTION
        self.__oven(self.__pm10_emission_pre, self.__fuel_demand, self.__raw_mix)
        self.__gypsum_demand = self.__clinker_production_oven * GYPSUM_PROPORTION
        self.__mechanical_energy_milling = self.__total_cement_production * MECHANICAL_ENERGY_MILLING_PROPORTION
        self.__milling(self.__clinker_production_oven, self.__gypsum_demand)
        self.__mechanical_energy = self.__mechanical_energy_pre + self.__mechanical_energy_oven + self.__mechanical_energy_milling
        self.__co2_overall_emissions = total_cement_production * CO2_EMISSIONS_PROPORTION
        self.__heat_overall_losses = self.__heat_losses_oven
        self.__pm10_overall_emission = (self.__pm10_emission_pre + self.__pm10_emission_oven + self.__cement_emission)

    def __validate_total_production(self, total_cement_production) -> None:
        if total_cement_production < 5 or total_cement_production > 1000:
            raise ValueError(
                "The production should be a value between 5 and 1000"
            )

    def __pre_homogeneization_and_grinding(self, limestone_demand, clay_demand) -> None:
        """ Pre-homogenization and grinding handling of raw materials """
        self.__pm10_emission_pre = CLAY_LOSSES*clay_demand + LIMESTONE_LOSSES*limestone_demand
        self.__raw_mix = clay_demand + limestone_demand - self.__pm10_emission_pre

    def __oven(self, pm10_emission_pre, fuel_demand, raw_mix) -> None:
        """ OVEN - Calcination, clinkerization, combustion, cooling """
        self.__pm10_emission_oven = pm10_emission_pre
        self.__heat_losses_oven = ENERGY_LOSSES*FUEL_HC*fuel_demand
        self.__clinker_production_oven = raw_mix*(1 - CLINKER_LOSSES)

    def __milling(self, clinker_production_oven, gypsum_demand) -> None:
        """ Milling """
        self.__cement_emission = CEMENT_LOSSES*(clinker_production_oven + gypsum_demand)
        self.__cement_production = (1 - CEMENT_LOSSES)*(clinker_production_oven + gypsum_demand)

    def get_total_cement_production(self) -> float:
        """ Total cement production """
        return self.__total_cement_production

    def get_limestone_demand(self) -> float:
        """ Total limestone demand """
        return self.__limestone_demand

    def get_clay_demand(self) -> float:
        """ Total clay demand """
        return self.__clay_demand

    def get_fuel_demand(self) -> float:
        """ Total fuel demand """
        return self.__fuel_demand

    def get_water_demand(self) -> float:
        """ Total water demand """
        return self.__water_demand

    def get_gypsum_demand(self) -> float:
        """ gympsum total demand """
        return self.__gypsum_demand

    def get_mechanical_energy(self) -> float:
        """ Total mechanical energy """
        return self.__mechanical_energy

    def get_co2_overall_emissions(self) -> float:
        """ Total C02 emissions """
        return self.__co2_overall_emissions

    def get_heat_overall_losses(self) -> float:
        """ Total Heat losses """
        return self.__heat_overall_losses

    def get_pm10_overall_emission(self) -> float:
        """ Total PM10 emissions """
        return self.__pm10_overall_emission

    def csv(self, separator: str = ";") -> None:
        """ print the industry as CSV format """
        attributes = vars(self)
        lines = [[], []]
        for name, value in attributes.items():
            name = name.replace(f"_{self.__class__.__name__}__", "")
            if name in UNITS:
                unit = UNITS[name]
                lines[0].append(name)
                lines[1].append(str(value))
                lines[0].append(name + "_unit")
                lines[1].append(unit)
        for line in lines:
            print(separator.join(line))

    def csv_header(self) -> list:
        attributes = vars(self)
        line = []
        for name in attributes:
            name = name.replace(f"_{self.__class__.__name__}__", "")
            if name in UNITS:
                unit = UNITS[name]
                line.append(f"{name} ({unit})")
        return line

    def csv_row(self) -> list:
        attributes = vars(self)
        line = []
        for name, value in attributes.items():
            name = name.replace(f"_{self.__class__.__name__}__", "")
            if name in UNITS:
                line.append(str(value))
        return line

    def __str__(self) -> str:
        final_str = NAME
        final_str += "\n" + "-" * len(final_str) + "\n"
        attributes = vars(self)
        for name, value in attributes.items():
            name = name.replace(f"_{self.__class__.__name__}__", "")
            if name in UNITS:
                unit = UNITS[name]
                print_name = name.replace("_", " ").title()
                final_str += f"{print_name}: {value:.2f} {unit}\n"
        return final_str
