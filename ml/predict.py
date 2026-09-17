import sqlite3
import pandas as pd
import joblib


DATABASE_FILE = "data/system_metrics.db"

MODEL_FILE = "models/cpu_prediction_model.pkl"


# ==================================================
# LOAD DATA FROM SQLITE
# ==================================================

connection = sqlite3.connect(
    DATABASE_FILE
)

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
# FEATURE ENGINEERING
# ==================================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
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
# LATEST DATA
# ==================================================

latest = df.iloc[-1]


features = [

    "cpu",

    "ram",

    "disk",

    "cpu_avg",

    "ram_avg",

    "cpu_change",

    "ram_change"

]


X_latest = (
    latest[features]
    .to_frame()
    .T
)


# ==================================================
# LOAD MODEL
# ==================================================

model = joblib.load(
    MODEL_FILE
)


# ==================================================
# PREDICT
# ==================================================

prediction = model.predict(
    X_latest
)[0]


prediction = max(
    0,
    min(100, prediction)
)


# ==================================================
# DISPLAY
# ==================================================

print(
    "AI CPU PREDICTION"
)


print(
    "-----------------"
)


print(
    f"Current CPU: {latest['cpu']:.1f}%"
)


print(
    f"Current RAM: {latest['ram']:.1f}%"
)


print(
    f"Current Disk: {latest['disk']:.1f}%"
)


print(
    f"Predicted CPU in 5 minutes: {prediction:.1f}%"
)