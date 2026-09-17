import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os


DATABASE_FILE = "data/system_metrics.db"

MODEL_FILE = "models/anomaly_model.pkl"


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
    disk
FROM system_metrics
ORDER BY id
"""

df = pd.read_sql_query(
    query,
    connection
)

connection.close()


# ==================================================
# DISPLAY
# ==================================================

print(
    "AI SYSTEM MONITOR - ANOMALY DETECTION"
)

print(
    "--------------------------------------"
)


print(
    "Training rows:",
    len(df)
)


# ==================================================
# FEATURES
# ==================================================

features = [

    "cpu",

    "ram",

    "disk"

]


X = df[features]


# ==================================================
# TRAIN ISOLATION FOREST
# ==================================================

model = IsolationForest(

    n_estimators=100,

    contamination=0.05,

    random_state=42,

    n_jobs=1

)


print(
    "\nTraining anomaly detection model..."
)


model.fit(X)


# ==================================================
# SAVE MODEL
# ==================================================

os.makedirs(
    "models",
    exist_ok=True
)


joblib.dump(
    model,
    MODEL_FILE
)


print(
    "\nAnomaly detection model saved!"
)


print(
    "Location:",
    MODEL_FILE
)


# ==================================================
# DETECT ANOMALIES
# ==================================================

df["anomaly"] = model.predict(
    X
)


anomalies = df[
    df["anomaly"] == -1
]


print(
    "\nAnomaly Results"
)


print(
    "----------------"
)


print(
    "Total records:",
    len(df)
)


print(
    "Anomalies detected:",
    len(anomalies)
)


if len(anomalies) > 0:

    print(
        "\nRecent anomalies:"
    )

    print(
        anomalies[
            [
                "timestamp",
                "cpu",
                "ram",
                "disk"
            ]
        ].tail(10)
    )

else:

    print(
        "\nNo anomalies detected."
    )