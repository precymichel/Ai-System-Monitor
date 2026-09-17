import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sqlite3
import psutil
import os
import subprocess
import sys
import time


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI System Monitor",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE PATHS
# ============================================================

DATABASE_FILE = "data/system_metrics.db"
CPU_MODEL_FILE = "models/cpu_prediction_model.pkl"
ANOMALY_MODEL_FILE = "models/anomaly_model.pkl"


# ============================================================
# CUSTOM STREAMLIT CSS
# No HTML cards are used.
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #080c14;
    }

    [data-testid="stSidebar"] {
        background-color: #0c111b;
        border-right: 1px solid #202938;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
    }

    h2 {
        font-size: 1.5rem !important;
        font-weight: 750 !important;
    }

    h3 {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetric"] {
        background-color: #111722;
        border: 1px solid #273244;
        border-radius: 16px;
        padding: 18px;
        min-height: 130px;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc;
        font-weight: 800;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 0.85rem;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #0f1520;
        border: 1px solid #202b3d;
        border-radius: 16px;
    }

    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 650;
    }

    .stProgress > div > div > div > div {
        border-radius: 10px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #202b3d;
        border-radius: 14px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return sqlite3.connect(DATABASE_FILE)


@st.cache_data(ttl=3)
def load_metrics(limit=150):

    if not os.path.exists(DATABASE_FILE):
        return pd.DataFrame()

    connection = get_connection()

    query = """
        SELECT
            timestamp,
            cpu,
            ram,
            disk,
            bytes_sent,
            bytes_received
        FROM system_metrics
        ORDER BY id DESC
        LIMIT ?
    """

    df = pd.read_sql_query(
        query,
        connection,
        params=(limit,)
    )

    connection.close()

    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df = df.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    return df


def get_total_records():

    if not os.path.exists(DATABASE_FILE):
        return 0

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM system_metrics"
    )

    result = cursor.fetchone()[0]

    connection.close()

    return result


# ============================================================
# SYSTEM STATUS
# ============================================================

def resource_status(
    value,
    warning,
    critical
):

    if value >= critical:
        return "CRITICAL"

    if value >= warning:
        return "WARNING"

    return "NORMAL"


def calculate_risk(
    cpu,
    ram,
    disk,
    anomaly
):

    if anomaly or cpu >= 90 or ram >= 90:
        return "CRITICAL"

    if cpu >= 70 or ram >= 80 or disk >= 90:
        return "WARNING"

    return "NORMAL"


def calculate_health(
    cpu,
    ram,
    disk,
    anomaly
):

    score = 100

    if cpu >= 90:
        score -= 30

    elif cpu >= 70:
        score -= 15

    if ram >= 90:
        score -= 30

    elif ram >= 80:
        score -= 15

    if disk >= 90:
        score -= 20

    if anomaly:
        score -= 20

    return max(
        0,
        min(100, score)
    )


# ============================================================
# CPU PREDICTION
# ============================================================

def get_cpu_prediction(df):

    if not os.path.exists(
        CPU_MODEL_FILE
    ):
        return None

    if len(df) < 70:
        return None

    try:

        import joblib

        model = joblib.load(
            CPU_MODEL_FILE
        )

        data = df.copy()

        data["cpu_avg"] = (
            data["cpu"]
            .rolling(12)
            .mean()
        )

        data["ram_avg"] = (
            data["ram"]
            .rolling(12)
            .mean()
        )

        data["cpu_change"] = (
            data["cpu"]
            .diff()
        )

        data["ram_change"] = (
            data["ram"]
            .diff()
        )

        data = data.dropna()

        if data.empty:
            return None

        latest = data.iloc[-1]

        features = pd.DataFrame([{
            "cpu": latest["cpu"],
            "ram": latest["ram"],
            "disk": latest["disk"],
            "cpu_avg": latest["cpu_avg"],
            "ram_avg": latest["ram_avg"],
            "cpu_change": latest["cpu_change"],
            "ram_change": latest["ram_change"]
        }])

        prediction = model.predict(
            features
        )[0]

        return max(
            0,
            min(100, float(prediction))
        )

    except Exception:
        return None


# ============================================================
# ANOMALY DETECTION
# ============================================================

def get_anomaly(df):

    if not os.path.exists(
        ANOMALY_MODEL_FILE
    ):
        return False

    if len(df) < 20:
        return False

    try:

        import joblib

        model = joblib.load(
            ANOMALY_MODEL_FILE
        )

        latest = df[
            ["cpu", "ram", "disk"]
        ].tail(1)

        result = model.predict(
            latest
        )[0]

        return result == -1

    except Exception:
        return False


