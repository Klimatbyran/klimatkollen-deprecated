# -*- coding: utf-8 -*-

import argparse
import json
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from solutions.cars.ev_change_rate import get_ev_change_rate
from solutions.cars.electric_vehicle_per_charge_points import (
    get_electric_vehicle_per_charge_points,
)
from solutions.bicycles.bicycle_data_calculations import calculate_bike_lane_per_capita
from facts.plans.plans_data_prep import get_climate_plans
from facts.municipalities_counties import get_municipalities
from facts.procurements.climate_requirements_in_procurements import get_procurement_data
from issues.emissions.emission_data_calculations import emission_calculations
from issues.consumption.consumption_data_calculations import get_consumption_emissions

# Notebook from ClimateView that our calculations are based on:
# https://colab.research.google.com/drive/1qqMbdBTu5ulAPUe-0CRBmFuh8aNOiHEb?usp=sharing


def create_dataframe(to_percentage: bool) -> pd.DataFrame:
    """
    Creates a DataFrame with climate data for Swedish municipalities.

    Args:
        to_percentage (bool): Whether to convert values to percentages

    Returns:
        pd.DataFrame: DataFrame containing climate data for municipalities
    """

    municipality_df = get_municipalities()
    print("1. Municipalities loaded and prepped")

    municipality_df = emission_calculations(municipality_df)
    print("2. Climate data and calculations added")

    municipality_df = get_ev_change_rate(municipality_df, to_percentage)
    print("3. Hybrid car data and calculations added")

    municipality_df = get_climate_plans(municipality_df)
    print("4. Climate plans added")

    df_bike_lanes = calculate_bike_lane_per_capita()
    municipality_df = municipality_df.merge(df_bike_lanes, on="Kommun", how="left")
    print("5. Bicycle data added")

    municipality_df = get_consumption_emissions(municipality_df)
    print("6. Consumption emission data added")

    df_evpc = get_electric_vehicle_per_charge_points()
    municipality_df = municipality_df.merge(df_evpc, on="Kommun", how="left")
    print("7. CPEV for December 2023 added")

    df_procurements = get_procurement_data()
    municipality_df = municipality_df.merge(df_procurements, on="Kommun", how="left")
    print("8. Climate requirements in procurements added")

    return municipality_df


def series_to_dict(row: pd.Series, numeric_columns: List[Any]) -> Dict:
    """
    Transforms a pandas Series into a dictionary.

    Args:
    row: The pandas Series to transform.

    Returns:
    A dictionary with the transformed data.
    """
    return {
        "name": row["Kommun"],
        "region": row["Län"],
        "emissions": {str(year): row[year] for year in numeric_columns},
        "budget": row["Budget"],
        "emissionBudget": row["parisPath"],
        "approximatedHistoricalEmission": row["approximatedHistorical"],
        "totalApproximatedHistoricalEmission": row["totalApproximatedHistorical"],
        "trend": row["trend"],
        "trendEmission": row["trendEmission"],
        "historicalEmissionChangePercent": row["historicalEmissionChangePercent"],
        "neededEmissionChangePercent": row["neededEmissionChangePercent"],
        "hitNetZero": row["hitNetZero"],
        "budgetRunsOut": row["budgetRunsOut"],
        "electricCarChangePercent": row["evChangeRate"],
        "electricCarChangeYearly": row["evChangeYearly"],
        "climatePlanLink": row["Länk till aktuell klimatplan"],
        "climatePlanYear": row["Antagen år"],
        "climatePlanComment": row["Namn, giltighetsår, kommentar"],
        "bicycleMetrePerCapita": row["bikeMetrePerCapita"],
        "totalConsumptionEmission": row["Total emissions"],
        "electricVehiclePerChargePoints": (
            row["EVPC"] if pd.notna(row["EVPC"]) else None
        ),
        "procurementScore": row["procurementScore"],
        "procurementLink": row["procurementLink"],
    }


def round_processing(value, num_decimals: int):
    """
    Rounds numeric values to specified decimal places, handling both floats and nested dictionaries.

    Args:
        v: Value to round (float or dict)
        num_decimals (int): Number of decimal places

    Returns:
        Rounded value of the same type as input
    """

    new_value = value
    if isinstance(value, float):
        new_value = np.round(value, num_decimals)
    elif isinstance(value, dict):
        new_value = {k: round_processing(a, num_decimals) for k, a in value.items()}
    return new_value


def max_decimals(entry: Dict, num_decimals: int) -> Dict:
    """
    Rounds numeric values in a dictionary to specified decimal places.

    Args:
        entry: Dictionary containing numeric values
        num_decimals (int): Number of decimal places

    Returns:
        Dictionary with rounded numeric values
    """

    return {k: round_processing(v, num_decimals) for k, v in entry.items()}


def df_to_dict(df_to_convert: pd.DataFrame, num_decimals: int) -> dict:
    """
    Converts DataFrame to a list of dictionaries with optional decimal rounding.

    Args:
        df (pd.DataFrame): Input DataFrame
        num_decimals (int): Number of decimal places to round to (-1 for no rounding)

    Returns:
        list: List of dictionaries containing municipality data
    """

    numeric_columns = [col for col in df_to_convert.columns if str(col).isdigit()]

    return (
        [
            max_decimals(
                series_to_dict(df_to_convert.iloc[i], numeric_columns), num_decimals
            )
            for i in range(len(df_to_convert))
        ]
        if num_decimals >= 0
        else [
            series_to_dict(df_to_convert.iloc[i], numeric_columns)
            for i in range(len(df_to_convert))
        ]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Climate data calculations")
    parser.add_argument(
        "-o",
        "--outfile",
        default="output/climate-data.json",
        type=str,
        help="Output filename (JSON formatted)",
    )
    parser.add_argument(
        "-t",
        "--to_percentage",
        action="store_true",
        default=False,
        help="Convert to percentages",
    )
    parser.add_argument(
        "-n",
        "--num_decimals",
        default=-1,
        type=int,
        help="Number of decimals to round to",
    )

    args = parser.parse_args()

    df = create_dataframe(args.to_percentage)

    temp = df_to_dict(df, args.num_decimals)

    output_file = args.outfile

    with open(output_file, "w", encoding="utf8") as json_file:
        # save dataframe as json file
        json.dump(temp, json_file, ensure_ascii=False, default=str)

    print("Climate data JSON file created and saved")
