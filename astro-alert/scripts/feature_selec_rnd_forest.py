import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def forest():
    df_train = pd.read_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset2.csv")
    features = ["Mass","Radius","Latitude","Longitude","Velocity","Volume","Density"]

    X_train = df_train[features]
    Y_train = df_train["Impact Energy"]

    rf = RandomForestRegressor(n_estimators=100, random_state=42)

    rf.fit(X_train, Y_train)

    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]

    feature_dict = {}
    for f in range(X_train.shape[1]):
        feature_dict[features[indices[f]]] = round(importances[indices[f]], 3)

    return feature_dict
