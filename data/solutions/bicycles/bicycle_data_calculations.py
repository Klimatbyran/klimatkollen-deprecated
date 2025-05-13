import pandas as pd


PATH_BICYCLE_DATA = "solutions/bicycles/sources/Cykelnät per komun 20241231.xlsx"
PATH_POPULATION_DATA = "solutions/bicycles/sources/be0101_tabhel2024.xlsx"


def calculate_bike_lane_per_capita():
    """
    Perform calculations on bicycle data and population data on municipality level.

    This function reads bicycle data and population data from Excel files, performs
    data cleaning and merging, and calculates the bike lane per capita per municipality.

    Returns:
        pandas.DataFrame: A DataFrame containing the calculated bike lane per capita.
    """

    df_raw_bicycles = pd.read_excel(PATH_BICYCLE_DATA, skiprows=3)
    df_bicycles = df_raw_bicycles[["Kommun", "Totalsumma"]]
    df_bicycles.loc[df_bicycles["Kommun"] == "Malung", "Kommun"] = "Malung-Sälen"
    df_bicycles.loc[df_bicycles["Kommun"] == "Upplands-Väsby", "Kommun"] = (
        "Upplands Väsby"
    )

    df_raw_population = pd.read_excel(PATH_POPULATION_DATA, skiprows=5)
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
    df_merged["bikeMetrePerCapita"] = df_merged["Totalsumma"] / df_merged["Folkmängd"]

    return df_merged[["Kommun", "bikeMetrePerCapita"]]
