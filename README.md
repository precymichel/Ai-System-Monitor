\# AI-Powered Real-Time System Monitoring \& Predictive Analytics



An AI-powered system monitoring application that tracks real-time computer performance, stores historical metrics, detects abnormal system behavior, and predicts future CPU usage using machine learning.



\## Features



\- Real-time CPU monitoring

\- RAM usage monitoring

\- Disk usage monitoring

\- Network traffic monitoring

\- Top CPU-consuming processes

\- Historical performance analysis

\- SQLite database for metric storage

\- CPU usage prediction using Random Forest

\- System anomaly detection using Isolation Forest

\- Automatic system risk classification

\- System health score

\- Real-time alerts

\- Streamlit dashboard

\- Plotly visualizations

\- AI model retraining

\- Automatic data collection



\## Technologies Used



\- Python

\- Streamlit

\- Pandas

\- NumPy

\- Scikit-learn

\- Plotly

\- psutil

\- SQLite

\- Joblib



\## Machine Learning



\### CPU Prediction



A Random Forest Regression model is used to predict CPU usage approximately 5 minutes into the future.



Features include:



\- Current CPU usage

\- Current RAM usage

\- Disk usage

\- Rolling CPU average

\- Rolling RAM average

\- CPU change

\- RAM change



\### Anomaly Detection



Isolation Forest is used to identify unusual system behavior based on:



\- CPU usage

\- RAM usage

\- Disk usage



\## Project Structure



```text

Ai-System-Monitor/

│

├── app.py

├── requirements.txt

├── README.md

│

├── monitoring/

│   ├── system\_metrics.py

│   └── process\_monitor.py

│

├── database/

│   ├── \_\_init\_\_.py

│   └── database.py

│

├── ml/

│   ├── train.py

│   ├── predict.py

│   ├── anomaly.py

│   └── retrain.py

│

├── models/

│   ├── cpu\_prediction\_model.pkl

│   └── anomaly\_model.pkl

│

└── data/

&#x20;   └── system\_metrics.db







Installation



Clone the repository:



git clone YOUR\_GITHUB\_REPOSITORY\_URL



Go to the project directory:



cd Ai-System-Monitor



Create a virtual environment:



python -m venv venv



Activate the virtual environment on Windows:



venv\\Scripts\\activate



Install dependencies:



pip install -r requirements.txt

Running the Project

1\. Start system monitoring



Open Terminal 1:



python -m monitoring.system\_metrics



This continuously collects system metrics and stores them in SQLite.



2\. Start the dashboard



Open Terminal 2:



streamlit run app.py



The Streamlit dashboard will open in your browser.



Running Machine Learning



Train the CPU prediction model:



python ml/train.py



Train the anomaly detection model:



python ml/anomaly.py



Generate a CPU prediction:



python ml/predict.py



Retrain both models:



python ml/retrain.py

System Risk Levels



The dashboard classifies system conditions into:



NORMAL

WARNING

CRITICAL



Risk classification considers CPU, RAM, disk usage, and detected anomalies.



Database



Historical monitoring data is stored in:



data/system\_metrics.db



The database stores:



Timestamp

CPU usage

RAM usage

Disk usage

Network bytes sent

Network bytes received

Future Improvements

Improve CPU prediction accuracy with more historical data

Add additional prediction models

Add configurable alert thresholds

Add email notifications

Add deployment support

Add authentication

Improve dashboard UI

Add model performance tracking

Author



Michel Prescilla V



B.Tech Computer Science and Engineering



Project Type



Machine Learning | Python | Data Analytics | System Monitoring | Streamlit

