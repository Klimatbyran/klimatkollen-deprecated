import json
import pandas as pd


PATH_CONSUMPTION_DATA = "issues/consumption/consumption_data_raw.json"


def get_consumption_emissions(df):
    """Add consumption emissions data to the input DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing municipality data

    Returns:
        pd.DataFrame: DataFrame with consumption emissions data added
    """

    # Parse JSON data
    with open(PATH_CONSUMPTION_DATA, "r", encoding="utf-8") as file:
        data = json.load(file)

    # List to store each municipality's emission properties
    features_list = []
    total_emissions_list = []

    for item in data:
        for feature in item["features"]:
            # Get properties
            properties = feature["properties"]

            # Rename keys
            properties["Kommun"] = properties.pop("kom_namn")

            total_emissions_list.append(
                {
                    "Kommun": properties["Kommun"],
                    "Konsumtionsutsläpp (ton/person/år)": properties["Total emissions"],
                }
            )

            # Remove unwanted 'geoid' and 'län' key
            properties.pop("geoid", None)

            features_list.append(properties)

    # Convert to pandas DataFrame
    df_consumption = pd.DataFrame(features_list)

    df = df.merge(df_consumption, on="Kommun", how="left")
    return df
