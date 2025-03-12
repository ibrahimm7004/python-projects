import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler

def train_model():
    df_train = pd.read_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset2.csv")
    features = ["Mass", "Radius", "Volume", "Density"]

    X_train = df_train[features]
    scaler = MinMaxScaler()
    X_train_normalized = scaler.fit_transform(X_train)

    Y_train = df_train["Impact Energy"]

    knn = KNeighborsRegressor()
    knn.fit(X_train_normalized, Y_train)
    return knn, scaler



def predict_impact_energy():
    # Load dataset1 for prediction
    df_test = pd.read_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/dataset1.csv")
    df_test.drop('Velocity', axis=1, inplace=True)

    knn_model, scaler = train_model()
    features = ["Mass", "Radius", "Volume", "Density"]
    X_test = df_test[features]

    X_test_normalized = scaler.transform(X_test)  # Normalization
    df_test['Impact Energy'] = predicted_impact_energy = knn_model.predict(X_test_normalized)
    df_test.to_csv("C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/predicted_dataset1.csv")

    return list(predicted_impact_energy[:10])

