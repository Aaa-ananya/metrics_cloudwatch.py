
import multiprocessing
import time
import os

# Number of CPU cores available
CPU_CORES = os.cpu_count() or 1

# Shared CPU load target
target_cpu = multiprocessing.Value('d', 0.0)

# Stop signal
stop_event = multiprocessing.Event()


def generate_cpu_load():
    while not stop_event.is_set():

        target = target_cpu.value
        cycle_time = 1.0

        busy_time = cycle_time * target / 100
        sleep_time = cycle_time - busy_time

        start = time.perf_counter()

        # Generate CPU load
        while time.perf_counter() - start < busy_time:
            if stop_event.is_set():
                return
            _ = 12345 * 67890

        if sleep_time > 0:
            time.sleep(sleep_time)


def main():
    print(f"Available CPU cores: {CPU_CORES}")

    workers = []

    # Start one worker per CPU core
    for _ in range(CPU_CORES):
        process = multiprocessing.Process(
            target=generate_cpu_load
        )
        process.start()
        workers.append(process)

    try:
        # Increase CPU utilization
        for cpu in range(10, 71, 10):
            target_cpu.value = cpu
            print(f"Increasing CPU load: {cpu}%")
            time.sleep(30)

        # Decrease CPU utilization
        for cpu in range(60, -1, -10):
            target_cpu.value = cpu
            print(f"Decreasing CPU load: {cpu}%")
            time.sleep(30)

        print("CPU load demonstration completed.")

    except KeyboardInterrupt:
        print("\nStopping CPU load...")

    finally:
        stop_event.set()

        for process in workers:
            process.join(timeout=2)
            if process.is_alive():
                process.terminate()

        print("All CPU workers stopped.")


if __name__ == "__main__":
    main()
