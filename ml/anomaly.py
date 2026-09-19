import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest

from database.database import get_metrics


print("======================================")
print("AI SYSTEM MONITOR - ANOMALY DETECTION")
print("======================================")


# --------------------------------------
# Load data from Supabase
# --------------------------------------

rows = get_metrics(100000)

if not rows:
    print("No data available in Supabase.")
    exit()


df = pd.DataFrame(rows)

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)

df = df.sort_values(
    "timestamp"
).reset_index(drop=True)


print(f"Training rows: {len(df)}")


if len(df) < 20:

    print(
        "Not enough data for anomaly detection."
    )

    exit()


# --------------------------------------
# Features
# --------------------------------------

features = [
    "cpu",
    "ram",
    "disk"
]

X = df[features]


# --------------------------------------
# Isolation Forest
# --------------------------------------

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42,
    n_jobs=1
)

model.fit(X)


# --------------------------------------
# Detect anomalies
# --------------------------------------

df["anomaly"] = model.predict(X)


anomaly_count = (
    df["anomaly"] == -1
).sum()


print("\nANOMALY RESULTS")
print("--------------------------------------")

print(
    f"Total records: {len(df)}"
)

print(
    f"Anomalies detected: {anomaly_count}"
)


# --------------------------------------
# Recent anomalies
# --------------------------------------

recent_anomalies = df[
    df["anomaly"] == -1
].tail(10)


if not recent_anomalies.empty:

    print("\nRecent anomalies:")

    print(
        recent_anomalies[
            [
                "timestamp",
                "cpu",
                "ram",
                "disk"
            ]
        ].to_string(index=False)
    )


# --------------------------------------
# Save model
# --------------------------------------

os.makedirs(
    "models",
    exist_ok=True
)

model_path = (
    "models/anomaly_model.pkl"
)

joblib.dump(
    model,
    model_path
)


print("\nAnomaly model saved:")
print(model_path)

print("\nAnomaly detection completed successfully.")