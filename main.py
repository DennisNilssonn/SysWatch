import time
import psutil
import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def display_usage(cpu_usage, memory_usage, bars=50):
    cpu_bar = "█" * int((cpu_usage / 100.0) * bars) + "-" * (
        bars - int((cpu_usage / 100.0) * bars)
    )
    memory_bar = "█" * int((memory_usage / 100.0) * bars) + "-" * (
        bars - int((memory_usage / 100.0) * bars)
    )

    # Rensa skärmen och visa uppdaterad information
    clear_screen()
    print(f"CPU usage: |{cpu_bar}| {cpu_usage:.2f}%")
    print(f"Memory usage: |{memory_bar}| {memory_usage:.2f}%")


while True:
    display_usage(psutil.cpu_percent(), psutil.virtual_memory().percent)
    time.sleep(0.5)
