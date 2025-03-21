# Cleaning
import pandas as pd
import numpy as np
import random


def clean2():
    df = pd.read_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/raw_D2.csv")

    df = df.drop(df.index[289:952])
    df = df.drop(
        ["Peak Brightness Date/Time (UT)", "Altitude (km)", "vx", "vy", "vz"], axis=1
    )

    df["Latitude (deg.)"] = df["Latitude (deg.)"].str[:-1]
    df["Longitude (deg.)"] = df["Longitude (deg.)"].str[:-1]

    # Adding Mass Feature
    df["Mass"] = df.apply(
        lambda row: (2 * row["Calculated Total Impact Energy (kt)"])
        / (row["Velocity (km/s)"] ** 2),
        axis=1,
    )

    column_index = 5
    multiplier = 1000000

    for i in df.index:
        df.iloc[i, column_index] *= multiplier

    df["Mass"] = df["Mass"].astype(int)
    df["Mass (kg)"] = df["Mass"]
    df = df.drop(["Mass"], axis=1)

    # Adding radius
    for i in range(len(df)):
        df["Radius"] = (
            random.uniform(0.2, 0.9) * df["Calculated Total Impact Energy (kt)"]
        )

    # Adding volume
    df["Volume"] = df.apply(
        lambda row: ((4 / 3) * (np.pi) * (row["Radius"] ** 3)), axis=1
    )

    # Adding density
    for i in range(len(df)):
        df["Density"] = random.uniform(10000, 20000) * df["Mass (kg)"]

    # Saving to csv
    df.to_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset2.csv", index=False)
