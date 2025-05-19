# pylint: disable=invalid-name
# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

from issues.emissions.historical_data_calculations import get_n_prep_data_from_smhi
from issues.emissions.approximated_data_calculations import (
    calculate_approximated_historical,
)
from issues.emissions.trend_calculations import (
    calculate_trend_coefficients,
    calculate_trend,
)


CURRENT_YEAR = 2025  # current year
YEAR_SECONDS = 60 * 60 * 24 * 365  # a year in seconds


LAST_YEAR_WITH_SMHI_DATA = (
    2023  # last year for which the National Emission database has data
)
PATH_SMHI = "https://nationellaemissionsdatabasen.smhi.se/api/getexcelfile/?county=0&municipality=0&sub=CO2"


# ------- NATIONAL CARBON BUDGETS AND OVERHEADS -------

# Numbers below from
# https://www.cemus.uu.se/wp-content/uploads/2023/12/Paris-compliant-carbon-budgets-for-Swedens-counties-.pdf
# Found in tables on page 10 and 19. The numbers are in metric tonnes.

# National C02 budget for 50% chance of staying below 1.5 degrees
NATIONAL_BUDGET_15 = 80e6
# National C02 budget for 50% chance of staying below 1.7 degrees
NATIONAL_BUDGET_17 = 285e6
# National overhead for 1.7 degree scenario, 53 433 000 + 1 364 000 rounded to match preciseness of the other numbers
NATIONAL_OVERHEAD_17 = 55e6
# Year from which the carbon budgets applies
BUDGET_YEAR = 2024


# ------- CEMENT CARBON EMISSIONS -------

# Sources for cement deduction
# Mörbylånga: https://utslappisiffror.naturvardsverket.se/sv/Sok/Anlaggningssida/?pid=1441
# Skövde: https://utslappisiffror.naturvardsverket.se/sv/Sok/Anlaggningssida/?pid=5932
# Gotland: https://utslappisiffror.naturvardsverket.se/sv/Sok/Anlaggningssida/?pid=834

CEMENT_DEDUCTION = {
    "Mörbylånga": {
        2010: 248025000 / 1000,
        2015: 255970000 / 1000,
        2016: 239538000 / 1000,
        2017: 255783000 / 1000,
        2018: 241897000 / 1000,
        2019: 65176000 / 1000,
        2020: 0,
        2021: 0,
        2022: 0,
        2023: 0,
    },
    "Skövde": {
        2010: 356965000 / 1000,
        2015: 358634000 / 1000,
        2016: 384926000 / 1000,
        2017: 407633130 / 1000,
        2018: 445630340 / 1000,
        2019: 440504330 / 1000,
        2020: 459092473 / 1000,
        2021: 439174727 / 1000,
        2022: 406856000 / 1000,
        2023: 340611000 / 1000,
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
        2022: 1514132000 / 1000,
        2023: 1511971000 / 1000,
    },
}


def deduct_cement(df, cement_deduction):
    """
    Deducts cement emissions from the given DataFrame based on the provided cement deduction values.

    Args:
        df (pandas.DataFrame): The DataFrame containing the emission data.
        cement_deduction (dict): A dictionary specifying the cement
                                 deduction values for each municipality.

    Returns:
        pandas.DataFrame: The DataFrame with the cement emissions deducted.
    """

    df_cem = df.copy()

    # Deduct cement from given municipalities
    for i in cement_deduction.keys():
        for j in cement_deduction[i].keys():
            df_cem.loc[df_cem["Kommun"] == i, j] = (
                df_cem.loc[df_cem["Kommun"] == i, j].values - cement_deduction[i][j]
            )

    return df_cem


def calculate_n_subtract_national_overheads(
    national_budget_15, national_budget_17, national_overhead_17
):
    """
    This function calculates national overheads for a 1.5 degree scenario carbon budget
    and then subtracts it from corresponding national carbon budget.
    It uses the known values for national CO2 budgets for 1.5 and 1.7 degree scenarios,
    as well as the national overhead for the 1.7 degree scenario.

    Returns:
        float: The calculated national CO2 budget for a 1.5 degree scenario.
    """

    # Calculate national overhead for 1.5 degree scenario in metric tonnes
    national_overhead_15 = (
        national_overhead_17 / national_budget_17
    ) * national_budget_15
    # Subtract national overhead from national budget for 1.5 degree scenario
    return national_budget_15 - national_overhead_15


