# 🤖 AI-Powered Real-Time System Monitoring & Predictive Analytics

<p align="center">
  <strong>Real-Time System Monitoring • Data Analytics • Machine Learning • Anomaly Detection • Predictive Analytics</strong>
</p>

<p align="center">
  An end-to-end Python application that collects real-time system metrics,
  stores historical data in Supabase PostgreSQL, analyzes system behavior,
  predicts future CPU utilization, detects anomalies, and presents
  system insights through an interactive Streamlit dashboard.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)

![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?

# 🏗️ System Architecture

The project follows a complete data pipeline from real-time system monitoring
to storage, analytics, machine learning, anomaly detection, and visualization.

```text
                    ┌─────────────────────────┐
                    │      Windows PC         │
                    │                         │
                    │ CPU / RAM / Disk /      │
                    │ Network / Processes     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Python Monitoring    │
                    │        Agent            │
                    │                         │
                    │        psutil           │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Supabase           │
                    │      PostgreSQL         │
                    │                         │
                    │    system_metrics      │
                    └────────────┬────────────┘
                                 │
                  ┌──────────────┴──────────────┐
                  │                             │
                  ▼                             ▼
       ┌─────────────────────┐       ┌─────────────────────┐
       │   Data Analytics    │       │   Machine Learning  │
       │                     │       │                     │
       │ Historical Metrics  │       │ CPU Prediction      │
       │ Trends              │       │ Anomaly Detection   │
       │ Statistics          │       │                     │
       └──────────┬──────────┘       └──────────┬──────────┘
                  │                             │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Streamlit Dashboard  │
                    │                         │
                    │ Real-Time Monitoring    │
                    │ AI Insights              │
                    │ Alerts                   │
                    │ Charts                   │
                    │ Process Monitoring       │
                    │ Historical Analytics     │
                    │ Model Control            │
                    └─────────────────────────┘

🔄 Data Flow

The application processes system information through the following pipeline:

System Metrics
      ↓
psutil
      ↓
Python Monitoring Script
      ↓
Supabase PostgreSQL
      ↓
Data Retrieval
      ↓
Data Preprocessing
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Prediction + Anomaly Detection
      ↓
Streamlit Dashboard
      ↓
AI Insights & Alerts
Step 1 — System Monitoring

The monitoring agent uses Python and psutil to collect system-level information.

The application collects:

CPU utilization
RAM utilization
Disk utilization
Network bytes sent
Network bytes received
Timestamp

The monitoring script continuously collects new observations.

Example:

2026-09-30 18:10:20 | CPU: 35.4% | RAM: 72.1% | Disk: 82.6%
2026-09-30 18:10:35 | CPU: 48.2% | RAM: 73.0% | Disk: 82.6%
2026-09-30 18:10:50 | CPU: 91.7% | RAM: 75.4% | Disk: 82.6%
📊 Metrics Collected
Metric	Description
CPU	Current CPU utilization percentage
RAM	Current memory utilization percentage
Disk	Disk storage utilization percentage
Bytes Sent	Network data sent
Bytes Received	Network data received
Timestamp	Time at which the metric was collected

These metrics form the foundation of the project's analytics and machine
learning pipeline.

🗄️ Database Layer

The project uses Supabase PostgreSQL as the cloud database.

The main table is:

system_metrics
Database Schema
CREATE TABLE system_metrics (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    cpu REAL,
    ram REAL,
    disk REAL,
    bytes_sent BIGINT,
    bytes_received BIGINT
);
Database Responsibilities

The database is responsible for:

Storing real-time monitoring data
Maintaining historical records
Providing data for analytics
Providing training data for ML models
Supporting historical trend analysis
Supporting model retraining

The application retrieves historical records directly from Supabase
whenever analytics or machine learning operations are performed.

🧹 Data Processing & Feature Engineering

Before training the machine learning model, the raw monitoring data is
processed using Pandas.

The application performs:

Timestamp conversion
Sorting by timestamp
Rolling averages
Difference calculations
Missing-value removal
Feature selection
Train/test splitting
Generated Features

The CPU prediction model uses the following features:

cpu
ram
disk
cpu_avg
ram_avg
cpu_change
ram_change
Rolling Average

The application calculates rolling averages for CPU and RAM utilization.

df["cpu_avg"] = df["cpu"].rolling(12).mean()
df["ram_avg"] = df["ram"].rolling(12).mean()

These features provide the model with information about recent system
behavior rather than relying only on the current metric.

🤖 Machine Learning

The project contains two machine learning components:

1. CPU Prediction
2. Anomaly Detection
🔮 CPU Prediction

The CPU prediction component attempts to predict future CPU utilization
using historical system metrics.

The target is generated using:

df["future_cpu"] = df["cpu"].shift(-60)

The model uses:

CPU
RAM
Disk
CPU Rolling Average
RAM Rolling Average
CPU Change
RAM Change
Algorithm

The project uses:

Random Forest Regressor

Configuration:

RandomForestRegressor(
    n_estimators=50,
    random_state=42,
    n_jobs=1
)

The dataset is divided chronologically into:

80% → Training Data
20% → Testing Data

This preserves the time-series order instead of randomly shuffling
historical monitoring observations.

📈 CPU Prediction Pipeline
Supabase Data
      ↓
Pandas DataFrame
      ↓
Timestamp Sorting
      ↓
Feature Engineering
      ↓
Future CPU Target
      ↓
80/20 Time-Based Split
      ↓
Random Forest Regression
      ↓
Model Evaluation
      ↓
Save Model
      ↓
CPU Prediction

The trained model is stored at:

models/cpu_prediction_model.pkl
📏 Model Evaluation

The CPU prediction model is evaluated using:

Mean Absolute Error (MAE)

Measures the average absolute difference between actual and predicted
CPU utilization.

Root Mean Squared Error (RMSE)

Measures prediction error while giving larger errors more weight.

R² Score

Measures how well the model explains variation in the target variable.

Example training output from the current project:

======================================
MODEL RESULTS
======================================
MAE: 30.49
RMSE: 36.82
R2: -1.15

The current CPU prediction model demonstrates that the prediction pipeline
is functional, but the present dataset/model configuration does not provide
strong predictive performance.

This is an important limitation of the current implementation and an area
for future improvement.

🚨 Anomaly Detection

The second machine learning component identifies unusual system behavior.

The project uses:

Isolation Forest

Isolation Forest is an unsupervised machine learning algorithm suitable
for detecting unusual observations without requiring manually labeled
anomaly data.

The model analyzes:

CPU
RAM
Disk
🔍 Anomaly Detection Pipeline
Supabase Historical Data
          ↓
CPU / RAM / Disk
          ↓
Isolation Forest
          ↓
Normal / Anomaly
          ↓
Anomaly Count
          ↓
Dashboard Alerts

The model is configured using:

IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42,
    n_jobs=1
)

The trained anomaly model is stored at:

models/anomaly_model.pkl

Example output:

Training rows: 460
Total records: 460
Anomalies detected: 23

The detected anomalies can represent unusual combinations of CPU,
RAM, and disk utilization.

🧠 AI Insights

The dashboard combines monitoring information and machine learning
results to provide system-level insights.

Examples of dashboard insights include:

High CPU Usage Detected
High Memory Usage Detected
System Operating Normally
Potential Resource Pressure
Anomaly Detected

The purpose of these insights is to make raw system metrics easier to
understand without manually inspecting every data point.

⚙️ Real-Time Dashboard

The Streamlit application provides an interactive monitoring interface.

The dashboard includes:

System Status

Displays the current state of the system.

CPU Usage
RAM Usage
Disk Usage
System Status
📊 Performance Charts

Historical system metrics are visualized using Plotly.

Charts include:

CPU utilization over time
RAM utilization over time
Disk utilization over time
Network activity
Historical system trends

The dashboard allows users to select the number of historical records
displayed.

Available history options include:

50
100
150
200
250
300
🖥️ Process Monitoring

The project also monitors running Windows processes.

The process monitor identifies processes consuming significant system
resources.

The dashboard can display information such as:

Process Name
CPU Usage
Memory Usage
Process ID

This helps connect overall system resource usage with individual
processes.

For example:

High CPU Usage
       ↓
Process Monitoring
       ↓
Identify Resource-Heavy Process
       ↓
Investigate Application
📚 Historical Analytics

Historical data stored in Supabase can be analyzed through the dashboard.

Historical analytics help identify:

CPU usage patterns
Memory usage patterns
Disk utilization trends
Unusual resource spikes
Historical anomalies
Overall system behavior

Instead of only showing the current system state, the application
maintains a historical view of system performance.

🔄 Model Retraining

The project includes a model retraining workflow.

The retraining script executes:

1. CPU Prediction Model Training
2. Anomaly Detection Model Training

The workflow is:

New Monitoring Data
        ↓
Supabase
        ↓
Retrieve Historical Data
        ↓
Train CPU Prediction Model
        ↓
Train Anomaly Detection Model
        ↓
Save Updated Models

The retraining script is:

ml/retrain.py

It automatically executes:

ml.train
ml.anomaly

After successful execution:

models/cpu_prediction_model.pkl
models/anomaly_model.pkl

are updated with the newly trained models.

🎛️ AI Model Control

The Streamlit dashboard contains an AI Model Control section.

This allows the user to retrain the machine learning models using the
current Supabase dataset.

The dashboard displays:

Training records available

and provides the option to execute the model retraining workflow.

Example:

Training records available: 460

AI models retrained successfully.

This makes the project more than a static machine learning demo because
the models can be retrained as additional monitoring data becomes
available.

🧩 Project Modules

The project is divided into separate modules to keep monitoring,
database operations, machine learning, and visualization organized.

monitoring/
    system_metrics.py
    process_monitor.py

database/
    database.py

ml/
    train.py
    predict.py
    anomaly.py
    retrain.py

models/
    cpu_prediction_model.pkl
    anomaly_model.pkl

app.py

Each module has a specific responsibility:

Module	Responsibility
system_metrics.py	Collect system metrics
process_monitor.py	Monitor running processes
database.py	Connect and interact with Supabase
train.py	Train CPU prediction model
predict.py	Generate CPU predictions
anomaly.py	Train anomaly detection model
retrain.py	Retrain both ML models
app.py	Streamlit dashboard
models/	Store trained ML models
🛠️ Technology Stack
Programming Language
Python
Monitoring
psutil
Data Analysis
Pandas
NumPy
Data Visualization
Plotly
Streamlit
Machine Learning
Scikit-learn
Random Forest Regression
Isolation Forest
Model Persistence
Joblib
Database
PostgreSQL
Supabase
psycopg2
Development Tools
VS Code
Git
GitHub
Python Virtual Environment
⭐ Key Features

The project currently includes:

Real-time CPU monitoring
Real-time RAM monitoring
Disk utilization monitoring
Network statistics
Running process monitoring
Cloud PostgreSQL database
Historical metric storage
Interactive Streamlit dashboard
Plotly data visualization
CPU prediction
Machine learning anomaly detection
AI-generated system insights
Historical analytics
Model evaluation
Model retraining
Persistent trained models
GitHub-ready project structure
give third part
Part 3 — Installation, Setup, Usage, GitHub, Limitations & Recruiter Summary

Copy this directly after Part 2 in your README.md:

# 🚀 Installation & Setup

Follow the steps below to run the project locally.

---

## 1. Clone the Repository

```bash
git clone https://github.com/precymichel/Ai-System-Monitor.git

Move into the project directory:

cd Ai-System-Monitor
2. Create a Virtual Environment

Create a Python virtual environment:

py -m venv venv

Activate the virtual environment on Windows:

venv\Scripts\activate

After activation, the terminal should show:

(venv)
3. Install Dependencies

Install the required Python packages:

python -m pip install -r requirements.txt

The project uses the following main dependencies:

streamlit
pandas
numpy
plotly
psutil
scikit-learn
joblib
psycopg2-binary
🔐 Supabase Configuration

The application uses Supabase PostgreSQL to store monitoring data.

Create a Supabase project and obtain the PostgreSQL connection string.

The project expects the database connection through:

DATABASE_URL
Windows Environment Variable

In the terminal, configure the database URL:

set DATABASE_URL=your_supabase_postgresql_connection_string

Example format:

postgresql://username:password@host:port/database

Do not commit your real database credentials to GitHub.

🗃️ Database Setup

The application automatically creates the required table through:

database/database.py

The database table is:

system_metrics

The structure contains:

id
timestamp
cpu
ram
disk
bytes_sent
bytes_received

You can also create the table manually in Supabase SQL Editor:

CREATE TABLE system_metrics (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    cpu REAL,
    ram REAL,
    disk REAL,
    bytes_sent BIGINT,
    bytes_received BIGINT
);
▶️ Running the Project

The project contains multiple components.

For the complete workflow, run the monitoring agent first.

Step 1 — Start System Monitoring

Open a terminal in the project directory:

venv\Scripts\activate

Set the database connection:

set DATABASE_URL=your_supabase_postgresql_connection_string

Run:

python monitoring\system_metrics.py

You should see:

======================================
AI SYSTEM MONITOR
======================================
Supabase database connected.
Collecting system data...
Press CTRL+C to stop.

2026-09-30 18:10:20 | CPU: 35.4% | RAM: 72.1% | Disk: 82.6%

The monitoring agent continuously collects new system metrics.

Press:

CTRL + C

to stop monitoring.

📊 Step 2 — Start the Streamlit Dashboard

Open another terminal.

Activate the virtual environment:

venv\Scripts\activate

Set the database connection:

set DATABASE_URL=your_supabase_postgresql_connection_string

Run:

streamlit run app.py

Streamlit will start the dashboard locally.

The terminal will display a local address similar to:

Local URL: http://localhost:8501

Open the URL in your browser.

🤖 Step 3 — Train the CPU Prediction Model

Make sure sufficient monitoring data has been collected.

Run:

python -m ml.train

The script retrieves monitoring data from Supabase and trains the CPU
prediction model.

Example:

======================================
AI SYSTEM MONITOR - CPU PREDICTION
======================================

Total database records: 460
Training samples: 311
Testing samples: 78

======================================
MODEL RESULTS
======================================
MAE: 30.49
RMSE: 36.82
R2: -1.15

Model saved:
models/cpu_prediction_model.pkl
🔍 Step 4 — Train the Anomaly Detection Model

Run:

python -m ml.anomaly

The model analyzes CPU, RAM, and disk utilization.

Example:

======================================
AI SYSTEM MONITOR - ANOMALY DETECTION
======================================

Training rows: 460
Total records: 460
Anomalies detected: 23

Anomaly model saved:
models/anomaly_model.pkl

Anomaly detection completed successfully.
🔮 Step 5 — Generate CPU Prediction

Run:

python -m ml.predict

Example output:

======================================
AI CPU PREDICTION
======================================

Current CPU: 94.8%
Current RAM: 76.9%
Current Disk: 82.6%

Predicted CPU in 5 minutes: 45.0%

The prediction is generated using the trained Random Forest model.

🔄 Step 6 — Retrain All Models

The project provides a single command to retrain both machine learning
models:

python -m ml.retrain

The workflow performs:

CPU Prediction Model
        ↓
Anomaly Detection Model
        ↓
Updated Model Files

Example:

======================================
AI SYSTEM MONITOR - MODEL RETRAINING
======================================

[1/2] Training CPU prediction model...
--------------------------------------

CPU prediction training completed.

[2/2] Training anomaly detection model...
-----------------------------------------

Anomaly detection completed successfully.

======================================
MODEL RETRAINING COMPLETED
======================================

Models updated successfully:
- CPU prediction model
- Anomaly detection model
🧪 Testing the Database Connection

Before running the complete application, the Supabase connection can be
tested with:

python -c "from database.database import create_database; create_database(); print('Supabase connected successfully!')"

Successful output:

Supabase connected successfully!
📁 Final Project Structure
Ai-System-Monitor/
│
├── app.py
│
├── monitoring/
│   ├── __init__.py
│   ├── system_metrics.py
│   └── process_monitor.py
│
├── database/
│   ├── __init__.py
│   └── database.py
│
├── ml/
│   ├── train.py
│   ├── predict.py
│   ├── anomaly.py
│   └── retrain.py
│
├── models/
│   ├── cpu_prediction_model.pkl
│   └── anomaly_model.pkl
│
├── data/
│   └── system_metrics.csv
│
├── requirements.txt
├── .gitignore
└── README.md
🔒 Security

Sensitive credentials should never be committed to GitHub.

The database connection should be provided through an environment
variable:

DATABASE_URL

The .gitignore file should contain:

venv/
__pycache__/
*.pyc
.env
data/*.db
data/*.csv
*.log

If using a .env file locally, make sure it is included in .gitignore.

Never upload:

Database passwords
API keys
Secret keys
Private credentials
Personal access tokens

to the public repository.

🧠 Engineering Decisions

Several technical decisions were made during development.

Why Python?

Python provides a strong ecosystem for:

System monitoring
Data analysis
Machine learning
Database integration
Dashboard development
Why psutil?

psutil provides access to system-level information such as:

CPU
Memory
Disk
Network
Processes

This makes it suitable for building a lightweight system monitoring
application.

Why Supabase?

Supabase provides a PostgreSQL database that can store monitoring data
outside the local application.

This allows the application to maintain historical data independently
from the Streamlit dashboard.

Why Streamlit?

Streamlit makes it possible to quickly build an interactive Python-based
analytics dashboard without requiring a separate frontend framework.

Why Random Forest?

Random Forest provides a practical baseline for regression using
multiple system metrics and engineered features.

It also provides a lightweight approach suitable for this project.

Why Isolation Forest?

Isolation Forest is suitable for unsupervised anomaly detection because
the monitoring dataset does not require manually labeled anomaly records.

🧩 Challenges Solved During Development

The project involved solving several real-world development issues.

1. Virtual Environment Issues

The project initially encountered Python environment and package
installation problems.

The virtual environment was recreated to provide a clean development
environment.

2. Dependency Problems

Machine learning dependencies required troubleshooting during
installation.

The final project uses a lightweight requirements.txt containing only
the packages required by the application.

3. Database Migration

The project initially used local storage and was later migrated to
Supabase PostgreSQL.

The database layer was redesigned to use:

psycopg2

and PostgreSQL queries.

4. Database Connection Issues

Connection and authentication issues were resolved by configuring the
Supabase PostgreSQL connection string correctly through:

DATABASE_URL
5. SQLite to Supabase Migration

The machine learning scripts originally depended on local SQLite data.

The following components were migrated to Supabase:

train.py
predict.py
anomaly.py
retrain.py

This allowed the entire ML pipeline to use the same historical dataset
stored in PostgreSQL.

6. Model Training with Limited Data

Machine learning models require sufficient historical records.

The project therefore collects monitoring data continuously before
training.

The dashboard also displays the number of available training records.

7. Streamlit Data Handling

The dashboard was designed to handle historical data retrieved from
Supabase and display it through interactive charts.

⚠️ Current Limitations

The current project is a working prototype and has several limitations.

CPU Prediction Accuracy

The current CPU prediction model has limited predictive performance.

The latest recorded evaluation was:

MAE: 30.49
RMSE: 36.82
R²: -1.15

Therefore, the CPU prediction feature should currently be considered an
experimental predictive analytics component rather than a production-grade
forecasting system.

Limited Dataset

The quality of predictions depends strongly on the amount and variety of
historical monitoring data.

Longer monitoring periods could provide more useful training data.

Local Execution

The current dashboard is designed primarily for local execution.

The monitoring agent needs to run on the machine whose system resources
are being monitored.

Windows Focus

The current implementation uses:

psutil.disk_usage("C:\\")

so the disk monitoring configuration is specifically focused on the
Windows C: drive.

🚀 Future Improvements

Possible future improvements include:

Improve CPU forecasting accuracy
Collect longer historical datasets
Add more time-series features
Add CPU forecasting using dedicated time-series models
Add RAM prediction
Add disk usage prediction
Add network traffic prediction
Add automated alert notifications
Add email alerts
Add Telegram alerts
Add configurable thresholds
Add model performance tracking
Add automated scheduled retraining
Add authentication
Add role-based dashboard access
Add Docker support
Add cloud deployment
Add CI/CD
Add automated testing
Add model versioning
Add database indexes for larger datasets
Add production monitoring
📌 Project Status
🟢 Real-Time Monitoring       → Completed
🟢 Supabase Database          → Completed
🟢 Historical Data Storage    → Completed
🟢 Streamlit Dashboard        → Completed
🟢 Process Monitoring         → Completed
🟢 CPU Prediction             → Implemented
🟢 Anomaly Detection          → Implemented
🟢 AI Insights                → Implemented
🟢 Model Retraining           → Implemented
🟢 GitHub Repository          → Completed
🟡 Prediction Accuracy        → Needs Improvement
🟡 Production Deployment      → Future Work
🎥 Demo

The project can be demonstrated locally using the Streamlit dashboard.

Start the monitoring agent:

python monitoring\system_metrics.py

Then start the dashboard:

streamlit run app.py

Open:

http://localhost:8501

The dashboard demonstrates:

Real-time system metrics
Historical charts
CPU/RAM/Disk analysis
Process monitoring
AI insights
Anomaly detection
CPU prediction
Model retraining
Supabase-backed historical data
📸 Screenshots

Add screenshots of the dashboard here.

Recommended screenshots:

1. Real-Time Dashboard
screenshots/dashboard.png
2. Performance Charts
screenshots/performance.png
3. AI Insights
screenshots/ai-insights.png
4. Anomaly Detection
screenshots/anomaly.png
5. Model Control
screenshots/model-control.png

Example Markdown:

![Dashboard](screenshots/dashboard.png)
💼 Skills Demonstrated

This project demonstrates practical experience in:

Python Development
Python programming
Modular application design
Exception handling
Environment management
Package management
Data Analytics
Pandas
NumPy
Data preprocessing
Feature engineering
Historical trend analysis
Data visualization
Machine Learning
Supervised learning
Random Forest Regression
Unsupervised learning
Isolation Forest
Model evaluation
Model persistence
Model retraining
Database
PostgreSQL
Supabase
SQL
Database connectivity
CRUD operations
Historical data storage
Dashboard Development
Streamlit
Plotly
Interactive charts
Real-time monitoring interfaces
Analytics dashboards
Software Engineering
Modular project structure
Virtual environments
Git
GitHub
Requirements management
Environment variables
Debugging
📈 What This Project Demonstrates to Recruiters

This project demonstrates the ability to build a complete data and
machine learning application rather than only training an isolated model.

The complete workflow includes:

Data Collection
      ↓
Data Storage
      ↓
Data Processing
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Model Evaluation
      ↓
Prediction
      ↓
Anomaly Detection
      ↓
Visualization
      ↓
Dashboard
      ↓
Model Retraining

This demonstrates practical exposure to the complete lifecycle of a
data-driven application.

👩‍💻 Author
Michel Prescilla V

B.Tech Computer Science and Engineering

Aspiring:

Data Analyst
Frontend Developer
AI/Data Applications Developer

Interested in building practical applications combining:

Data Analytics
+
Artificial Intelligence
+
Machine Learning
+
Frontend Development
🔗 Project Repository

GitHub:

https://github.com/precymichel/Ai-System-Monitor

