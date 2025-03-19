# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import os
import pandas as pd
from pandas.testing import assert_frame_equal
from trafa.data_to_xlsx import process_json_files
class TestDataToXlsx(unittest.TestCase):

    def setUp(self):
        self.folder_path = 'data/tests/reference_dataframes'
        self.output_file = 'data/tests/reference_dataframes/output.xlsx'
        self.expected_output_file = 'data/tests/reference_dataframes/expected_output.xlsx'


    def test_process_json_files(self):
        # Call the function to process the JSON files
        process_json_files(self.folder_path, self.output_file)

        # Read the expected output file and the generated output file
        expected_df = pd.read_excel(self.expected_output_file, sheet_name=None)
        generated_df = pd.read_excel(self.output_file, sheet_name=None)

        # Assert that the generated output matches the expected output
        for sheet_name in expected_df.keys():
            assert_frame_equal(generated_df[sheet_name], expected_df[sheet_name])

        # Clean up the generated output file
        os.remove(self.output_file)

if __name__ == '__main__':
    unittest.main()