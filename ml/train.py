import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os


DATABASE_FILE = "data/system_metrics.db"


# ==================================================
# LOAD DATA FROM SQLITE
# ==================================================

connection = sqlite3.connect(DATABASE_FILE)

query = """
SELECT
    timestamp,
    cpu,
    ram,
    disk,
    bytes_sent,
    bytes_received
FROM system_metrics
ORDER BY id
"""

df = pd.read_sql_query(
    query,
    connection
)

connection.close()


# ==================================================
# CHECK DATA
# ==================================================

print("AI SYSTEM MONITOR - CPU PREDICTION")
print("----------------------------------")

print("Total database records:", len(df))


if len(df) < 80:

    print(
        "\nNot enough data for training."
    )

    print(
        "Collect more system metrics first."
    )

    exit()


# ==================================================
# FEATURE ENGINEERING
# ==================================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)


# Predict CPU 5 minutes into the future
# 60 records × approximately 5 seconds = 5 minutes

df["future_cpu"] = (
    df["cpu"]
    .shift(-60)
)


df["cpu_avg"] = (
    df["cpu"]
    .rolling(12)
    .mean()
)


df["ram_avg"] = (
    df["ram"]
    .rolling(12)
    .mean()
)


df["cpu_change"] = (
    df["cpu"]
    .diff()
)


df["ram_change"] = (
    df["ram"]
    .diff()
)


df = df.dropna()


# ==================================================
# FEATURES
# ==================================================

features = [

    "cpu",

    "ram",

    "disk",

    "cpu_avg",

    "ram_avg",

    "cpu_change",

    "ram_change"

]


X = df[features]

y = df["future_cpu"]


# ==================================================
# TRAIN / TEST SPLIT
# ==================================================

split = int(
    len(df) * 0.8
)


X_train = X.iloc[:split]

X_test = X.iloc[split:]


y_train = y.iloc[:split]

y_test = y.iloc[split:]


print(
    "Training samples:",
    len(X_train)
)

print(
    "Testing samples:",
    len(X_test)
)


# ==================================================
# RANDOM FOREST
# ==================================================

model = RandomForestRegressor(

    n_estimators=50,

    random_state=42,

    n_jobs=1

)


print(
    "\nTraining model..."
)


model.fit(
    X_train,
    y_train
)


# ==================================================
# PREDICTION
# ==================================================

predictions = model.predict(
    X_test
)


# ==================================================
# MODEL EVALUATION
# ==================================================

mae = mean_absolute_error(
    y_test,
    predictions
)


mse = mean_squared_error(
    y_test,
    predictions
)


rmse = mse ** 0.5


r2 = r2_score(
    y_test,
    predictions
)


print(
    "\nMODEL RESULTS"
)


print(
    "-------------"
)


print(
    "MAE :",
    round(mae, 2)
)


print(
    "RMSE:",
    round(rmse, 2)
)


print(
    "R2  :",
    round(r2, 2)
)


# ==================================================
# SAVE MODEL
# ==================================================

os.makedirs(
    "models",
    exist_ok=True
)


model_path = (
    "models/cpu_prediction_model.pkl"
)


joblib.dump(
    model,
    model_path
)


print(
    "\nModel saved successfully!"
)


print(
    "Location:",
    model_path
)