def calculate_municipality_budgets(
    df, last_year_in_range, current_year, budget, budget_year
):
    """
    Calculates the budget for each municipality based on emission data.

    Args:
        df (pandas.DataFrame): The input DataFrame containing emission data.

    Returns:
        pandas.DataFrame: The updated DataFrame with the calculated budgets for each municipality.
    """

    # Apply GF (grand fathering) to get the share of the budget for each municipality
    # GF is based on SMHI data from 2015 onwards
    years_range_gf = range(2015, last_year_in_range + 1)
    df["budgetShare"] = (
        df[years_range_gf].sum(axis=1) / df[years_range_gf].sum(axis=0).sum()
    )

    # Each municipality gets its share of the budget
    df["Budget"] = budget * df["budgetShare"]

    # Get years passed since the year the budget starts "eating"
    all_years_since_budget = list(range(budget_year, current_year))

    # Separate years with recorded data from years with approximated data
    recorded_years_since_budget = [
        x for x in all_years_since_budget if x <= last_year_in_range
    ]
    approximated_years_since_budget = [
        x for x in all_years_since_budget if x > last_year_in_range
    ]

    # Subtract emissions from budget for years that have passed since the budget started "eating"
    # For recorded values, subtract values as is
    for item in recorded_years_since_budget:
        df["Budget"] = df["Budget"] - df[item]
    # For approximated values, subtract total emission from approximated years since budget
    temp = []
    if approximated_years_since_budget:
        for i in range(len(df)):
            # Get index in approximated historical series for
            # the year from which emissions need to be subtracted
            approximated_years = list(df.iloc[i]["approximatedHistorical"].keys())
            start_subtract_year_idx = approximated_years.index(
                approximated_years_since_budget[0]
            )
            # Get approximated values and years since budget
            y_approx = list(df.iloc[i]["approximatedHistorical"].values())[
                start_subtract_year_idx:
            ]
            x_approx = list(df.iloc[i]["approximatedHistorical"].keys())[
                start_subtract_year_idx:
            ]

            # Get the cumulative emissions from the approximated historical data,
            # starting from the year approximated values needs to be subtracted from the budget
            approx_emissions_since_budget = np.trapz(y_approx, x_approx)

            temp.append(approx_emissions_since_budget)
        df["Budget"] = df["Budget"] - temp

    return df


def calculate_paris_path(df, last_year_in_range, current_year, budget_year):
    """
    Calculate the exponential curve that satisfies each municipality's budget.

    Args:
        df (pandas.DataFrame): The input DataFrame containing emission data.

    Returns:
        pandas.DataFrame: The input DataFrame with an additional column 'parisPath' that
        contains the exponential path of needed emissions decrease for each municipality
        in order to comply with the Paris 1.5 degree goal.
    """

    # Year from which the budget applies
    # (after correction with respect to years passed since budget start)
    first_year = max(budget_year, current_year)

    temp = []
    for i in range(len(df)):
        # Check if the budget is 0 or negative
        if df.iloc[i]["Budget"] <= 0:
            temp.append(None)  # Set parisPath to None
            continue  # Skip to the next municipality

        # We'll store the exponential path for each municipality in a dictionary
        # where the keys are the years
        dicts = {}
        # Years range will be set to from when the budget applies until 2050
        years_range = range(first_year, 2050 + 1)

        for year in years_range:
            # Calculate what the emission level has to be at future year
            # if one were to follow the exponential decay curve
            # If data has been recorded for the year the budget kicks in, use recorded values
            if first_year <= last_year_in_range:
                dicts[year] = df.iloc[i][first_year] * np.exp(
                    -(df.iloc[i][first_year])
                    / (df.iloc[i]["Budget"])
                    * (year - first_year)
                )
            else:  # If no data has been recorded for the year the budget kicks in, use trend values
                dicts[year] = df.iloc[i]["trend"][first_year] * np.exp(
                    -(df.iloc[i]["trend"][first_year])
                    / (df.iloc[i]["Budget"])
                    * (year - first_year)
                )
        temp.append(dicts)

    df["parisPath"] = temp

    return df


