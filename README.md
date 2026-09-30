# 🤖 AI-Powered Real-Time System Monitoring & Predictive Analytics

An end-to-end Python project that monitors system resources in real time,
stores metrics in Supabase PostgreSQL, detects anomalies, predicts future
CPU usage, and visualizes system performance through an interactive
Streamlit dashboard.

## 🚀 Features

- Real-time CPU, RAM and Disk monitoring
- Network activity monitoring
- Running process monitoring
- Supabase PostgreSQL data storage
- Interactive Streamlit dashboard
- Historical performance analytics
- CPU usage prediction using Random Forest
- Anomaly detection using Isolation Forest
- AI-based system insights
- Machine learning model retraining

## 🏗️ Architecture

```text
Windows System
      ↓
Python + psutil
      ↓
Supabase PostgreSQL
      ↓
Data Processing
      ↓
Machine Learning
 ┌────┴─────────────┐
 ↓                  ↓
CPU Prediction   Anomaly Detection
 └────┬─────────────┘
      ↓
Streamlit Dashboard
##🛠️ Tech Stack
Python
Pandas & NumPy
Scikit-learn
Streamlit
Plotly
psutil
Supabase PostgreSQL
Joblib
Git & GitHub
##📁 Project Structure
Ai-System-Monitor/
│
├── app.py
├── monitoring/
│   ├── system_metrics.py
│   └── process_monitor.py
├── database/
│   └── database.py
├── ml/
│   ├── train.py
│   ├── predict.py
│   ├── anomaly.py
│   └── retrain.py
├── models/
│   ├── cpu_prediction_model.pkl
│   └── anomaly_model.pkl
├── requirements.txt
├── .gitignore
└── README.md
##⚙️ Installation

##Clone the repository:

git clone https://github.com/precymichel/Ai-System-Monitor.git
cd Ai-System-Monitor

##Create and activate virtual environment:

py -m venv venv
venv\Scripts\activate

##Install dependencies:

pip install -r requirements.txt
##🔐 Database Configuration

Set your Supabase PostgreSQL connection string:

set DATABASE_URL=your_supabase_database_url

Do not commit database credentials or .env files to GitHub.

▶️ Run the Project

Start system monitoring:

python monitoring\system_metrics.py

Start the Streamlit dashboard in another terminal:

streamlit run app.py

Open:

http://localhost:8501
🤖 Machine Learning
CPU Prediction

Uses Random Forest Regression to predict future CPU utilization based
on system metrics and engineered features.

Anomaly Detection

Uses Isolation Forest to identify unusual CPU, RAM and Disk usage
patterns.

Model Retraining

Both models can be retrained using:

python -m ml.retrain
📊 Dashboard

##The dashboard provides:

Current system status
CPU/RAM/Disk metrics
Performance charts
Process monitoring
Historical analytics
AI insights
Anomaly detection
CPU prediction
Model retraining controls
##🎯 Project Objective

The goal of this project is to demonstrate an end-to-end application
combining:

Real-Time Monitoring + Data Analytics + Machine Learning + Database +
Interactive Visualization

##⚠️ Current Limitation

The CPU prediction model is currently a prototype and its predictive
performance needs further improvement with larger datasets and enhanced
time-series features.

##🔮 Future Improvements
Improve prediction accuracy
Add RAM and Disk forecasting
Automated alerts
Email/Telegram notifications
Automated model retraining
Cloud deployment
Docker support
CI/CD pipeline
👩‍💻 Author

Michel Prescilla V

B.Tech Computer Science & Engineering

Interested in Data Analytics, AI, Machine Learning and Frontend
Development.

##🔗 GitHub

https://github.com/precymichel/Ai-System-Monitor
