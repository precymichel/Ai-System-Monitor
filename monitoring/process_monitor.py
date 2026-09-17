import psutil
import time


def get_top_processes(limit=10):

    processes = []

    # Initialize CPU measurement
    for process in psutil.process_iter(
        ["pid", "name", "memory_percent"]
    ):
        try:
            process.cpu_percent(interval=None)
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    # Wait briefly for CPU measurement
    time.sleep(1)

    # Get CPU and RAM usage
    for process in psutil.process_iter(
        ["pid", "name", "memory_percent"]
    ):

        try:

            cpu = process.cpu_percent(interval=None)
            ram = process.info["memory_percent"]

            processes.append({
                "PID": process.info["pid"],
                "Process": process.info["name"],
                "CPU (%)": cpu,
                "RAM (%)": ram
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    # Sort by CPU usage
    processes.sort(
        key=lambda x: x["CPU (%)"],
        reverse=True
    )

    return processes[:limit]


if __name__ == "__main__":

    print("TOP SYSTEM PROCESSES")
    print("--------------------")

    top_processes = get_top_processes()

    for process in top_processes:

        print(
            f"{process['PID']:>6} | "
            f"{process['Process']:<30} | "
            f"CPU: {process['CPU (%)']:>6.1f}% | "
            f"RAM: {process['RAM (%)']:>6.1f}%"
        )