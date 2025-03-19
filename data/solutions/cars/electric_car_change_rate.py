import pandas as pd


# calculations based on trafa data
PATH_CARS_DATA = "output/trafa-output.xlsx"


def get_electric_car_change_rate(df, to_percent: bool = False):
    # LOAD AND PREP DATA ON CHANGE RATE OF PERCENTAGE OF NEWLY REGISTERED RECHARGABLE CARS PER MUNICIPALITY AND YEAR
    df_raw_cars = pd.read_excel(PATH_CARS_DATA)
    
    # # Years is all coumns except the first and last
    years = df_raw_cars.columns.difference(["Kommun", "Trend", "Unnamed: 0"])
    
    df_raw_cars["electricCarChangePercent"] = df_raw_cars[
        "Trend"
    ].apply(
        lambda x: round(x * (100 if to_percent else 1), 2)
    )
    
    df_raw_cars["electricCarChangeYearly"] = df_raw_cars.apply(
        lambda x: {year: round(x.loc[year] * (100 if to_percent else 1),2) for year in years},
        axis=1
    )

    df_cars = df_raw_cars.filter(
        ["Kommun", "electricCarChangePercent", "electricCarChangeYearly"], axis=1
    )

    df = df.merge(df_cars, on="Kommun", how="left")

    return df