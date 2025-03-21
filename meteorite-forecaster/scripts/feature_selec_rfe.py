import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import RFE


def rfe():
    df_train = pd.read_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset2.csv")
    features = [
        "Mass",
        "Radius",
        "Latitude",
        "Longitude",
        "Velocity",
        "Volume",
        "Density",
    ]

    # Create X_train dataframe containing the features
    X_train = df_train[features]

    # Create Y_train dataframe containing the target variable (impact energy)
    Y_train = df_train["Impact Energy"]

    # Create a Random Forest Regressor model
    rf = RandomForestRegressor(n_estimators=100, random_state=42)

    # Perform Recursive Feature Elimination with Random Forest as estimator
    rfe = RFE(estimator=rf, n_features_to_select=4, step=1)
    rfe.fit(X_train, Y_train)

    # Get the selected feature indices
    selected_indices = rfe.support_

    selected_features_dict = {}
    for f in range(len(selected_indices)):
        selected_features_dict[X_train.columns[f]] = selected_indices[f]

    return selected_features_dict
