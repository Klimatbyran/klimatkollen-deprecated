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
from issues.consumption.consumption_emissions import get_consumption_emissions

# Notebook from ClimateView that our calculations are based on:
# https://colab.research.google.com/drive/1qqMbdBTu5ulAPUe-0CRBmFuh8aNOiHEb?usp=sharing


def create_dataframe(to_percentage: bool) -> pd.DataFrame:
    """Create a comprehensive climate dataframe by merging multiple data sources"""

    municipalities_df = get_municipalities()
    print("1. Municipalities loaded and prepped")

    emissions_df = emission_calculations(municipalities_df)
    print("2. Climate data and calculations added")

    ev_change_rate_df = get_ev_change_rate(emissions_df, to_percentage)
    print("3. Hybrid car data and calculations added")

    climate_plans_df = get_climate_plans(ev_change_rate_df)
    print("4. Climate plans added")

    bike_lane_df = calculate_bike_lane_per_capita()
    climate_plans_with_bike_df = climate_plans_df.merge(
        bike_lane_df, on="Kommun", how="left"
    )
    print("5. Bicycle data added")

    consumption_emissions_df = get_consumption_emissions()
    bike_lane_with_consumption_emissions_df = consumption_emissions_df.merge(
        climate_plans_with_bike_df, on="Kommun", how="left"
    )
    print("6. Consumption emission data added")

    evpc_df = get_electric_vehicle_per_charge_points()
    consumption_emissions_with_evpc_df = bike_lane_with_consumption_emissions_df.merge(
        evpc_df, on="Kommun", how="left"
    )
    print("7. CPEV for December 2023 added")

    procurement_df = get_procurement_data()
    result_df = consumption_emissions_with_evpc_df.merge(
        procurement_df, on="Kommun", how="left"
    )
    print("8. Climate requirements in procurements added")

    return result_df.sort_values(by="Kommun").reset_index(drop=True)


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
        "totalConsumptionEmission": row["consumptionEmissions"],
        "electricVehiclePerChargePoints": (
            row["EVPC"] if pd.notna(row["EVPC"]) else None
        ),
        "procurementScore": row["procurementScore"],
        "procurementLink": row["procurementLink"],
    }


def round_processing(v, num_decimals: int):
    new_v = v
    if isinstance(v, float):
        new_v = np.round(v, num_decimals)
    elif isinstance(v, dict):
        new_v = {k: round_processing(a, num_decimals) for k, a in v.items()}
    return new_v


def max_decimals(entry: Dict, num_decimals: int) -> Dict:
    return {k: round_processing(v, num_decimals) for k, v in entry.items()}


def df_to_dict(input_df: pd.DataFrame, num_decimals: int) -> dict:
    """Convert dataframe to list of dictionaries with optional decimal rounding."""
    numeric_columns = [col for col in input_df.columns if str(col).isdigit()]

    return [
        (
            max_decimals(
                series_to_dict(input_df.iloc[i], numeric_columns), num_decimals
            )
            if num_decimals >= 0
            else series_to_dict(input_df.iloc[i], numeric_columns)
        )
        for i in range(len(input_df))
    ]


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
        default=True,
        help="Convert to percentages",
    )
    parser.add_argument(
        "-n",
        "--num_decimals",
        default=2,
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
