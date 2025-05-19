import unittest
import json
from pathlib import Path
from unittest.mock import patch
import pandas as pd
from sector_emissions import (
    create_sector_emissions_dict,
    generate_sector_emissions_file,
)


class TestSectorEmissions(unittest.TestCase):
    """Test cases for sector emissions data processing and file generation."""

    def setUp(self):
        """Set up test data that will be used in multiple tests."""
        self.input_df = pd.DataFrame(
            {
                "Kommun": ["Ale", "Alingsås"],
                "2020_Transport": [56224.7124, 54756.95],
                "2020_Industri": [72722.13, 3492.44],
                "2021_Transport": [55911.56, 54401.87],
                "2021_Industri": [79064.9, 141.82],
            }
        )

    def test_create_sector_emissions_dict(self):
        """Test the creation of sector emissions dictionary with sample data."""
        result = create_sector_emissions_dict(self.input_df)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Ale")
        self.assertEqual(result[1]["name"], "Alingsås")

        # Check Ale's 2020 data
        self.assertEqual(result[0]["sectors"]["2020"]["Transport"], 56224.71)
        self.assertEqual(result[0]["sectors"]["2020"]["Industri"], 72722.13)

        # Check Alingsås's 2021 data
        self.assertEqual(result[1]["sectors"]["2021"]["Transport"], 54401.87)
        self.assertEqual(result[1]["sectors"]["2021"]["Industri"], 141.82)

        # Test with different number of decimals
        result_3_decimals = create_sector_emissions_dict(self.input_df, num_decimals=3)
        self.assertEqual(
            result_3_decimals[0]["sectors"]["2020"]["Transport"], 56224.712
        )

    def test_create_sector_emissions_dict_with_nulls(self):
        """Test sector emissions dictionary creation with null values in input data."""
        # Test data with null values
        input_df = pd.DataFrame(
            {
                "Kommun": ["Ale"],
                "2020_Transport": [56224.712],
                "2020_Industri": [None],
            }
        )

        result = create_sector_emissions_dict(input_df)
        self.assertEqual(result[0]["sectors"]["2020"]["Transport"], 56224.71)
        self.assertIsNone(result[0]["sectors"]["2020"]["Industri"])

    def test_generate_sector_emissions_file(self):
        """Test the generation of sector emissions JSON file with mocked data."""
        output_file = Path("test-sector-emissions.json")
        mock_df = pd.DataFrame(
            {
                "Kommun": ["Ale"],
                "2020_Transport": [56224.71],
                "2020_Industri": [72722.13],
            }
        )

        with patch("sector_emissions.get_smhi_data", return_value=mock_df), patch(
            "sector_emissions.extract_sector_data", return_value=mock_df
        ):
            generate_sector_emissions_file(str(output_file))
            self._verify_generated_file(output_file)
            output_file.unlink()

    def _verify_generated_file(self, output_file):
        """Verify the generated file exists and contains correct data."""
        self.assertTrue(output_file.exists())
        with open(output_file, "r", encoding="utf8") as file:
            data = json.load(file)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Ale")
        self.assertEqual(data[0]["sectors"]["2020"]["Transport"], 56224.71)
        self.assertEqual(data[0]["sectors"]["2020"]["Industri"], 72722.13)


if __name__ == "__main__":
    unittest.main()
