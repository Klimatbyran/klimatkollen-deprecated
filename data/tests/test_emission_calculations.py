# -*- coding: utf-8 -*-
import datetime
import unittest
import pandas as pd

from issues.emissions.emission_data_calculations import (
    calculate_historical_change_percent,
    deduct_cement,
    calculate_n_subtract_national_overheads,
    calculate_municipality_budgets,
    calculate_paris_path,
    calculate_needed_change_percent,
    calculate_hit_net_zero,
    calculate_budget_runs_out,
)
from issues.emissions.trend_calculations import (
    calculate_trend_coefficients,
    calculate_trend,
)
from issues.emissions.approximated_data_calculations import (
    calculate_approximated_historical,
)


LAST_YEAR_WITH_SMHI_DATA = 2021
CURRENT_YEAR = 2024
NATIONAL_BUDGET = 80e6
BUDGET_YEAR = 2024


class TestEmissionCalculations(unittest.TestCase):

    def test_deduct_cement(self):
        # Sample data frame for Skövde and Gotland
        df_input = pd.DataFrame(
            {
                "Kommun": ["Skövde", "Gotland"],
                2010: [546338.699134178, 1981476.17399167],
                2015: [494776.01973774, 2195403.90927869],
                2016: [532612.492354495, 2124789.02188846],
                2017: [543896.716984358, 2024382.31793093],
                2018: [586444.17315306, 2143010.50127022],
                2019: [576595.998007861, 1966304.75819611],
                2020: [567399.427902324, 1820053.10059352],
                2021: [571141.947070738, 1741013.9429687],
            }
        )

        df_expected = pd.DataFrame(
            {
                "Kommun": ["Skövde", "Gotland"],
                2010: [189373.699134178, 401665.17399167],
                2015: [136142.01973774, 269367.90927869],
                2016: [147686.492354495, 220902.02188846],
                2017: [136263.586984358, 267272.31793093],
                2018: [140813.83315306, 402598.50127022],
                2019: [136091.668007861, 429824.75819611],
                2020: [108306.954902324, 195590.10059352],
                2021: [131967.220070738, 119802.9429687],
            }
        )

        cement_deduction = {
            "Skövde": {
                2010: 356965000 / 1000,
                2015: 358634000 / 1000,
                2016: 384926000 / 1000,
                2017: 407633130 / 1000,
                2018: 445630340 / 1000,
                2019: 440504330 / 1000,
                2020: 459092473 / 1000,
                2021: 439174727 / 1000,
            },
            "Gotland": {
                2010: 1579811000 / 1000,
                2015: 1926036000 / 1000,
                2016: 1903887000 / 1000,
                2017: 1757110000 / 1000,
                2018: 1740412000 / 1000,
                2019: 1536480000 / 1000,
                2020: 1624463000 / 1000,
                2021: 1621211000 / 1000,
            },
        }

        df_result = deduct_cement(df_input, cement_deduction)

        pd.testing.assert_frame_equal(df_result, df_expected, check_dtype=False)

    def test_calculate_trend_coefficients(self):
        # Sample data frame for Norrköping
        df_input = pd.DataFrame(
            {
                "Kommun": ["Norrköping"],
                2015: [575029.197615897],
                2016: [587981.674412033],
                2017: [562126.750235607],
                2018: [567506.055574675],
                2019: [561072.598453251],
                2020: [511529.0569374],
                2021: [543303.129520453],
            }
        )

        df_expected = df_input.copy()
        df_expected["trendCoefficients"] = [[-8.89777111e03, 1.85140662e07]]

        df_result = calculate_trend_coefficients(df_input, LAST_YEAR_WITH_SMHI_DATA)

        pd.testing.assert_frame_equal(df_result, df_expected, check_exact=False)

    def test_calculate_approximated_historical(self):
        # Sample data frame for Norrköping
        df_input = pd.DataFrame(
            {
                "Kommun": ["Norrköping"],
                2015: [575029.197615897],
                2016: [587981.674412033],
                2017: [562126.750235607],
                2018: [567506.055574675],
                2019: [561072.598453251],
                2020: [511529.0569374],
                2021: [543303.129520453],
                "trendCoefficients": [[-8.89777111e03, 1.85140662e07]],
            }
        )

        df_expected = df_input.copy()
        df_expected["approximatedHistorical"] = [
            {
                2021: 543303.129520453,
                2022: 522772.98167590424,
                2023: 513875.21056812257,
                2024: 504977.43946033716,
            }
        ]
        df_expected["totalApproximatedHistorical"] = [1560788.47673442]

        df_result = calculate_approximated_historical(
            df_input, LAST_YEAR_WITH_SMHI_DATA, CURRENT_YEAR
        )

        pd.testing.assert_frame_equal(df_result, df_expected, check_exact=False)

    def test_calculate_trend(self):
        # Sample data frame for Norrköping
        df_input = pd.DataFrame(
            {
                "Kommun": ["Norrköping"],
                2015: [575029.197615897],
                2016: [587981.674412033],
                2017: [562126.750235607],
                2018: [567506.055574675],
                2019: [561072.598453251],
                2020: [511529.0569374],
                2021: [543303.129520453],
                "trendCoefficients": [[-8.89777111e03, 1.85140662e07]],
                "approximatedHistorical": [
                    {
                        2021: 543303.129520453,
                        2022: 522772.98167590424,
                        2023: 513875.21056812257,
                        2024: 504977.43946033716,
                    }
                ],
            }
        )

        df_expected = df_input.copy()
        df_expected["trend"] = [
            {
                2024: 504977.43946033716,
                2025: 496079.66835255176,
                2026: 487181.8972447701,
                2027: 478284.1261369847,
                2028: 469386.355029203,
                2029: 460488.5839214176,
                2030: 451590.8128136322,
                2031: 442693.0417058505,
                2032: 433795.2705980651,
                2033: 424897.4994902797,
                2034: 415999.728382498,
                2035: 407101.9572747126,
                2036: 398204.18616693094,
                2037: 389306.41505914554,
                2038: 380408.64395136014,
                2039: 371510.87284357846,
                2040: 362613.10173579305,
                2041: 353715.33062800765,
                2042: 344817.559520226,
                2043: 335919.78841244057,
                2044: 327022.0173046589,
                2045: 318124.2461968735,
                2046: 309226.4750890881,
                2047: 300328.7039813064,
                2048: 291430.932873521,
                2049: 282533.1617657356,
                2050: 273635.3906579539,
            }
        ]
        df_expected["trendEmission"] = [10121967.672179997]

        df_result = calculate_trend(df_input, LAST_YEAR_WITH_SMHI_DATA, CURRENT_YEAR)

        pd.testing.assert_frame_equal(df_result, df_expected, check_exact=False)

    def test_calculate_n_subtract_national_overheads(self):
        expected = 9
        result = calculate_n_subtract_national_overheads(10, 20, 2)
        assert result == expected

    def test_calculate_municipality_budgets(self):
        # Sample data frame for Municipality A and Municipality B
        df_input = pd.DataFrame(
            {
                "Kommun": ["Municipality A", "Municipality B"],
                2015: [40000, 200000],
                2016: [43000, 280000],
                2017: [45000, 310000],
                2018: [46000, 290000],
                2019: [46500, 350000],
                2020: [47800, 390000],
                2021: [50000, 400000],
            }
        )

        df_expected = df_input.copy()
        df_expected["budgetShare"] = [0.12539888902021, 0.87460111097979]
        df_expected["Budget"] = [10031911.1216168, 69968088.8783832]

        df_result = calculate_municipality_budgets(
            df_input,
            LAST_YEAR_WITH_SMHI_DATA,
            CURRENT_YEAR,
            NATIONAL_BUDGET,
            BUDGET_YEAR,
        )

        pd.testing.assert_frame_equal(df_result, df_expected, check_exact=False)

    def test_calculate_paris_path_remaining_budget(self):
        # Sample data frame for Norrköping
        df_input = pd.DataFrame(
            {
                "Kommun": ["Norrköping"],
                "Budget": [1157838.12807669],
                "trend": [
                    {
                        2024: 504977.43946033716,
                        2025: 496079.66835255176,
                        2026: 487181.8972447701,
                        2027: 478284.1261369847,
                        2028: 469386.355029203,
                        2029: 460488.5839214176,
                        2030: 451590.8128136322,
                        2031: 442693.0417058505,
                        2032: 433795.2705980651,
                        2033: 424897.4994902797,
                        2034: 415999.728382498,
                        2035: 407101.9572747126,
                        2036: 398204.18616693094,
                        2037: 389306.41505914554,
                        2038: 380408.64395136014,
                        2039: 371510.87284357846,
                        2040: 362613.10173579305,
                        2041: 353715.33062800765,
                        2042: 344817.559520226,
                        2043: 335919.78841244057,
                        2044: 327022.0173046589,
                        2045: 318124.2461968735,
                        2046: 309226.4750890881,
                        2047: 300328.7039813064,
                        2048: 291430.932873521,
                        2049: 282533.1617657356,
                        2050: 273635.3906579539,
                    }
                ],
            }
        )

        df_expected = df_input.copy()
        df_expected["parisPath"] = [
            {
                2024: 504977.43946033716,
                2025: 326482.2399151613,
                2026: 211080.0298206054,
                2027: 136469.22724080042,
                2028: 88231.22679833537,
                2029: 57043.991086745686,
                2030: 36880.558473274155,
                2031: 23844.32728825376,
                2032: 15416.0340126457,
                2033: 9966.90331440479,
                2034: 6443.8857359296035,
                2035: 4166.154929756807,
                2036: 2693.537348429262,
                2037: 1741.4483065820225,
                2038: 1125.895731969664,
                2039: 727.9235303605029,
                2040: 470.6232122627634,
                2041: 304.2712574641341,
                2042: 196.71999958028954,
                2043: 127.18506032213942,
                2044: 82.2287495102609,
                2045: 53.16321924049305,
                2046: 34.371529384136416,
                2047: 22.222168805472034,
                2048: 14.367262535801231,
                2049: 9.288842802859493,
                2050: 6.005500379855265,
            }
        ]

        df_result = calculate_paris_path(
            df_input, LAST_YEAR_WITH_SMHI_DATA, CURRENT_YEAR, BUDGET_YEAR
        )

        pd.testing.assert_frame_equal(df_result, df_expected, check_exact=False)

    def test_calculate_paris_path_no_budget(self):
        # Sample data frame for Norrköping
        df_input = pd.DataFrame(
            {
                "Kommun": ["Norrköping"],
                "Budget": [-1],
                "trend": [
                    {
                        2024: 504977.43946033716,
                        2025: 496079.66835255176,
                        2026: 487181.8972447701,
                        2027: 478284.1261369847,
                        2028: 469386.355029203,
                        2029: 460488.5839214176,
                        2030: 451590.8128136322,
                        2031: 442693.0417058505,
                        2032: 433795.2705980651,
                        2033: 424897.4994902797,
                        2034: 415999.728382498,
                        2035: 407101.9572747126,
                        2036: 398204.18616693094,
                        2037: 389306.41505914554,
                        2038: 380408.64395136014,
                        2039: 371510.87284357846,
                        2040: 362613.10173579305,
                        2041: 353715.33062800765,
                        2042: 344817.559520226,
                        2043: 335919.78841244057,
                        2044: 327022.0173046589,
                        2045: 318124.2461968735,
                        2046: 309226.4750890881,
                        2047: 300328.7039813064,
                        2048: 291430.932873521,
                        2049: 282533.1617657356,
                        2050: 273635.3906579539,
                    }
                ],
            }
        )

        df_expected = df_input.copy()
        df_expected["parisPath"] = None

        df_result = calculate_paris_path(
            df_input, LAST_YEAR_WITH_SMHI_DATA, CURRENT_YEAR, BUDGET_YEAR
        )

        pd.testing.assert_frame_equal(df_result, df_expected, check_exact=False)

    def test_calculate_historical_change_percent(self):
        # Sample data frame for Östersund
        df_input = pd.DataFrame(
            {
                "Kommun": ["Östersund"],
                2015: [143786.390451667],
                2016: [136270.272900585],
                2017: [134890.137836385],
                2018: [123096.170608436],
                2019: [113061.651497606],
                2020: [94746.1396597532],
                2021: [95248.2864179093],
            }
        )

        df_expected = df_input.copy()
        df_expected["historicalEmissionChangePercent"] = [-6.46746990789292]

        df_result = calculate_historical_change_percent(
            df_input, LAST_YEAR_WITH_SMHI_DATA
        )

        pd.testing.assert_frame_equal(df_result, df_expected, check_exact=False)

    def test_calculate_needed_change_percent(self):
        # Sample data frame for Jokkmokk
        df_input = pd.DataFrame(
            {
                "Kommun": ["Jokkmokk"],
                "Budget": 1e10,
                "parisPath": [
                    {
                        2024: 22187.783636475913,
                        2025: 16425.542706550976,
                        2026: 12159.77483939365,
                        2027: 9001.841022018716,
                        2028: 6664.033080874027,
                        2029: 4933.361608404003,
                        2030: 3652.15125193863,
                        2031: 2703.675470355793,
                        2032: 2001.5219920378186,
                        2033: 1481.7200986344162,
                        2034: 1096.9124793187386,
                        2035: 812.0406738047835,
                        2036: 601.1510201095242,
                        2037: 445.0301082647478,
                        2038: 329.4543145348899,
                        2039: 243.893937398689,
                        2040: 180.55387371026865,
                        2041: 133.66343443992008,
                        2042: 98.95059762020891,
                        2043: 73.25279954404822,
                        2044: 54.22880477828064,
                        2045: 40.14540448945623,
                        2046: 29.71950992118386,
                        2047: 22.001254718639636,
                        2048: 16.287455966742968,
                        2049: 12.05754968346613,
                        2050: 8.92616407781006,
                    }
                ],
            }
        )

        df_expected = df_input.copy()
        df_expected["neededEmissionChangePercent"] = [25.970331351402]

        df_result = calculate_needed_change_percent(df_input, CURRENT_YEAR, BUDGET_YEAR)

        pd.testing.assert_frame_equal(df_result, df_expected, check_exact=False)

        # Sample data frame for Jokkmokk
        df_input = pd.DataFrame(
            {
                "Kommun": ["Jokkmokk"],
                "Budget": -1,
                "parisPath": [
                    {
                        2024: 22187.783636475913,
                        2025: 16425.542706550976,
                        2026: 12159.77483939365,
                        2027: 9001.841022018716,
                        2028: 6664.033080874027,
                        2029: 4933.361608404003,
                        2030: 3652.15125193863,
                        2031: 2703.675470355793,
                        2032: 2001.5219920378186,
                        2033: 1481.7200986344162,
                        2034: 1096.9124793187386,
                        2035: 812.0406738047835,
                        2036: 601.1510201095242,
                        2037: 445.0301082647478,
                        2038: 329.4543145348899,
                        2039: 243.893937398689,
                        2040: 180.55387371026865,
                        2041: 133.66343443992008,
                        2042: 98.95059762020891,
                        2043: 73.25279954404822,
                        2044: 54.22880477828064,
                        2045: 40.14540448945623,
                        2046: 29.71950992118386,
                        2047: 22.001254718639636,
                        2048: 16.287455966742968,
                        2049: 12.05754968346613,
                        2050: 8.92616407781006,
                    }
                ],
            }
        )

        df_expected = df_input.copy()
        df_expected["neededEmissionChangePercent"] = None

        df_result = calculate_needed_change_percent(df_input, CURRENT_YEAR, BUDGET_YEAR)

        pd.testing.assert_frame_equal(df_result, df_expected, check_exact=False)

    def test_calculate_hit_net_zero(self):
        # Sample DataFrame for municipalitis 'Ale' and 'Alingsås'
        df_input = pd.DataFrame(
            {
                "Kommun": ["Ale", "Alingsås"],
                "trendCoefficients": [
                    [7.82334178e02, -1.43894275e06],
                    [-1.97662497e03, 4.06091905e06],
                ],
            }
        )

        df_expected = df_input.copy()
        df_expected["hitNetZero"] = [None, datetime.date(2054, 6, 13)]

        df_result = calculate_hit_net_zero(df_input, LAST_YEAR_WITH_SMHI_DATA)

        pd.testing.assert_frame_equal(df_result, df_expected, check_exact=False)

    def test_budget_runs_out(self):
        # Sample DataFrame for municipality 'Ale'
        df_input = pd.DataFrame(
            {
                "Kommun": ["Ale"],
                "trend": [
                    {
                        2024: 144501.62223702623,
                        2025: 145283.9564149473,
                        2026: 146066.29059286858,
                        2027: 146848.62477078964,
                        2028: 147630.95894871093,
                        2029: 148413.293126632,
                        2030: 149195.6273045533,
                        2031: 149977.96148247435,
                        2032: 150760.2956603954,
                        2033: 151542.6298383167,
                        2034: 152324.96401623776,
                        2035: 153107.29819415906,
                        2036: 153889.63237208012,
                        2037: 154671.96655000118,
                        2038: 155454.30072792247,
                        2039: 156236.63490584353,
                        2040: 157018.96908376482,
                        2041: 157801.30326168588,
                        2042: 158583.63743960718,
                        2043: 159365.97161752824,
                        2044: 160148.3057954493,
                        2045: 160930.6399733706,
                        2046: 161712.97415129165,
                        2047: 162495.30832921294,
                        2048: 163277.642507134,
                        2049: 164059.97668505507,
                        2050: 164842.31086297636,
                    }
                ],
                "trendCoefficients": [[7.82334178e02, -1.43894275e06]],
                "Budget": [286595.380915185],
            }
        )

        df_expected = df_input.copy()
        df_expected["budgetRunsOut"] = [datetime.date(2025, 12, 22)]

        df_result = calculate_budget_runs_out(df_input, CURRENT_YEAR, BUDGET_YEAR)

        pd.testing.assert_frame_equal(df_result, df_expected, check_exact=False)


if __name__ == "__main__":
    unittest.main()
