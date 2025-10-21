import time
import psutil
import threading
import json
import os
from datetime import datetime
from utils import clear_screen
from ui import divider


def load_alarms():
    # Läser in sparade alarm från fil
    if os.path.exists("alarms.json"):
        try:
            with open("alarms.json", "r") as f:
                content = f.read().strip()
                if not content:
                    # Tom fil, skapa tom struktur
                    return {"cpu": [], "memory": [], "disk": []}
                return json.loads(content)
        except (json.JSONDecodeError, ValueError):
            # Filen är trasig, skapa ny
            print("Korrupt alarm-fil upptäckt. Återställer till standard...")
            return {"cpu": [], "memory": [], "disk": []}
    else:
        return {"cpu": [], "memory": [], "disk": []}


def save_alarms(alarms_data):
    # Skriver alarm till fil
    with open("alarms.json", "w") as f:
        json.dump(alarms_data, f, indent=2)


def reset_triggered_alarms():
    # Nollställer alla utlösta alarm
    alarms_data = load_alarms()
    for alarm_type in alarms_data:
        for alarm in alarms_data[alarm_type]:
            alarm["triggered"] = None
    save_alarms(alarms_data)


def check_alarms(cpu_usage, memory_usage, disk_usage, alarms_data):
    # Kollar om några alarm ska gå av
    warnings = []
    alarms_updated = False
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Kolla CPU alarm
    for alarm in alarms_data["cpu"]:
        if cpu_usage >= alarm["value"] and alarm["triggered"] is None:
            alarm["triggered"] = current_time
            warnings.append(
                f"***VARNING, LARM AKTIVERAT, CPU ANVÄNDNING ÖVERSTIGER {alarm['value']}%***"
            )
            alarms_updated = True

    # Kolla minnes alarm
    for alarm in alarms_data["memory"]:
        if memory_usage >= alarm["value"] and alarm["triggered"] is None:
            alarm["triggered"] = current_time
            warnings.append(
                f"***VARNING, LARM AKTIVERAT, MINNESANVÄNDNING ÖVERSTIGER {alarm['value']}%***"
            )
            alarms_updated = True

    # Kolla disk alarm
    for alarm in alarms_data["disk"]:
        if disk_usage >= alarm["value"] and alarm["triggered"] is None:
            alarm["triggered"] = current_time
            warnings.append(
                f"***VARNING, LARM AKTIVERAT, DISKANVÄNDNING ÖVERSTIGER {alarm['value']}%***"
            )
            alarms_updated = True

    # Spara om något alarm gick av
    if alarms_updated:
        save_alarms(alarms_data)

    return warnings


def display_usage(cpu_usage, memory_usage, disk_usage, alarms_data, bars=50):
    cpu_bar = "█" * int((cpu_usage / 100.0) * bars) + "░" * (
        bars - int((cpu_usage / 100.0) * bars)
    )
    memory_bar = "█" * int((memory_usage / 100.0) * bars) + "░" * (
        bars - int((memory_usage / 100.0) * bars)
    )
    disk_bar = "█" * int((disk_usage / 100.0) * bars) + "░" * (
        bars - int((disk_usage / 100.0) * bars)
    )
    clear_screen()
    print("=" * 80)
    print(f"CPU usage:    |{cpu_bar}| {cpu_usage:.2f}%\n")
    print(f"Memory usage: |{memory_bar}| {memory_usage:.2f}%\n")
    print(f"Disk usage:   |{disk_bar}| {disk_usage:.2f}%")
    print("=" * 80)

    # Visa alla alarm
    print("\nAKTIVA ALARM:")
    # Hämta aktiva alarm
    active_alarms = []
    for alarm_type, alarms in alarms_data.items():
        for alarm in alarms:
            if alarm["triggered"] is None:
                active_alarms.append(
                    f"  * {alarm_type.upper()}: {alarm['value']}% - Status: Aktiv"
                )

    if active_alarms:
        for alarm in active_alarms:
            print(alarm)
    else:
        print("  (Inga aktiva alarm)")

    print("\nUTLÖSTA ALARM:")

    # Hämta utlösta alarm
    triggered_alarms = []
    for alarm_type, alarms in alarms_data.items():
        for alarm in alarms:
            if alarm["triggered"] is not None:
                triggered_alarms.append(
                    f"  * {alarm_type.upper()}: {alarm['value']}% - Utlöst: {alarm['triggered']}"
                )

    if triggered_alarms:
        for alarm in triggered_alarms:
            print(alarm)
    else:
        print("  (Inga utlösta alarm)")

    print("-" * 80)
    print("press enter to go back to the menu")


def monitor_system():
    def wait_for_enter():
        input()

    enter_thread = threading.Thread(target=wait_for_enter)
    enter_thread.daemon = True
    enter_thread.start()

    # Ladda sparade alarm
    alarms_data = load_alarms()

    # Håll koll på vilka varningar som visats
    last_warnings = set()

    while enter_thread.is_alive():
        # Läs systemdata
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent

        # Uppdatera skärmen
        display_usage(cpu_usage, memory_usage, disk_usage, alarms_data)

        # Kolla om något alarm ska gå av
        current_warnings = check_alarms(
            cpu_usage, memory_usage, disk_usage, alarms_data
        )

        # Visa nya varningar
        for warning in current_warnings:
            if warning not in last_warnings:
                print(f"\n{warning}")

        last_warnings = set(current_warnings)

        time.sleep(0.5)
