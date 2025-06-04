import json
import pandas as pd
from pathlib import Path


def get_consumption_emissions():
    """Add consumption emissions data to the input DataFrame from source JSON files.

    Args:
        df (pd.DataFrame): Input DataFrame containing municipality data

    Returns:
        pd.DataFrame: DataFrame with consumption emissions data added
    """
    # Path to source JSON files
    sources_dir = Path(__file__).parent / "sources"

    # List to store emissions data for all municipalities
    all_municipalities = []

    # Process each JSON file in the sources directory
    for file_path in sources_dir.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as file:
            municipalities_data = json.load(file)

            # Extract municipality data (exclude country and county entries)
            for entry in municipalities_data:
                # Skip entries for Sweden (SE) and counties (2-digit codes)
                if entry["code"] == "SE" or (len(entry["code"]) <= 2):
                    continue

                municipality = {
                    "Kommun": entry["name"],
                    "consumptionEmissions": float(entry["emissions"]) / 1000,
                }

                all_municipalities.append(municipality)

    # Convert to pandas DataFrame
    df_consumption = pd.DataFrame(all_municipalities)

    return df_consumption