# ============================================================
# TOP PROCESSES
# ============================================================

def get_top_processes():

    processes = []

    try:

        for process in psutil.process_iter(
            ["pid", "name"]
        ):

            try:
                process.cpu_percent(
                    None
                )
            except:
                pass

        time.sleep(0.35)

        for process in psutil.process_iter(
            ["pid", "name", "memory_percent"]
        ):

            try:

                name = process.info.get(
                    "name"
                )

                if name == "System Idle Process":
                    continue

                cpu = process.cpu_percent(
                    None
                )

                ram = process.info.get(
                    "memory_percent",
                    0
                )

                processes.append({
                    "Process": name,
                    "PID": process.info["pid"],
                    "CPU %": round(
                        cpu,
                        1
                    ),
                    "RAM %": round(
                        ram,
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
            key=lambda x: x["CPU %"],
            reverse=True
        )

        return pd.DataFrame(
            processes[:10]
        )

    except Exception:

        return pd.DataFrame()


# ============================================================
# RESOURCE CHART
# ============================================================

def resource_chart(
    df,
    column,
    title
):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df[column],
            mode="lines",
            line=dict(
                width=2.5
            ),
            fill="tozeroy",
            hovertemplate=(
                "%{x}<br>"
                "%{y:.1f}%"
                "<extra></extra>"
            )
        )
    )

    fig.add_hline(
        y=70,
        line_dash="dash",
        annotation_text="Warning"
    )

    fig.add_hline(
        y=90,
        line_dash="dash",
        annotation_text="Critical"
    )

    fig.update_layout(
        title=title,
        height=330,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        ),
        paper_bgcolor="#0f1520",
        plot_bgcolor="#0f1520",
        font=dict(
            color="#cbd5e1"
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridcolor="#202938"
        ),
        hovermode="x unified"
    )

    return fig


# ============================================================
# NETWORK CHART
# ============================================================

def network_chart(df):

    data = df.copy()

    data["upload_mb"] = (
        data["bytes_sent"]
        .diff()
        .clip(lower=0)
        / 1024
        / 1024
    )

    data["download_mb"] = (
        data["bytes_received"]
        .diff()
        .clip(lower=0)
        / 1024
        / 1024
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["timestamp"],
            y=data["upload_mb"],
            mode="lines",
            name="Upload"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["timestamp"],
            y=data["download_mb"],
            mode="lines",
            name="Download"
        )
    )

    fig.update_layout(
        title="Network Traffic",
        height=330,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        ),
        paper_bgcolor="#0f1520",
        plot_bgcolor="#0f1520",
        font=dict(
            color="#cbd5e1"
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            title="MB",
            showgrid=True,
            gridcolor="#202938"
        )
    )

    return fig


# ============================================================
# LOAD DATA
# ============================================================

df = load_metrics(150)


# ============================================================
# NO DATA
# ============================================================

