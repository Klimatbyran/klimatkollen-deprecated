import unittest
import os
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal, assert_index_equal


class TestDataToXlsx(unittest.TestCase):

    def setUp(self):
        self.calculations_file = "data/solutions/cars/sources/kpi1_calculations.xlsx"
        self.output_file = "data/output/trafa-output.xlsx"
        
    def test_validate_previous_data(self):
        excel_data = pd.read_excel(self.calculations_file, sheet_name="Antal nya laddbilar")
        comparison_data_2015 = pd.read_excel(self.output_file, sheet_name="Personbilar-2016")
        data_2015 = excel_data.iloc[::1, :4]
        data_2016 = excel_data.iloc[::1, 1::3]
        data_2015.columns = data_2015.iloc[1]
        data_2015 = data_2015.drop([0, 1, len(data_2015) -1])
        print(data_2016)
        # first four columns of the data
        compare_data = comparison_data_2015.iloc[::1, :4]
        # print(compare_data)
        missing = [
            "Bjurholm"
            "Bräcke"
            "Dorotea"
            "Jokkmokk"
            "Malå"
            "Munkfors"
            "Nordmaling"
            "Sorsele"
            "Storfors"
            "Älvdalen"
            "Ödeshög"]

        kommuner = data_2015["Kommun"]
        kommuner_compare = compare_data["Kommun"]

        for komun in kommuner:
            if komun not in kommuner_compare.values and komun in missing:
                print(komun)
                
        # print(compare_data[~data_2015.isin(compare_data)].dropna())
        
        
        

         
        
        # for i in range(4):
        #  assert_series_equal(data_2015.iloc[:, i], compare_data.iloc[:, i], check_dtype=False)

       
        
   
if __name__ == '__main__':
    unittest.main()