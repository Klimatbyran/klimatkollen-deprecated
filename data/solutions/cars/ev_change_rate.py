# pylint: disable=invalid-name
import pandas as pd


# calculations based on trafa data
PATH_CARS_DATA = "solutions/cars/sources/kpi1_calculations.xlsx"


def get_ev_change_rate(df, to_percent: bool = True):
    """Calculate the change rate of newly registered rechargeable cars per municipality and year."""
    df_raw_cars = pd.read_excel(PATH_CARS_DATA)

    df_raw_cars.columns = df_raw_cars.iloc[1]  # name columns after row
    df_raw_cars = df_raw_cars.drop([0, 1])  # drop usless rows
    df_raw_cars = df_raw_cars.reset_index(drop=True)

    years = [
        2015,
        2016,
        2017,
        2018,
        2019,
        2020,
        2021,
        2022,
        2023,
        2024,
    ]  # NOTE: this needs to be updated if the data is updated

    df_raw_cars["evChangeYearly"] = df_raw_cars.apply(
        lambda x: {year: x.loc[year] * (100 if to_percent else 1) for year in years},
        axis=1,
    )

    df_raw_cars["evChangeRate"] = df_raw_cars["evChangeRate"] * (
        100 if to_percent else 1
    )

    df_cars = df_raw_cars.filter(["Kommun", "evChangeRate", "evChangeYearly"], axis=1)

    df = df.merge(df_cars, on="Kommun", how="left")

    return df
