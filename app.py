import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import time
import joblib
import psutil
import sqlite3
import subprocess
import sys
from datetime import datetime


# ==================================================
# FILE PATHS
# ==================================================

DATABASE_FILE = "data/system_metrics.db"

CPU_MODEL_FILE = "models/cpu_prediction_model.pkl"

ANOMALY_MODEL_FILE = "models/anomaly_model.pkl"


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI System Monitor",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("AI-Powered Real-Time System Monitor")

st.caption(
    "Real-time monitoring with AI prediction, "
    "anomaly detection, process analysis and SQLite"
)


# ==================================================
# CHECK DATABASE
# ==================================================

if not os.path.exists(DATABASE_FILE):

    st.warning("SQLite database not found.")

    st.info(
        "Start the monitoring script first:\n\n"
        "python -m monitoring.system_metrics"
    )

    st.stop()


# ==================================================
# LOAD SQLITE DATA
# ==================================================

try:

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

except Exception as e:

    st.error(
        f"Database error: {e}"
    )

    st.stop()


# ==================================================
# CHECK DATA
# ==================================================

if df.empty:

    st.warning(
        "No system metrics available yet."
    )

    st.info(
        "Keep the monitoring script running."
    )

    st.stop()


# ==================================================
# TIMESTAMP
# ==================================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)

latest = df.iloc[-1]


# ==================================================
# CURRENT VALUES
# ==================================================

cpu = float(latest["cpu"])

ram = float(latest["ram"])

disk = float(latest["disk"])


# ==================================================
# NETWORK SPEED
# ==================================================

upload_speed = 0

download_speed = 0


if len(df) >= 2:

    previous = df.iloc[-2]

    time_difference = (
        latest["timestamp"]
        - previous["timestamp"]
    ).total_seconds()

    if time_difference > 0:

        upload_speed = (
            float(latest["bytes_sent"])
            - float(previous["bytes_sent"])
        ) / time_difference

        download_speed = (
            float(latest["bytes_received"])
            - float(previous["bytes_received"])
        ) / time_difference


upload_kbps = max(
    0,
    upload_speed / 1024
)

download_kbps = max(
    0,
    download_speed / 1024
)


# ==================================================
# CPU PREDICTION
# ==================================================

prediction = None


if (
    os.path.exists(CPU_MODEL_FILE)
    and len(df) >= 13
):

    try:

        cpu_model = joblib.load(
            CPU_MODEL_FILE
        )

        ml_df = df.copy()

        ml_df["cpu_avg"] = (
            ml_df["cpu"]
            .rolling(12)
            .mean()
        )

        ml_df["ram_avg"] = (
            ml_df["ram"]
            .rolling(12)
            .mean()
        )

        ml_df["cpu_change"] = (
            ml_df["cpu"]
            .diff()
        )

        ml_df["ram_change"] = (
            ml_df["ram"]
            .diff()
        )

        ml_df = ml_df.dropna()

        if len(ml_df) > 0:

            latest_ml = ml_df.iloc[-1]

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
                latest_ml[features]
                .to_frame()
                .T
            )

            prediction = cpu_model.predict(
                X_latest
            )[0]

            prediction = max(
                0,
                min(100, prediction)
            )

    except Exception as e:

        st.warning(
            f"CPU prediction error: {e}"
        )


# ==================================================
# ANOMALY DETECTION
# ==================================================

anomaly_status = "Normal"


if os.path.exists(ANOMALY_MODEL_FILE):

    try:

        anomaly_model = joblib.load(
            ANOMALY_MODEL_FILE
        )

        anomaly_features = [
            "cpu",
            "ram",
            "disk"
        ]

        X_anomaly = (
            latest[anomaly_features]
            .to_frame()
            .T
        )

        anomaly_result = (
            anomaly_model
            .predict(X_anomaly)[0]
        )

        if anomaly_result == -1:

            anomaly_status = "Anomaly Detected"

        else:

            anomaly_status = "Normal"

    except Exception as e:

        st.warning(
            f"Anomaly detection error: {e}"
        )


# ==================================================
# RISK LEVEL
# ==================================================

alerts = []


if cpu >= 90:

    alerts.append(
        f"CPU usage is critically high at {cpu:.1f}%."
    )

elif cpu >= 70:

    alerts.append(
        f"CPU usage is high at {cpu:.1f}%."
    )


if ram >= 90:

    alerts.append(
        f"RAM usage is critically high at {ram:.1f}%."
    )

elif ram >= 80:

    alerts.append(
        f"RAM usage is high at {ram:.1f}%."
    )


if disk >= 90:

    alerts.append(
        f"Disk storage usage is very high at {disk:.1f}%."
    )


if anomaly_status == "Anomaly Detected":

    alerts.append(
        "AI anomaly detection identified unusual "
        "system behavior."
    )


if (
    anomaly_status == "Anomaly Detected"
    or cpu >= 90
    or ram >= 90
):

    risk_level = "CRITICAL"

elif (
    cpu >= 70
    or ram >= 80
    or disk >= 90
):

    risk_level = "WARNING"

else:

    risk_level = "NORMAL"


