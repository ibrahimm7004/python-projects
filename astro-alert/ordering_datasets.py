import pandas as pd


def order():
    df1 = pd.read_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset1.csv")
    df2 = pd.read_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset2.csv")

    # Rename D2 columns:
    df2 = df2.rename(
        columns={
            "Latitude (deg.)": "Latitude",
            "Longitude (deg.)": "Longitude",
            "Velocity (km/s)": "Velocity",
            "Mass (kg)": "Mass",
            "Total Radiated Energy (J)": "Radiated Energy",
            "Calculated Total Impact Energy (kt)": "Impact Energy",
        }
    )
    df2.to_csv("D:/ds_proj/excel_files/dataset2.csv", index=False)

    # Adding empty columns to apply KNN on dataset 1:
    df1["Radiated Energy"] = ""
    df1["Impact Energy"] = ""
    df1.to_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset1.csv", index=False)

    # Ordering the CSV's:
    column_order = list(df1.columns)
    df2 = df2[column_order]
    df2.to_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset2.csv", index=False)
