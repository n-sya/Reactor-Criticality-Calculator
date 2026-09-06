import json
from pathlib import Path

import pytest

from calculations import (
    calculate_multiplication_factor,
    classify_criticality,
)


TEST_CASES_PATH = Path(__file__).parent / "test_cases.json"


def load_test_cases():
    with TEST_CASES_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)["test_cases"]


@pytest.mark.parametrize(
    "test_case",
    load_test_cases(),
    ids=lambda test_case: test_case["name"],
)
def test_criticality_calculation(test_case):
    result = calculate_multiplication_factor(
        test_case["number_densities"],
        nuclear_data=test_case["nuclear_data"],
    )

    multiplication_factor = result["multiplication_factor"]
    expected = test_case["expected"]

    assert multiplication_factor == pytest.approx(
        expected["multiplication_factor"]
    )
    assert result["total_absorption"] == pytest.approx(
        expected["total_absorption"]
    )
    assert result["total_neutron_production"] == pytest.approx(
        expected["total_neutron_production"]
    )

    classification = classify_criticality(multiplication_factor)

    assert classification == expected["classification"]