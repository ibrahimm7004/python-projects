# Cleaning
import pandas as pd
import numpy as np
import csv


def clean1():
    data = pd.read_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/raw_D1.csv", encoding="cp1252")

    nRow, nCol = data.shape
    print(f"There are {nRow} rows and {nCol} columns")

    data.drop(0, axis=0, inplace=True)
    data.drop(
        [
            "Empty",
            "State",
            "Bolide Type",
            "URL",
            "Notes",
            "Crater Name",
            "Age (Ma)",
            "Exposed",
            "Drilled",
            "Country",
        ],
        axis=1,
        inplace=True,
    )

    data = data.drop(index=146)
    data = data.drop(index=74)

    data = data.reset_index(
        level=None, drop=True, inplace=False, col_level=0, col_fill=" "
    )

    with open("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset1.csv", mode="w", newline="") as file:
        writer = csv.writer(file)

        # Add Mass Feature:

        # Add Volume:
        data["Radius"] = data.apply(
            lambda row: (0.5 * row["Diameter (km)"]), axis=1
        )  # Adding Radius
        data["Volume"] = data.apply(
            lambda row: ((4 / 3) * (3.142) * (row["Radius"]) ** 3), axis=1
        )  # Adding Radius

        # Add Density:
        data["Density"] = data["Rock"].replace(
            {
                "Crystalline": 2.95,
                "Sedimentary": 2.4,
                "Metasedimentary": 2.65,
                "Mixed": 5,
            }
        )
        data.drop(["Rock"], axis=1, inplace=True)

    data["Mass"] = data.apply(
        lambda row: ((row["Density"]) / (row["Volume"])), axis=1
    )  # Adding Radius

    data.loc[data["Mass"] < 100, "Mass"] *= 1000
    data.loc[data["Mass"] < 100, "Mass"] *= 1000

    # Add Velocity Feature:
    G = 6.67430 * (10 ** (-11))
    pi = np.pi
    C = 1
    data["Velocity"] = data.apply(
        lambda row: np.sqrt(
            (8 * G * pi * row["Mass"])
            / (3 * C * row["Density"] * (row["Diameter (km)"] ** 2))
        ),
        axis=1,
    )

    data.loc[data["Velocity"] < 0.001, "Velocity"] *= 10000
    data.loc[data["Velocity"] < 0.01, "Velocity"] *= 1000
    data.loc[data["Velocity"] < 0.1, "Velocity"] *= 100
    data.loc[data["Velocity"] < 1, "Velocity"] *= 10
    data.loc[data["Velocity"] < 10, "Velocity"] += 15

    data.drop(["Diameter (km)"], axis=1, inplace=True)

    # Saving as csv
    data.to_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset1.csv", index=False)

