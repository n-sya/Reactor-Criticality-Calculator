import json

from variables import (
    BARN_TO_SQUARE_METRE,
    CRITICALITY_TOLERANCE,
    NUCLEAR_DATA_PATH,
)


# Load the thermal neutron cross-section data
def load_nuclear_data():
    with NUCLEAR_DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


# Convert a microscopic cross section from barns to square metres
def barns_to_square_metres(cross_section_barns):
    if cross_section_barns < 0:
        raise ValueError("Cross section must not be negative.")

    return cross_section_barns * BARN_TO_SQUARE_METRE


# Calculate the macroscopic absorption cross section for one species
def macroscopic_absorption_cross_section(
    number_density,
    absorption_cross_section_barns,
):
    if number_density < 0:
        raise ValueError("Number density must not be negative.")

    microscopic_cross_section = barns_to_square_metres(
        absorption_cross_section_barns
    )

    return number_density * microscopic_cross_section


# Calculate the neutron-production contribution for one species
def neutron_production_cross_section(
    number_density,
    fission_cross_section_barns,
    neutrons_per_fission,
):
    if number_density < 0:
        raise ValueError("Number density must not be negative.")

    if neutrons_per_fission < 0:
        raise ValueError("Neutrons per fission must not be negative.")

    fission_cross_section = barns_to_square_metres(
        fission_cross_section_barns
    )

    return neutrons_per_fission * number_density * fission_cross_section


# Calculate the zero-leakage multiplication factor
def calculate_multiplication_factor(number_densities, nuclear_data=None):
    if nuclear_data is None:
        nuclear_data = load_nuclear_data()

    total_absorption = 0.0
    total_neutron_production = 0.0
    contributions = {}

    for species, number_density in number_densities.items():
        if species not in nuclear_data:
            raise ValueError(f"Unknown species: {species}")

        if number_density < 0:
            raise ValueError(
                f"Number density for {species} must not be negative."
            )

        species_data = nuclear_data[species]

        absorption = macroscopic_absorption_cross_section(
            number_density,
            species_data["absorption_cross_section_barns"],
        )

        neutron_production = neutron_production_cross_section(
            number_density,
            species_data["fission_cross_section_barns"],
            species_data["neutrons_per_fission"],
        )

        total_absorption += absorption
        total_neutron_production += neutron_production

        contributions[species] = {
            "number_density": number_density,
            "macroscopic_absorption": absorption,
            "neutron_production": neutron_production,
        }

    if total_absorption <= 0.0:
        raise ValueError(
            "Total macroscopic absorption cross section must be greater than zero."
        )

    multiplication_factor = total_neutron_production / total_absorption

    return {
        "multiplication_factor": multiplication_factor,
        "total_absorption": total_absorption,
        "total_neutron_production": total_neutron_production,
        "contributions": contributions,
    }


# Classify the multiplication factor
def classify_criticality(
    multiplication_factor,
    tolerance=CRITICALITY_TOLERANCE,
):
    if multiplication_factor < 0:
        raise ValueError("Multiplication factor must not be negative.")

    if abs(multiplication_factor - 1.0) <= tolerance:
        return "Critical"

    if multiplication_factor < 1.0:
        return "Subcritical"

    return "Supercritical"