# ==================================================
# CURRENT METRICS
# ==================================================

st.subheader(
    "💻 Current System Metrics"
)


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "CPU Usage",
        f"{cpu:.1f}%"
    )


with col2:

    st.metric(
        "RAM Usage",
        f"{ram:.1f}%"
    )


with col3:

    st.metric(
        "Disk Usage",
        f"{disk:.1f}%"
    )


with col4:

    st.metric(
        "Upload Speed",
        f"{upload_kbps:.1f} KB/s"
    )


with col5:

    st.metric(
        "Download Speed",
        f"{download_kbps:.1f} KB/s"
    )


st.divider()


# ==================================================
# SYSTEM ALERT
# ==================================================

st.subheader(
    "🚨 System Alert"
)


if risk_level == "CRITICAL":

    st.error(
        "CRITICAL: Immediate attention required."
    )

    for alert in alerts:

        st.write(
            "•",
            alert
        )


elif risk_level == "WARNING":

    st.warning(
        "WARNING: System resources are under high load."
    )

    for alert in alerts:

        st.write(
            "•",
            alert
        )


else:

    st.success(
        "NORMAL: System resources are operating normally."
    )

    st.write(
        "No significant system issues detected."
    )


st.divider()


# ==================================================
# AI SYSTEM ANALYSIS
# ==================================================

st.subheader(
    "🤖 AI System Analysis"
)


col1, col2, col3 = st.columns(3)


with col1:

    if prediction is not None:

        st.metric(
            "Predicted CPU in 5 Minutes",
            f"{prediction:.1f}%"
        )

    else:

        st.warning(
            "CPU prediction unavailable."
        )


with col2:

    st.metric(
        "Anomaly Detection",
        anomaly_status
    )


with col3:

    st.metric(
        "System Risk Level",
        risk_level
    )


st.divider()


# ==================================================
# AI MODEL CONTROL
# ==================================================

st.subheader(
    "🧠 AI Model Control"
)


col1, col2, col3 = st.columns(3)


with col1:

    if os.path.exists(CPU_MODEL_FILE):

        st.success(
            "CPU Prediction Model: Ready"
        )

    else:

        st.error(
            "CPU Prediction Model: Missing"
        )


with col2:

    if os.path.exists(ANOMALY_MODEL_FILE):

        st.success(
            "Anomaly Model: Ready"
        )

    else:

        st.error(
            "Anomaly Model: Missing"
        )


with col3:

    st.info(
        f"Training Records: {len(df)}"
    )


st.write("")


if st.button(
    "🔄 Retrain AI Models",
    use_container_width=True
):

    with st.spinner(
        "Training AI models..."
    ):

        result = subprocess.run(
            [
                sys.executable,
                "ml/retrain.py"
            ],
            capture_output=True,
            text=True
        )


    if result.returncode == 0:

        st.success(
            "AI models retrained successfully!"
        )

        with st.expander(
            "View Training Output"
        ):

            st.code(
                result.stdout
            )

        st.rerun()

    else:

        st.error(
            "Model retraining failed."
        )

        with st.expander(
            "View Error"
        ):

            st.code(
                result.stderr
            )


st.divider()


# ==================================================
# HISTORICAL PERFORMANCE
# ==================================================

st.subheader(
    "📊 Historical Performance"
)


cpu_average = df["cpu"].mean()

cpu_min = df["cpu"].min()

cpu_max = df["cpu"].max()


ram_average = df["ram"].mean()

ram_min = df["ram"].min()

ram_max = df["ram"].max()


disk_average = df["disk"].mean()

disk_min = df["disk"].min()

disk_max = df["disk"].max()


# CPU statistics

st.markdown(
    "### CPU Statistics"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Average CPU",
        f"{cpu_average:.1f}%"
    )


with col2:

    st.metric(
        "Minimum CPU",
        f"{cpu_min:.1f}%"
    )


with col3:

    st.metric(
        "Maximum CPU",
        f"{cpu_max:.1f}%"
    )


# RAM statistics

st.markdown(
    "### RAM Statistics"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Average RAM",
        f"{ram_average:.1f}%"
    )


with col2:

    st.metric(
        "Minimum RAM",
        f"{ram_min:.1f}%"
    )


with col3:

    st.metric(
        "Maximum RAM",
        f"{ram_max:.1f}%"
    )


# Disk statistics

st.markdown(
    "### Disk Statistics"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Average Disk",
        f"{disk_average:.1f}%"
    )


with col2:

    st.metric(
        "Minimum Disk",
        f"{disk_min:.1f}%"
    )


with col3:

    st.metric(
        "Maximum Disk",
        f"{disk_max:.1f}%"
    )


st.divider()


# ==================================================
# SYSTEM HEALTH
# ==================================================

st.subheader(
    "🩺 Overall System Health"
)


health_score = 100


if cpu >= 90:

    health_score -= 30

elif cpu >= 70:

    health_score -= 15


if ram >= 90:

    health_score -= 30

elif ram >= 80:

    health_score -= 15


if disk >= 90:

    health_score -= 20


if anomaly_status == "Anomaly Detected":

    health_score -= 20


