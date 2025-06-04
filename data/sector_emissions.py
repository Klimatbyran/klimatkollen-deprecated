# -*- coding: utf-8 -*-
from typing import Dict, List
import json
import pandas as pd

from issues.emissions.historical_data_calculations import (
    get_smhi_data,
    extract_sector_data,
)


def create_sector_emissions_dict(
    input_df: pd.DataFrame, num_decimals: int = 2
) -> List[Dict]:
    """Create a list of dictionaries containing sector emissions data for each municipality.

    Args:
        df: DataFrame containing sector emissions data
        num_decimals: Number of decimal places to round to (default: 2)

    Returns:
        List of dictionaries with municipality sector emissions data
    """
    result = []

    for _, row in input_df.iterrows():
        municipality_data = {"name": row["Kommun"], "sectors": {}}

        # Get all columns that contain sector data (they have '_' in their name)
        sector_columns = [col for col in row.index if "_" in str(col)]

        for col in sector_columns:
            # Split column name to get year and sector
            year, sector = col.split("_")
            if year not in municipality_data["sectors"]:
                municipality_data["sectors"][year] = {}

            # Round the value to specified decimals
            value = round(float(row[col]), num_decimals) if pd.notna(row[col]) else None
            municipality_data["sectors"][year][sector] = value

        result.append(municipality_data)

    return result


def generate_sector_emissions_file(
    output_file: str = "output/sector-emissions.json", num_decimals: int = 2
) -> None:
    """Generate a JSON file containing sector emissions data for all municipalities.

    Args:
        output_file: path to output JSON file
        num_decimals: number of decimal places to round to
    """
    df_raw = get_smhi_data()

    df_sectors = extract_sector_data(df_raw)

    sector_data = create_sector_emissions_dict(df_sectors, num_decimals)

    with open(output_file, "w", encoding="utf8") as json_file:
        json.dump(sector_data, json_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    generate_sector_emissions_file()
