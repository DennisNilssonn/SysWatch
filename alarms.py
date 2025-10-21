from utils import clear_screen, center_text
from ui import divider, terminal_header
import time
import json
import os
from datetime import datetime
from logger import syswatch_logger


class JsonFile:
    def __init__(self, filename="alarms.json"):
        self.filename = filename
        self.alarms = self.load_alarms()

    def load_alarms(self):
        # Läser in alarm från fil
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
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

    def save_alarms(self, alarms_data):
        # Skriver alarm till fil
        with open(self.filename, "w") as f:
            json.dump(alarms_data, f, indent=2)

    def get_next_id(self, alarm_type, alarms_data):
        # Ger nästa lediga ID
        if not alarms_data[alarm_type]:
            return 1
        return max(alarm["id"] for alarm in alarms_data[alarm_type]) + 1


def validate_range_input(alarm_type, min_value=0, max_value=100):
    # Kollar att användaren matar in ett giltigt nummer
    while True:
        alarm_input = input(
            f"Choose {alarm_type} alarm value({min_value}-{max_value}%): "
        )

        # Logga input direkt
        syswatch_logger.log_input(alarm_input)

        if not alarm_input.isdigit():
            print("Invalid value. Please enter a number.")
            continue

        input_value = int(alarm_input)

        if input_value < min_value or input_value > max_value:
            print("Invalid value. Please enter a number between 0-100.")
            continue

        break

    return input_value


def create_alarm():
    alarm_file = JsonFile()

    def save_alarm(alarm_type):
        clear_screen()
        terminal_header(f"Choose {alarm_type} value")
        input_value = validate_range_input(alarm_type, 0, 100)

        # Läs in sparade alarm
        alarms_data = alarm_file.load_alarms()

        # Kolla om alarmet redan finns
        existing_values = [alarm["value"] for alarm in alarms_data[alarm_type]]
        if input_value in existing_values:
            terminal_header(f"Alarm already exists!")
            print(f"A {alarm_type} alarm with value {input_value}% already exists.")
            print("Please choose a different value.")
            input("Press Enter to try again...")
            save_alarm(alarm_type)
            return

        # Skapa nytt alarm
        new_alarm = {
            "id": alarm_file.get_next_id(alarm_type, alarms_data),
            "value": input_value,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "triggered": None,
        }

        # Spara alarmet
        alarms_data[alarm_type].append(new_alarm)
        alarm_file.save_alarms(alarms_data)

        # Logga att alarmet skapades
        syswatch_logger.log_alarm_created(alarm_type, input_value)

        terminal_header(f"Saving {alarm_type} alarm at {input_value}%")
        time.sleep(1)
        return

    terminal_header("CREATE NEW ALARM")
    print("1. CPU")
    print("2. Memory")
    print("3. Disk")
    print("\nPress Enter to go back to main menu")
    print("-" * 48)
    choice = input("Choose an option: ").lower().strip()

    # Logga input direkt
    syswatch_logger.log_input(choice)

    if choice == "1":
        save_alarm("cpu")
    elif choice == "2":
        save_alarm("memory")
    elif choice == "3":
        save_alarm("disk")
    elif choice == "":
        return
    else:
        input("Invalid choice. Press Enter to try again...")
        create_alarm()


def list_alarms():
    alarm_file = JsonFile()
    alarms_data = alarm_file.load_alarms()
    terminal_header("Alarm list")
    for alarm_type, alarms in alarms_data.items():
        print(f"{alarm_type.upper()}:")
        for alarm in alarms:
            triggered_info = (
                f"| Triggered: {alarm['triggered']}" if alarm["triggered"] else ""
            )
            print(
                f"ID: {alarm['id']}| Value: {alarm['value']}%| Created: {alarm['created']}{triggered_info}"
            )
        print()
    input("Press Enter to go back to main menu")
    return


def delete_alarm():
    alarm_file = JsonFile()
    alarms_data = alarm_file.load_alarms()

    # Samla alla alarm för att visa i lista
    all_alarms = []
    for alarm_type, alarms in alarms_data.items():
        for alarm in alarms:
            all_alarms.append({"type": alarm_type, "alarm": alarm})

    if not all_alarms:
        terminal_header("Delete Alarm")
        print("Inga alarm att ta bort!")
        input("Tryck Enter för att gå tillbaka...")
        return

    while True:
        terminal_header("Delete Alarm")
        print("Välj alarm att ta bort:")
        print()

        # Visa alla alarm med nummer
        for i, item in enumerate(all_alarms, 1):
            alarm_type = item["type"].upper()
            value = item["alarm"]["value"]
            created = item["alarm"]["created"]
            print(f"{i}. {alarm_type}: {value}% (skapat: {created})")

        print()
        print("-" * 48)

        try:

            if len(all_alarms) == 1:
                choice = input(
                    "Välj nummer 1 eller tryck enter för att avbryta: "
                ).strip()
            else:
                choice = input(
                    f"Välj nummer 1 - {len(all_alarms)} eller tryck enter för att avbryta: "
                ).strip()

            # Logga input direkt
            syswatch_logger.log_input(choice)

            if choice == "":
                return

            choice_num = int(choice)
            if 1 <= choice_num <= len(all_alarms):
                # Fråga om bekräftelse
                selected = all_alarms[choice_num - 1]
                alarm_type = selected["type"]
                value = selected["alarm"]["value"]

                print()
                confirm_input = input(
                    f"Är du säker på att ta bort {alarm_type.upper()}: {value}%? (j/n): "
                )

                # Logga input direkt
                syswatch_logger.log_input(confirm_input)

                confirm = confirm_input.lower().strip()

                if confirm in ["j", "ja", "y", "yes"]:
                    # Ta bort alarmet
                    alarm_to_remove = selected["alarm"]
                    alarms_data[alarm_type].remove(alarm_to_remove)

                    # Spara ändringar
                    alarm_file.save_alarms(alarms_data)

                    # Logga att alarmet togs bort
                    syswatch_logger.log_alarm_deleted(
                        alarm_type, value, alarm_to_remove["id"]
                    )

                    clear_screen()
                    terminal_header(
                        f"Alarm {alarm_type.upper()}: {value}% har tagits bort!"
                    )
                    time.sleep(1)
                    return
                else:
                    terminal_header("Borttagning avbruten.")
                    time.sleep(1)
                    continue
            else:
                print("Ogiltigt val. Välj ett nummer från listan.")
                time.sleep(1)
                continue

        except ValueError:
            print("Ogiltig inmatning. Ange ett nummer.")
            time.sleep(1)
            continue
