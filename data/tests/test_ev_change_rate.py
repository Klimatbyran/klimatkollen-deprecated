# -*- coding: utf-8 -*-
import unittest
import pandas as pd

from solutions.cars.ev_change_rate import get_ev_change_rate


class TestBicycleCalculations(unittest.TestCase):

    def test_get_ev_change_rate(self):
        df_expected = pd.DataFrame(
            {
                "Kommun": ["Ale"],
                "evChangeRate": [7.22114538969724],
                "evChangeYearly": [
                    {
                        2015: 2.64385692068429,
                        2016: 1.28865979381443,
                        2017: 1.64383561643836,
                        2018: 5.02873563218391,
                        2019: 7.08860759493671,
                        2020: 27.338129496402903,
                        2021: 41.7276720351391,
                        2022: 55.6171983356449,
                        2023: 54.9056603773585,
                        2024: 48.8612836438923,
                    }
                ],
            }
        )

        df_input = pd.DataFrame({"Kommun": ["Ale"]})
        df_result = get_ev_change_rate(df_input)

        pd.testing.assert_frame_equal(
            df_result.iloc[:3], df_expected, check_dtype=False, atol=0.01
        )


if __name__ == "__main__":
    unittest.main()
