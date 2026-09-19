import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from database.database import get_metrics


print("======================================")
print("AI SYSTEM MONITOR - ML TRAINING")
print("======================================")


# --------------------------------------
# Load data from Supabase
# --------------------------------------

rows = get_metrics(100000)

if not rows:
    print("No data available in Supabase.")
    exit()

df = pd.DataFrame(rows)

df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.sort_values("timestamp").reset_index(drop=True)


print(f"Total database records: {len(df)}")


# --------------------------------------
# Create future CPU target
# --------------------------------------

df["future_cpu"] = df["cpu"].shift(-60)


# --------------------------------------
# Feature engineering
# --------------------------------------

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


features = [
    "cpu",
    "ram",
    "disk",
    "cpu_avg",
    "ram_avg",
    "cpu_change",
    "ram_change"
]


df = df.dropna()


if len(df) < 80:

    print(
        f"Not enough data for training. "
        f"Need at least 80 usable records, got {len(df)}."
    )

    exit()


X = df[features]
y = df["future_cpu"]


# --------------------------------------
# Time-order train/test split
# --------------------------------------

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


# --------------------------------------
# Train model
# --------------------------------------

model = RandomForestRegressor(
    n_estimators=50,
    random_state=42,
    n_jobs=1
)

model.fit(
    X_train,
    y_train
)


# --------------------------------------
# Evaluate model
# --------------------------------------

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


print("\nMODEL RESULTS")
print("--------------------------------------")

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R2: {r2:.2f}")


# --------------------------------------
# Save model
# --------------------------------------

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


print("\nModel saved:")
print(model_path)

print("\nTraining completed successfully.")