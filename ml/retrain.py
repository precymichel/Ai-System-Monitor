import subprocess
import sys


print("======================================")
print("AI SYSTEM MONITOR - MODEL RETRAINING")
print("======================================")


# ==================================================
# TRAIN CPU PREDICTION MODEL
# ==================================================

print("\n[1/2] Training CPU prediction model...")
print("--------------------------------------")

result = subprocess.run(
    [sys.executable, "ml/train.py"]
)

if result.returncode != 0:

    print("\nCPU model training failed.")

    sys.exit(1)


# ==================================================
# TRAIN ANOMALY MODEL
# ==================================================

print("\n[2/2] Training anomaly detection model...")
print("-----------------------------------------")

result = subprocess.run(
    [sys.executable, "ml/anomaly.py"]
)

if result.returncode != 0:

    print("\nAnomaly model training failed.")

    sys.exit(1)


# ==================================================
# COMPLETE
# ==================================================

print("\n======================================")
print("MODEL RETRAINING COMPLETED")
print("======================================")

print("\nModels updated successfully:")
print("- CPU prediction model")
print("- Anomaly detection model")