if df.empty:

    st.title(
        "🖥️ AI System Monitor"
    )

    st.caption(
        "Real-Time Monitoring & Predictive Analytics"
    )

    st.warning(
        "No monitoring data is available."
    )

    st.code(
        "python -m monitoring.system_metrics",
        language="cmd"
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(
        "🖥️ AI Monitor"
    )

    st.caption(
        "System Intelligence Center"
    )

    st.divider()

    st.subheader(
        "⚙️ Monitoring"
    )

    refresh_seconds = st.slider(
        "Refresh interval",
        3,
        15,
        5
    )

    history_limit = st.selectbox(
        "History records",
        [50, 100, 150],
        index=2
    )

    st.divider()

    st.subheader(
        "🤖 AI Models"
    )

    if os.path.exists(
        CPU_MODEL_FILE
    ):

        st.success(
            "CPU Prediction Ready"
        )

    else:

        st.warning(
            "CPU Prediction Missing"
        )

    if os.path.exists(
        ANOMALY_MODEL_FILE
    ):

        st.success(
            "Anomaly Model Ready"
        )

    else:

        st.warning(
            "Anomaly Model Missing"
        )

    st.divider()

    st.subheader(
        "🗄️ Database"
    )

    st.metric(
        "Records",
        get_total_records()
    )

    if os.path.exists(
        DATABASE_FILE
    ):

        st.success(
            "SQLite Connected"
        )

    st.divider()

    st.caption(
        "Python • psutil • SQLite\n"
        "Scikit-learn • Plotly • Streamlit"
    )


# Reload selected history
df = load_metrics(
    history_limit
)

latest = df.iloc[-1]

cpu = float(latest["cpu"])
ram = float(latest["ram"])
disk = float(latest["disk"])


# ============================================================
# AI
# ============================================================

prediction = get_cpu_prediction(
    df
)

anomaly = get_anomaly(
    df
)

risk = calculate_risk(
    cpu,
    ram,
    disk,
    anomaly
)

health = calculate_health(
    cpu,
    ram,
    disk,
    anomaly
)

cpu_status = resource_status(
    cpu,
    70,
    90
)

ram_status = resource_status(
    ram,
    80,
    90
)

disk_status = resource_status(
    disk,
    90,
    95
)


# ============================================================
# HEADER
# ============================================================

title_col, status_col = st.columns(
    [5, 1]
)

with title_col:

    st.title(
        "🖥️ AI System Monitor"
    )

    st.caption(
        "Real-Time Monitoring & Predictive Analytics"
    )

with status_col:

    st.success(
        "● LIVE"
    )


st.divider()


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

st.header(
    "System Overview"
)

st.caption(
    "Current resource utilization of the monitored machine."
)

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "CPU Usage",
        f"{cpu:.1f}%",
        cpu_status
    )

    st.progress(
        min(cpu / 100, 1.0)
    )


with c2:

    st.metric(
        "Memory Usage",
        f"{ram:.1f}%",
        ram_status
    )

    st.progress(
        min(ram / 100, 1.0)
    )


with c3:

    st.metric(
        "Disk Usage",
        f"{disk:.1f}%",
        disk_status
    )

    st.progress(
        min(disk / 100, 1.0)
    )


with c4:

    st.metric(
        "System Health",
        f"{health}/100",
        risk
    )

    st.progress(
        health / 100
    )


# ============================================================
# AI INSIGHTS
# ============================================================

st.header(
    "🤖 AI Insights"
)

st.caption(
    "Machine-learning predictions and intelligent system analysis."
)

a1, a2, a3 = st.columns(3)


with a1:

    with st.container(border=True):

        st.subheader(
            "🔮 CPU Prediction"
        )

        if prediction is not None:

            st.metric(
                "Predicted CPU",
                f"{prediction:.1f}%"
            )

            if prediction >= 90:

                st.error(
                    "Predicted CPU load is critical."
                )

            elif prediction >= 70:

                st.warning(
                    "Predicted CPU load is elevated."
                )

            else:

                st.success(
                    "Predicted CPU load is within normal range."
                )

            st.caption(
                "Estimated CPU usage approximately 5 minutes ahead."
            )

        else:

            st.info(
                "CPU prediction model is not available."
            )


with a2:

    with st.container(border=True):

        st.subheader(
            "🧠 Anomaly Detection"
        )

        if anomaly:

            st.error(
                "ANOMALY DETECTED"
            )

            st.write(
                "The latest system metrics differ from learned normal patterns."
            )

        else:

            st.success(
                "SYSTEM NORMAL"
            )

            st.write(
                "No anomaly detected in the latest measurement."
            )

        st.caption(
            "Isolation Forest using CPU, RAM and disk."
        )


with a3:

    with st.container(border=True):

        st.subheader(
            "⚡ Risk Assessment"
        )

        if risk == "CRITICAL":

            st.error(
                "CRITICAL"
            )

            st.write(
                "Immediate attention may be required."
            )

        elif risk == "WARNING":

            st.warning(
                "WARNING"
            )

            st.write(
                "One or more system resources are elevated."
            )

        else:

            st.success(
                "NORMAL"
            )

            st.write(
                "System resources are within normal ranges."
            )

        st.caption(
            "Calculated from resources and anomaly detection."
        )


# ============================================================
# ALERTS
# ============================================================

st.header(
    "🚨 System Alerts"
)

alerts = []

if cpu >= 90:

    alerts.append(
        f"CPU usage is critically high: {cpu:.1f}%"
    )

elif cpu >= 70:

    alerts.append(
        f"CPU usage is elevated: {cpu:.1f}%"
    )

if ram >= 90:

    alerts.append(
        f"Memory usage is critically high: {ram:.1f}%"
    )

