# 🤖 AI-Powered Real-Time System Monitoring & Predictive Analytics

An end-to-end **AI-powered system monitoring and predictive analytics application** built with Python.

The system continuously monitors computer performance, stores real-time metrics in **Supabase PostgreSQL**, performs data analysis, uses Machine Learning to **predict CPU utilization and detect abnormal system behavior**, and presents the results through an interactive **Streamlit dashboard**.

---

## 📌 Overview

Modern computers continuously generate large amounts of system performance data such as CPU utilization, memory usage, disk usage, network activity, and process information.

This project was developed to transform this raw system data into useful insights using **Data Analytics and Machine Learning**.

The application follows a complete data pipeline:

```text
System Monitoring
       ↓
Data Collection
       ↓
Supabase PostgreSQL
       ↓
Data Processing
       ↓
Feature Engineering
       ↓
Machine Learning
       ↓
Prediction & Anomaly Detection
       ↓
Streamlit Dashboard
       ↓
AI Insights & Alerts