def calculate_historical_change_percent(df, last_year_in_range):
    """
    Calculate the historical average emission level change based on SMHI data from 2015 onwards.

    Args:
        df (pandas.DataFrame): The input DataFrame containing emission data.

    Returns:
        pandas.DataFrame: The input DataFrame with an additional column
                          'historicalEmissionChangePercent' representing
                          the historical average emission level change in percent for each row.
    """

    temp = []
    df = df.sort_values("Kommun", ascending=True)
    for i in range(len(df)):
        # Get the years we will use for the average
        years = np.arange(2015, last_year_in_range + 1)
        # Get the emissions from the years specified in the line above
        emissions = np.array(df.iloc[i][years], dtype=float)
        # Calculate diff (in percent) between each successive year
        diffs_in_percent = [
            (x - emissions[i - 1]) / emissions[i - 1] for i, x in enumerate(emissions)
        ][1:]
        # Calculate average diff
        avg_diff_in_percent = 100 * sum(diffs_in_percent) / len(diffs_in_percent)

        temp.append(avg_diff_in_percent)

    df["historicalEmissionChangePercent"] = temp

    return df


def calculate_needed_change_percent(df, current_year, budget_year):
    """
    Calculate the needed yearly emission level decrease to reach the Paris goal. Set to None if budget is <= 0.

    Args:
        df (pandas.DataFrame): The input DataFrame containing emission data.

    Returns:
        pandas.DataFrame: The input DataFrame with an additional column
                          'neededEmissionChangePercent' representing the
                          percentage change in emission levels needed to reach the goal.
                          This is None if the goal is unreachable.
    """

    # Year from which the paris path starts
    first_year = max(budget_year, current_year)

    temp = []
    for i in range(len(df)):
        if df.iloc[i]["Budget"] <= 0:
            temp.append(None)
        else:
            # arbitrarily chosen years
            start = df.iloc[i]["parisPath"][first_year + 1]
            final = df.iloc[i]["parisPath"][first_year + 2]
            temp.append(((start - final) / start) * 100)

    # Ensure the column is of object type to handle None correctly
    df["neededEmissionChangePercent"] = temp

    # Replace NaN values with None
    df["neededEmissionChangePercent"] = df["neededEmissionChangePercent"].replace(
        {np.nan: None}
    )

    return df


def calculate_hit_net_zero(df, last_year_in_range):
    """
    Calculates the date and year for when each municipality hits net zero emissions (if so).
    This is done by deriving where the linear trend line crosses the time axis.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the emissions data.

    Returns:
        pandas.DataFrame: The input DataFrame with an additional column 'hitNetZero' that contains
        the date when net zero emissions are reached for each municipality.
    """

    temp = []  # temporary list that we will append to
    for i in range(len(df)):
        last_year = last_year_in_range  # last year with recorded data
        # Get trend line coefficients
        fit = df.iloc[i]["trendCoefficients"]

        if fit[0] < 0:  # If the slope is negative we will reach the x-axis
            temp_f = -fit[1] / fit[0]  # Find where the line cross the x-axis
            # Initiate the first day of our starting point date.
            # Start at last_year+1 since the line can go up between last_year and last_year+1
            my_date = datetime(int(last_year + 1), 1, 1, 0, 0, 0)
            # Add the length between the starting date and the net zero date
            # to the starting date to get the date when net zero is reached
            temp.append(
                (
                    my_date
                    + relativedelta(
                        seconds=int((temp_f - int(last_year + 1)) * YEAR_SECONDS)
                    )
                ).date()
            )

        else:  # If the slope is not negative you will never reach net zero
            temp.append(None)

    df["hitNetZero"] = temp
    return df