elif ram >= 80:

    alerts.append(
        f"Memory usage is elevated: {ram:.1f}%"
    )

if disk >= 90:

    alerts.append(
        f"Disk usage is high: {disk:.1f}%"
    )

if anomaly:

    alerts.append(
        "AI anomaly detection identified unusual system behavior."
    )


if alerts:

    for alert in alerts:

        st.warning(
            alert
        )

else:

    st.success(
        "✓ No active alerts. System is operating normally."
    )


# ============================================================
# PERFORMANCE
# ============================================================

st.header(
    "📈 Performance Trends"
)

st.caption(
    "Historical system resource utilization."
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "CPU",
        "Memory",
        "Disk",
        "Network"
    ]
)

with tab1:

    st.plotly_chart(
        resource_chart(
            df,
            "cpu",
            "CPU Usage"
        ),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

with tab2:

    st.plotly_chart(
        resource_chart(
            df,
            "ram",
            "Memory Usage"
        ),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

with tab3:

    st.plotly_chart(
        resource_chart(
            df,
            "disk",
            "Disk Usage"
        ),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

with tab4:

    st.plotly_chart(
        network_chart(df),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# TOP PROCESSES
# ============================================================

st.header(
    "🔥 Top CPU Processes"
)

st.caption(
    "Processes currently consuming the most CPU resources."
)

process_df = get_top_processes()

if not process_df.empty:

    st.dataframe(
        process_df,
        use_container_width=True,
        hide_index=True,
        column_config={

            "Process":
                st.column_config.TextColumn(
                    "Process"
                ),

            "PID":
                st.column_config.NumberColumn(
                    "PID"
                ),

            "CPU %":
                st.column_config.ProgressColumn(
                    "CPU Usage",
                    min_value=0,
                    max_value=100,
                    format="%.1f%%"
                ),

            "RAM %":
                st.column_config.ProgressColumn(
                    "RAM Usage",
                    min_value=0,
                    max_value=100,
                    format="%.1f%%"
                )
        }
    )

else:

    st.info(
        "Process information unavailable."
    )


# ============================================================
# HISTORICAL ANALYTICS
# ============================================================

st.header(
    "📊 Historical Analytics"
)

h1, h2, h3, h4, h5 = st.columns(5)

with h1:

    st.metric(
        "Average CPU",
        f"{df['cpu'].mean():.1f}%"
    )

with h2:

    st.metric(
        "Peak CPU",
        f"{df['cpu'].max():.1f}%"
    )

with h3:

    st.metric(
        "Average RAM",
        f"{df['ram'].mean():.1f}%"
    )

with h4:

    st.metric(
        "Peak RAM",
        f"{df['ram'].max():.1f}%"
    )

with h5:

    st.metric(
        "Peak Disk",
        f"{df['disk'].max():.1f}%"
    )


# ============================================================
# RAW DATA
# ============================================================

with st.expander(
    "🔍 View Recent Monitoring Data"
):

    display_df = df.tail(25).copy()

    display_df["timestamp"] = (
        display_df["timestamp"]
        .dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# AI MODEL CONTROL
# ============================================================

st.header(
    "⚙️ AI Model Control"
)

st.caption(
    "Retrain the prediction and anomaly detection models."
)

model_col1, model_col2 = st.columns(
    [4, 1]
)

with model_col1:

    st.info(
        f"Training records available: {get_total_records()}"
    )

with model_col2:

    retrain = st.button(
        "🔄 Retrain Models",
        use_container_width=True
    )


if retrain:

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
                "AI models retrained successfully."
            )

            with st.expander(
                "Training Output"
            ):

                st.code(
                    result.stdout
                )

            st.cache_data.clear()

        else:

            st.error(
                "Model retraining failed."
            )

            with st.expander(
                "Error Details"
            ):

                st.code(
                    result.stderr
                )


# ============================================================
# DATABASE INFORMATION
# ============================================================

with st.expander(
    "🗄️ Database Information"
):

    db1, db2, db3 = st.columns(3)

    with db1:

        st.metric(
            "Total Records",
            get_total_records()
        )

    with db2:

        st.metric(
            "Displayed Records",
            len(df)
        )

    with db3:

        st.metric(
            "Last Update",
            latest["timestamp"].strftime(
                "%H:%M:%S"
            )
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI System Monitor • "
    "Real-Time System Intelligence • "
    "Python + SQLite + Scikit-learn + Streamlit"
)


# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(
    refresh_seconds
)

st.rerun()