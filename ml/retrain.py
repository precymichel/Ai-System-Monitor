import os
import subprocess
import sys


print("======================================")
print("AI SYSTEM MONITOR - MODEL RETRAINING")
print("======================================")


# Project root directory
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# Make sure child Python processes can import
# database, ml, monitoring, etc.
env = os.environ.copy()

existing_pythonpath = env.get("PYTHONPATH", "")

if existing_pythonpath:
    env["PYTHONPATH"] = PROJECT_ROOT + os.pathsep + existing_pythonpath
else:
    env["PYTHONPATH"] = PROJECT_ROOT


# ======================================
# CPU PREDICTION MODEL
# ======================================

print("\n[1/2] Training CPU prediction model...")
print("--------------------------------------")

result = subprocess.run(
    [
        sys.executable,
        "-m",
        "ml.train"
    ],
    cwd=PROJECT_ROOT,
    env=env
)


if result.returncode != 0:

    print("\nCPU model training failed.")

    sys.exit(1)


# ======================================
# ANOMALY DETECTION MODEL
# ======================================

print("\n[2/2] Training anomaly detection model...")
print("-----------------------------------------")

result = subprocess.run(
    [
        sys.executable,
        "-m",
        "ml.anomaly"
    ],
    cwd=PROJECT_ROOT,
    env=env
)


if result.returncode != 0:

    print("\nAnomaly model training failed.")

    sys.exit(1)


# ======================================
# COMPLETED
# ======================================

print("\n======================================")
print("MODEL RETRAINING COMPLETED")
print("======================================")

print("\nModels updated successfully:")
print("- CPU prediction model")
print("- Anomaly detection model")