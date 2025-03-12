import pandas as pd
from sklearn.preprocessing import RobustScaler
import xgboost as xgb

def train_model():
    df_train = pd.read_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset2.csv")
    features = ["Mass", "Radius", "Volume", "Density"]

    X_train = df_train[features]

    scaler = RobustScaler()
    X_train_normalized = scaler.fit_transform(X_train)

    Y_train = df_train["Radiated Energy"]
    xgboost_model = xgb.XGBRegressor()
    xgboost_model.fit(X_train_normalized, Y_train)

    return xgboost_model, scaler


def predict_radiated_energy():
    df_test = pd.read_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/predicted_dataset1.csv")
    
    xgboost_model, scaler = train_model()
    features = ["Mass", "Radius", "Volume", "Density"]
    X_test = df_test[features]

    # Normalization:
    X_test_normalized = scaler.transform(X_test)    
    df_test["Radiated Energy"] = xgboost_model.predict(X_test_normalized) / 100000000
    df_test.to_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/predicted_dataset1.csv")

    predicted_energy = df_test["Radiated Energy"].head(10).tolist()
    return predicted_energy
