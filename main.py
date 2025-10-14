import time
import psutil
import os
import threading


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


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
    print("Startar övervakning...")

    def wait_for_enter():
        input()

    enter_thread = threading.Thread(target=wait_for_enter)
    enter_thread.daemon = True
    enter_thread.start()

    while enter_thread.is_alive():
        display_usage(psutil.cpu_percent(), psutil.virtual_memory().percent)
        time.sleep(0.5)

    print("Stoppar övervakning...")


def show_menu():
    clear_screen()
    print(f"{'*'*20}SYSWATCH{'*'*20}\n")
    print("1. Övervaka systemet")
    print("q. Avsluta programmet")
    print("-" * 48)


def main():
    while True:
        show_menu()
        choice = input("Välj ett alternativ: ").lower().strip()
        if choice == "1":
            monitor_system()
        elif choice == "q":
            print("Avslutar programmet...")
            break
        else:
            input("Ogiltigt val. Tryck på Enter för att försöka igen...")


main()