def calculate_budget_runs_out(df, current_year, budget_year):
    """
    Calculate the year and date for when the CO2 budget runs out for each municipality (if so).
    This is done by integrating the trend line over the time it takes for the budget to be
    consumed and see where we are at the time axis by that point.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the data for each municipality.

    Returns:
        pandas.DataFrame: The input DataFrame with an additional column 'budgetRunsOut' that
        contains the year and date for when the CO2 budget runs out for each municipality.
    """

    # Year from which the budget applies
    # (after correction with respect to years passed since budget start)
    budget_start_year = max(budget_year, current_year)

    temp = []  # temporary list that we will append to
    for i in range(len(df)):
        # Get index in trend series for budget_start_year
        trend_years = list(df.iloc[i]["trend"].keys())
        budget_start_year_idx = trend_years.index(budget_start_year)
        # Get trend values for from budget_start_year onwards
        y_trend = list(df.iloc[i]["trend"].values())[budget_start_year_idx:]
        x_trend = list(df.iloc[i]["trend"].keys())[budget_start_year_idx:]

        # Get the cumulative emissions from the trend line,
        # starting from the year the corrected budget applies (from budget_start_year onwards)
        cumulative_emissions = np.trapz(y_trend, x_trend)

        # If the trends cumulative emission is larger than the budget,
        # the municipality will run out of budget
        if cumulative_emissions > df.iloc[i]["Budget"]:
            # Get the line coefficients for the trend line
            fit = df.iloc[i]["trendCoefficients"]

            # Remove the "anomaly" from the budget (if any)
            # Subtract emission from trend between budget_start_year and budget_start_year+1
            # since the line can go up between budget_start_year and budget_start_year+1
            # if BUDGET_YEAR == LAST_YEAR_WITH_SMHI_DATA
            B = df.iloc[i]["Budget"] - np.trapz(y_trend[:2], x_trend[:2])
            start_year_after_correction = budget_start_year + 1

            # Find the value where the budget B has been consumed
            # by solving -1/2(x1-x2)(2m+k(x1+x2))=B for x2 where x1=start_year_after_correction
            x = (
                np.sqrt(
                    2 * B * fit[0]
                    + (fit[0] * start_year_after_correction + fit[1]) ** 2
                )
                - fit[1]
            ) / (fit[0])

            # Initiate the first day of our starting point date
            my_date = datetime(start_year_after_correction, 1, 1, 0, 0, 0)
            # Calculate the time diff between starting date and point in time where budget runs out
            time_diff_in_years = x - (start_year_after_correction)
            time_diff_in_seconds = int(time_diff_in_years * YEAR_SECONDS)
            # Add diff to starting date to get date for when budget runs out
            budget_runs_out_date = (
                my_date + relativedelta(seconds=time_diff_in_seconds)
            ).date()

            temp.append(budget_runs_out_date)
        else:
            temp.append(None)

    df["budgetRunsOut"] = temp

    return df


def emission_calculations(df):
    """
    Perform emission calculations based on the given dataframe.

    Parameters:
    - df (pandas.DataFrame): The input dataframe containing municipality data.

    Returns:
    - df_budget_runs_out (pandas.DataFrame): The resulting dataframe with emissions data.
    """

    df_smhi = get_n_prep_data_from_smhi(df)

    df_cem = deduct_cement(df_smhi, CEMENT_DEDUCTION)

    df_trend_coefficients = calculate_trend_coefficients(
        df_cem, LAST_YEAR_WITH_SMHI_DATA
    )

    df_approxmimated_historical_total = calculate_approximated_historical(
        df_trend_coefficients, LAST_YEAR_WITH_SMHI_DATA, CURRENT_YEAR
    )

    df_trend = calculate_trend(
        df_approxmimated_historical_total, LAST_YEAR_WITH_SMHI_DATA, CURRENT_YEAR
    )

    # Calculate carbon budget with subtracted national overheads
    budget = calculate_n_subtract_national_overheads(
        NATIONAL_BUDGET_15, NATIONAL_BUDGET_17, NATIONAL_OVERHEAD_17
    )

    df_budgeted = calculate_municipality_budgets(
        df_trend, LAST_YEAR_WITH_SMHI_DATA, CURRENT_YEAR, budget, BUDGET_YEAR
    )

    df_paris = calculate_paris_path(
        df_budgeted, LAST_YEAR_WITH_SMHI_DATA, CURRENT_YEAR, BUDGET_YEAR
    )

    df_historical_change_percent = calculate_historical_change_percent(
        df_paris, LAST_YEAR_WITH_SMHI_DATA
    )

    df_needed_change_percent = calculate_needed_change_percent(
        df_historical_change_percent, CURRENT_YEAR, BUDGET_YEAR
    )

    df_net_zero = calculate_hit_net_zero(
        df_needed_change_percent, LAST_YEAR_WITH_SMHI_DATA
    )

    df_budget_runs_out = calculate_budget_runs_out(
        df_net_zero, CURRENT_YEAR, BUDGET_YEAR
    )

    return df_budget_runs_out
