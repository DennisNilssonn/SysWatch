import time
import psutil
import threading
from utils import clear_screen


def display_usage(cpu_usage, memory_usage, bars=50):
    cpu_bar = "█" * int((cpu_usage / 100.0) * bars) + "-" * (
        bars - int((cpu_usage / 100.0) * bars)
    )
    memory_bar = "█" * int((memory_usage / 100.0) * bars) + "-" * (
        bars - int((memory_usage / 100.0) * bars)
    )
    clear_screen()
    print(f"CPU usage: |{cpu_bar}| {cpu_usage:.2f}%")
    print(f"Memory usage: |{memory_bar}| {memory_usage:.2f}%")
    print("press enter to go back to the menu")


def monitor_system():
    def wait_for_enter():
        input()

    enter_thread = threading.Thread(target=wait_for_enter)
    enter_thread.daemon = True
    enter_thread.start()

    while enter_thread.is_alive():
        display_usage(psutil.cpu_percent(), psutil.virtual_memory().percent)
        time.sleep(0.5)
