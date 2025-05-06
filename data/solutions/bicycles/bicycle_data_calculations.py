import pandas as pd


PATH_BICYCLE_DATA_2023 = "solutions/bicycles/Cykelnät per komun 20231231.xlsx"
PATH_BICYCLE_DATA_2024 = "solutions/bicycles/Statistik_2024.xlsx"
PATH_POPULATION_DATA_2024 = "solutions/bicycles/be0101_tabhel2024.xlsx"


def calculate_bike_lane_per_capita():
    """
    Perform calculations on bicycle data and population data on municipality level.

    This function reads bicycle data and population data from Excel files, performs
    data cleaning and merging, and calculates the bike lane per capita per municipality.

    Returns:
        pandas.DataFrame: A DataFrame containing the merged data and the calculated bike lane per capita.
    """

    df_bicycles_2023_raw = pd.read_excel(PATH_BICYCLE_DATA_2023, skiprows=3)
    df_bicycles_2024_raw = pd.read_excel(PATH_BICYCLE_DATA_2024)
    df_raw_population = pd.read_excel(PATH_POPULATION_DATA_2024, skiprows=5)

    df_bicycles = df_bicycles_2023_raw[["Kommun", "Totalsumma"]]
    df_bicycles.loc[df_bicycles["Kommun"] == "Malung", "Kommun"] = "Malung-Sälen"
    df_bicycles.loc[df_bicycles["Kommun"] == "Upplands-Väsby", "Kommun"] = (
        "Upplands Väsby"
    )

    df_bicycles_2024 = df_bicycles_2024_raw[["Kommunnamn", "_length.sum"]].rename(
        columns={"Kommunnamn": "Kommun", "_length.sum": "Totalsumma_2024"}
    )

    # Merge 2024 sums into 2023 data
    df_bicycles = df_bicycles.merge(df_bicycles_2024, on="Kommun", how="left")

    # Add 2024 length to 2023 Totalsumma (fillna(0) in case of missing data)
    df_bicycles["Total"] = df_bicycles["Totalsumma"] + df_bicycles[
        "Totalsumma_2024"
    ].fillna(0)

    # Drop unnecessary rows
    df_population_drop = df_raw_population.drop([0, 1, 2, 3])

    # Filter out county rows (that have 2 codes in the 'Kommun' column instead of 4)
    df_population_municipality = df_population_drop[
        df_population_drop["Kommun"].str.len() == 4
    ]

    # Filter out unnecessary columns
    df_population_filter = df_population_municipality[["Kommunnamn", "Folkmängd"]]

    # Rename 'Kommunnamn' to 'Kommun' to match the bicycle dataframe
    df_population_renamed = df_population_filter.rename(
        columns={"Kommunnamn": "Kommun"}
    )

    # Strip 'Kommun' column of whitespaces
    df_population_renamed["Kommun"] = df_population_renamed["Kommun"].str.strip()

    # Merge bicycle and population dataframes
    df_merged = df_bicycles.merge(df_population_renamed, on="Kommun", how="left")

    # Calculate bike lane per capita
    df_merged["bikeMetrePerCapita"] = df_merged["Total"] / df_merged["Folkmängd"]

    return df_merged[["Kommun", "bikeMetrePerCapita"]]
