import psutil
import time
from datetime import datetime

from database.database import create_database, save_metrics


# ==================================================
# INITIALIZE DATABASE
# ==================================================

create_database()


# ==================================================
# COLLECT SYSTEM METRICS
# ==================================================

def get_system_metrics():

    cpu = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()
    ram = memory.percent

    disk = psutil.disk_usage("C:\\")
    disk_usage = disk.percent

    network = psutil.net_io_counters()

    return {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "cpu": cpu,
        "ram": ram,
        "disk": disk_usage,
        "bytes_sent": network.bytes_sent,
        "bytes_received": network.bytes_recv
    }


# ==================================================
# START MONITORING
# ==================================================

if __name__ == "__main__":

    print("AI SYSTEM MONITOR")
    print("=================")

    print("SQLite database connected.")

    print("Collecting system data...")

    print("Press CTRL+C to stop.\n")


    while True:

        metrics = get_system_metrics()

        # Save to SQLite
        save_metrics(metrics)


        print(
            f"{metrics['timestamp']} | "
            f"CPU: {metrics['cpu']:.1f}% | "
            f"RAM: {metrics['ram']:.1f}% | "
            f"Disk: {metrics['disk']:.1f}%"
        )


        time.sleep(5)