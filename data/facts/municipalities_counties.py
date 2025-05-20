import pandas as pd


def get_municipalities():
    """Load and process municipality data with their corresponding county codes."""
    municipalities_df = pd.read_excel("facts/kommunlankod_2023.xls")

    # Set column names to 'Kod' and 'Namn'
    municipalities_df.columns = ["Kod", "Namn"]

    # Drop unnecessary rows
    municipalities_df = municipalities_df.drop([0, 1, 2, 3, 4], axis=0).reset_index(
        drop=True
    )

    # Create an empty dataframe to store the result
    result_df = pd.DataFrame(columns=["Kommun", "Kod", "Län"])

    # Iterate through the rows of the dataframe
    for _, row in municipalities_df.iterrows():
        if len(row["Kod"]) == 4:  # Check if it is a four-digit code row
            code = row["Kod"]
            municipality = row["Namn"]
            # Lookup the county (Län) based on the two-digit code
            county = municipalities_df.loc[
                municipalities_df["Kod"] == code[:2], "Namn"
            ].values[0]
            # Append a new row to the 'result' DataFrame
            result_df = pd.concat(
                [
                    result_df,
                    pd.DataFrame(
                        {"Kommun": [municipality], "Kod": [code], "Län": [county]}
                    ),
                ],
                ignore_index=True,
            )

    # Return the resulting dataframe
    return result_df