health_score = max(
    0,
    min(100, health_score)
)


if health_score >= 80:

    health_status = "Healthy"

elif health_score >= 60:

    health_status = "Moderate"

else:

    health_status = "Needs Attention"


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "System Health Score",
        f"{health_score}/100"
    )


with col2:

    st.metric(
        "Health Status",
        health_status
    )


st.divider()


# ==================================================
# TOP PROCESSES
# ==================================================

st.subheader(
    "📋 Top CPU-Consuming Processes"
)


processes = []


for process in psutil.process_iter(
    ["pid", "name", "memory_percent"]
):

    try:

        process.cpu_percent(
            interval=None
        )

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):

        continue


time.sleep(1)


for process in psutil.process_iter(
    ["pid", "name", "memory_percent"]
):

    try:

        process_name = process.info["name"]


        if process_name == "System Idle Process":

            continue


        cpu_usage = process.cpu_percent(
            interval=None
        )


        ram_usage = process.info[
            "memory_percent"
        ]


        processes.append({

            "PID": process.info["pid"],

            "Process": process_name,

            "CPU (%)": round(
                cpu_usage,
                1
            ),

            "RAM (%)": round(
                ram_usage,
                1
            )

        })


    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):

        continue


processes.sort(
    key=lambda x: x["CPU (%)"],
    reverse=True
)


top_processes = processes[:10]


if top_processes:

    process_df = pd.DataFrame(
        top_processes
    )

    st.dataframe(
        process_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No process information available."
    )


st.divider()


# ==================================================
# CPU GRAPH
# ==================================================

st.subheader(
    "📈 CPU Usage"
)


cpu_fig = go.Figure()


cpu_fig.add_trace(
    go.Scatter(
        x=df["timestamp"],
        y=df["cpu"],
        mode="lines",
        name="CPU Usage"
    )
)


cpu_fig.update_layout(
    xaxis_title="Time",
    yaxis_title="CPU Usage (%)",
    yaxis=dict(
        range=[0, 100]
    )
)


st.plotly_chart(
    cpu_fig,
    use_container_width=True
)


# ==================================================
# RAM GRAPH
# ==================================================

st.subheader(
    "📈 RAM Usage"
)


ram_fig = go.Figure()


ram_fig.add_trace(
    go.Scatter(
        x=df["timestamp"],
        y=df["ram"],
        mode="lines",
        name="RAM Usage"
    )
)


ram_fig.update_layout(
    xaxis_title="Time",
    yaxis_title="RAM Usage (%)",
    yaxis=dict(
        range=[0, 100]
    )
)


st.plotly_chart(
    ram_fig,
    use_container_width=True
)


# ==================================================
# DISK GRAPH
# ==================================================

st.subheader(
    "📈 Disk Usage"
)


disk_fig = go.Figure()


disk_fig.add_trace(
    go.Scatter(
        x=df["timestamp"],
        y=df["disk"],
        mode="lines",
        name="Disk Usage"
    )
)


disk_fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Disk Usage (%)",
    yaxis=dict(
        range=[0, 100]
    )
)


st.plotly_chart(
    disk_fig,
    use_container_width=True
)


# ==================================================
# NETWORK GRAPH
# ==================================================

st.subheader(
    "🌐 Network Traffic"
)


if len(df) >= 2:

    network_df = df.copy()

    network_df["time_diff"] = (
        network_df["timestamp"]
        .diff()
        .dt.total_seconds()
    )

    network_df["upload_kbps"] = (
        network_df["bytes_sent"]
        .diff()
        / network_df["time_diff"]
        / 1024
    )

    network_df["download_kbps"] = (
        network_df["bytes_received"]
        .diff()
        / network_df["time_diff"]
        / 1024
    )

    network_df = network_df.dropna()


    network_fig = go.Figure()


    network_fig.add_trace(
        go.Scatter(
            x=network_df["timestamp"],
            y=network_df["upload_kbps"],
            mode="lines",
            name="Upload"
        )
    )


    network_fig.add_trace(
        go.Scatter(
            x=network_df["timestamp"],
            y=network_df["download_kbps"],
            mode="lines",
            name="Download"
        )
    )


    network_fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Speed (KB/s)"
    )


    st.plotly_chart(
        network_fig,
        use_container_width=True
    )

else:

    st.info(
        "Collecting enough network data..."
    )


st.divider()


# ==================================================
# RECENT METRICS
# ==================================================

st.subheader(
    "📋 Recent System Metrics"
)


st.dataframe(
    df[
        [
            "timestamp",
            "cpu",
            "ram",
            "disk",
            "bytes_sent",
            "bytes_received"
        ]
    ].tail(10),
    use_container_width=True,
    hide_index=True
)


# ==================================================
# DATABASE INFORMATION
# ==================================================

st.subheader(
    "🗄️ Database Information"
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Total Records",
        len(df)
    )


with col2:

    st.write(
        "Storage: SQLite"
    )


# ==================================================
# LAST UPDATE
# ==================================================

st.caption(
    f"Last data update: "
    f"{latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
)


# ==================================================
# AUTO REFRESH
# ==================================================

time.sleep(5)

st.rerun()