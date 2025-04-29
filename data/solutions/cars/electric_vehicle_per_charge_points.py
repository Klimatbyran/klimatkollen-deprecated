# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy.optimize import linprog


PATH_POWERCIRCLE_CPEV = (
    "solutions/cars/sources/powercircle_municipality_data_dec_2024.csv"
)


def get_electric_vehicle_per_charge_points():
    """
    This function loads data from a CSV file provided by PowerCircle and extracts a DataFrame with the municipality names
    in title case and their corresponding electric vehicles per charge points values for December 2023.

    Returns:
        df_evpc (DataFrame): A pandas DataFrame with two columns, 'Kommun' (in title case) and 'EVPC', containing the municipality¨
        names and their corresponding electric vehicles per charge points values.
    """

    # Load CPEV data from PowerCircle
    df_evpc_raw = pd.read_csv(PATH_POWERCIRCLE_CPEV)

    # Rename the unnamed column to "Kommun" and convert 'Kommun' to title case
    df_evpc_raw = df_evpc_raw.rename(columns={"Unnamed: 0": "Kommun"})
    df_evpc_raw["Kommun"] = df_evpc_raw["Kommun"].str.title()

    # Calculate reciprocals of CPEV values
    df_evpc_raw["EVPC"] = df_evpc_raw.apply(
        lambda row: (
            row["Antal laddbara fordon"] / row["Antal laddpunkter"]
            if row["Antal laddpunkter"] != 0
            else None
        ),
        axis=1,
    )

    # Extract the 'Kommun' and 'CPEV' columns
    df_evpc = df_evpc_raw[["Kommun", "EVPC"]]

    return df_evpc
