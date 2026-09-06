import unittest

from calculations import (
    barns_to_square_metres,
    calculate_multiplication_factor,
    classify_criticality,
    macroscopic_absorption_cross_section,
    neutron_production_cross_section,
)


class TestUnitConversion(unittest.TestCase):
    def test_barns_to_square_metres(self):
        result = barns_to_square_metres(1.0)

        self.assertAlmostEqual(result, 1e-28)


class TestMacroscopicAbsorption(unittest.TestCase):
    def test_u235_absorption(self):
        result = macroscopic_absorption_cross_section(
            3.00e25,
            683.0,
        )

        self.assertAlmostEqual(result, 2.049)


class TestNeutronProduction(unittest.TestCase):
    def test_u235_neutron_production(self):
        result = neutron_production_cross_section(
            3.00e25,
            587.0,
            2.43,
        )

        self.assertAlmostEqual(result, 4.27923)


class TestMultiplicationFactor(unittest.TestCase):
    def test_lecture_example(self):
        number_densities = {
            "Fe": 2.30e27,
            "H": 5.20e28,
            "O": 2.67e28,
            "Pu-239": 2.00e25,
            "U-235": 3.00e25,
            "U-238": 6.59e27,
            "Zr": 3.69e27,
        }

        result = calculate_multiplication_factor(number_densities)

        self.assertAlmostEqual(
            result["total_absorption"],
            8.280289,
            places=6,
        )
        self.assertAlmostEqual(
            result["total_neutron_production"],
            8.62343,
            places=5,
        )
        self.assertAlmostEqual(
            result["multiplication_factor"],
            1.0414407033,
            places=8,
        )


class TestCriticalityClassification(unittest.TestCase):
    def test_subcritical(self):
        self.assertEqual(classify_criticality(0.95), "Subcritical")

    def test_critical(self):
        self.assertEqual(classify_criticality(1.0), "Critical")

    def test_supercritical(self):
        self.assertEqual(classify_criticality(1.05), "Supercritical")


if __name__ == "__main__":
    unittest.main()