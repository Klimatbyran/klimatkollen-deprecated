# -*- coding: utf-8 -*-
import unittest
import pandas as pd

from issues.consumption.consumption_emissions import get_consumption_emissions


class TestConsumtionEmissionsCalculations(unittest.TestCase):
    """Test class for consumption emissions calculations."""

    def test_get_consumption_emissions(self):
        """Test that get_consumption_emissions returns correct data."""
        df_expected = pd.DataFrame(
            {
                "Kommun": ["Ale", "Alingsås", "Alvesta"],
                "consumptionEmissions": [
                    5585,
                    5528,
                    5157,
                ],
            }
        )

        df_result = get_consumption_emissions()

        pd.testing.assert_frame_equal(
            df_result.iloc[:3], df_expected, check_dtype=False
        )


if __name__ == "__main__":
    unittest.main()
