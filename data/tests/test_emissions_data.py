# -*- coding: utf-8 -*-
import unittest
import pandas as pd

from issues.emissions.historical_data_calculations import get_smhi_data
from issues.emissions.historical_data_calculations import get_n_prep_data_from_smhi

LAST_YEAR_WITH_SMHI_DATA = 2023
CURRENT_YEAR = 2025
NATIONAL_BUDGET = 80e6
BUDGET_YEAR = 2024

PATH_SMHI = "https://nationellaemissionsdatabasen.smhi.se/api/getexcelfile/?county=0&municipality=0&sub=CO2"


class TestEmissionData(unittest.TestCase):

    def test_get_smhi_data(self):
        """Test that the SMHI data has the correct values.
        Update test when new emissions data is released.
        Reason for test was issues with incorrect data being provided by SMHI"""
        df_full_dataset = get_smhi_data(PATH_SMHI)

        # Filter for municipalities Ale and Skövde,
        # where Huvudsektor is Alla and years 2022 and 2023
        # Also reset index
        df_result = df_full_dataset[
            (df_full_dataset["Kommun"].isin(["Ale", "Skövde"]))
            & (df_full_dataset["Huvudsektor"] == "Alla")
        ][["Kommun", 2022, 2023]].reset_index(drop=True)

        print(df_result.head())

        df_expected = pd.DataFrame(
            {
                "Kommun": ["Ale", "Skövde"],
                2022: [127275.382, 536185.9645],
                2023: [121635.2675, 470188.5876],
            }
        )

        pd.testing.assert_frame_equal(df_result, df_expected)

    def test_get_n_prep_data_from_smhi(self):
        """Test that the N-prep data has the correct columns and positive values."""
        path_input_df = "tests/reference_dataframes/df_municipalities.xlsx"

        df_input = pd.DataFrame(pd.read_excel(path_input_df))
        df_result = get_n_prep_data_from_smhi(df_input)
        result_columns = df_result.columns.to_list()[4:]  # Skip the first 4 columns
        expected_columns = [
            1990,
            2000,
            2005,
            2010,
            2015,
            2016,
            2017,
            2018,
            2019,
            2020,
            2021,
            2022,
            2023,
        ]

        # Check that the expected columns are in the dataframe
        assert result_columns == expected_columns

        # Each of the column values should all be greater than 0.0
        for col in expected_columns:
            assert (df_result[col] > 0.0).all() == True
