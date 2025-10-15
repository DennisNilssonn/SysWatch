import json
import os
from datetime import datetime
from ui import alarm_menu, divider
from utils import clear_screen, center_text


class AlarmManager:
    def __init__(self, filename="alarms.json"):
        self.filename = filename
        self.alarms = self.load_alarms_from_file()

    def load_alarms_from_file(self):
        if not os.path.exists(self.filename):
            return {"cpu": [], "memory": []}

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"cpu": [], "memory": []}

    def save_alarms_to_file(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.alarms, f, ensure_ascii=False, indent=2)

    def alarm_exists(self, alarm_type, alarm_value):
        alarms = self.alarms.get(alarm_type, [])
        return any(alarm["value"] == alarm_value for alarm in alarms)

    def get_next_id(self, alarm_type):
        alarms = self.alarms.get(alarm_type, [])
        return max([alarm["id"] for alarm in alarms], default=0) + 1

    def _display_header(self, title):
        clear_screen()
        divider("=")
        print(center_text(title))
        divider("=")

    def _display_message(self, title, message):
        self._display_header(title)
        print(message)
        input("\nTryck Enter för att fortsätta...")

    def _get_valid_input(self, prompt, validator, error_msg="Ogiltigt värde"):
        while True:
            value = input(prompt).strip()
            result = validator(value)
            if result is not None:
                return result
            print(error_msg)
            input("Tryck Enter för att försöka igen...")

    def show_alarm_type_menu(self):

        def validate_choice(choice):
            if choice == "1":
                return "cpu"
            elif choice == "2":
                return "memory"
            elif choice.lower() == "q":
                return "q"
            return None

        self._display_header("VÄLJ ALARMTYP")
        print("1. CPU-alarm")
        print("2. Minne-alarm\n")
        print("q. Tillbaka")
        divider("-")

        choice = self._get_valid_input(
            "Välj alternativ (1-2): ",
            validate_choice,
            "Ogiltigt val! Välj 1, 2 eller 'q' för att gå tillbaka.",
        )

        return None if choice == "q" else choice

    def get_alarm_value(self, alarm_type):

        def validate_value(value_str):
            try:
                value = float(value_str.replace("%", ""))
                return value if 0 <= value <= 100 else None
            except ValueError:
                return None

        self._display_header(f"VÄLJ VÄRDE FÖR {alarm_type.upper()}-ALARM")
        print(f"Hur hög ska {alarm_type}-användningen vara innan")
        print("alarmet utlöses?")
        print("Välj mellan 0% - 100%")
        divider("-")

        return self._get_valid_input(
            "Ange värde (0-100%): ",
            validate_value,
            "Ogiltigt värde! Använd endast siffror mellan 0-100%.",
        )

    def create_new_alarm(self):
        alarm_type = self.show_alarm_type_menu()
        if alarm_type is None:
            return False

        alarm_value = self.get_alarm_value(alarm_type)

        if self.alarm_exists(alarm_type, alarm_value):
            self._display_message(
                "ALARM REDAN SPARAT",
                f"Det finns redan ett {alarm_type}-alarm vid {alarm_value}%!",
            )
            return False

        # Skapa och spara nytt alarm
        new_alarm = self._create_alarm_object(alarm_type, alarm_value)
        self._add_alarm_to_list(alarm_type, new_alarm)
        self.save_alarms_to_file()

        # Visa bekräftelse
        self._display_message(
            "ALARM SPARAT!",
            f"{alarm_type.upper()}-alarm skapat vid {alarm_value}%\n"
            f"Skapat: {new_alarm['created']}\n"
            f"ID: {new_alarm['id']}",
        )
        return True

    def _create_alarm_object(self, alarm_type, alarm_value):
        return {
            "id": self.get_next_id(alarm_type),
            "value": alarm_value,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def _add_alarm_to_list(self, alarm_type, alarm):
        if alarm_type not in self.alarms:
            self.alarms[alarm_type] = []
        self.alarms[alarm_type].append(alarm)

    def list_alarms(self):
        self._display_header("SPARADE ALARM")

        if not self._has_alarms():
            print("Inga alarm sparade ännu.")
            return

        for alarm_type in ["cpu", "memory"]:
            self._display_alarms_for_type(alarm_type)

    def _has_alarms(self):
        return self.alarms and (self.alarms.get("cpu") or self.alarms.get("memory"))

    def _display_alarms_for_type(self, alarm_type):
        alarms = self.alarms.get(alarm_type, [])
        if not alarms:
            return

        type_name = "CPU" if alarm_type == "cpu" else "MINNE"
        print(f"{type_name}-ALARM:")

        for alarm in alarms:
            print(
                f"ID: {alarm['id']} | Värde: {alarm['value']}% | Skapat: {alarm['created']}"
            )

    def delete_alarm(self):
        self._display_header("TA BORT ALARM")

        alarm_type = self._get_alarm_type_input()
        if not alarm_type:
            return

        if not self._validate_alarm_type_has_alarms(alarm_type):
            return

        self._display_alarms_to_delete(alarm_type)
        alarm_id = self._get_alarm_id_to_delete()

        if self._delete_alarm_by_id(alarm_type, alarm_id):
            print(f"{alarm_type}-alarm ID {alarm_id} borttaget!")
            self.save_alarms_to_file()
        else:
            print(f"Alarm ID {alarm_id} hittades inte.")

    def _get_alarm_type_input(self):

        def validate_type(alarm_type):
            clean_type = alarm_type.lower().strip()
            return clean_type if clean_type in ["cpu", "memory"] else None

        return self._get_valid_input(
            "Ange typ (cpu/memory): ",
            validate_type,
            "Ogiltig typ. Använd 'cpu' eller 'memory'.",
        )

    def _validate_alarm_type_has_alarms(self, alarm_type):
        if alarm_type not in self.alarms or not self.alarms[alarm_type]:
            print(f"Inga {alarm_type}-alarm hittades.")
            return False
        return True

    def _display_alarms_to_delete(self, alarm_type):
        print(f"\nBefintliga {alarm_type}-alarm:")
        for alarm in self.alarms[alarm_type]:
            print(f"ID: {alarm['id']} | Värde: {alarm['value']}%")

    def _get_alarm_id_to_delete(self):

        def validate_id(alarm_id_str):
            try:
                return int(alarm_id_str)
            except ValueError:
                return None

        return self._get_valid_input(
            "\nAnge ID för alarm att ta bort: ",
            validate_id,
            "Ogiltigt ID. Använd endast siffror.",
        )

    def _delete_alarm_by_id(self, alarm_type, alarm_id):
        original_count = len(self.alarms[alarm_type])
        self.alarms[alarm_type] = [
            alarm for alarm in self.alarms[alarm_type] if alarm["id"] != alarm_id
        ]
        return len(self.alarms[alarm_type]) < original_count


def set_alarm():
    alarm_manager = AlarmManager()
    menu_actions = {
        "1": alarm_manager.create_new_alarm,
        "2": lambda: _show_alarms_and_wait(alarm_manager),
        "3": lambda: _delete_alarm_and_wait(alarm_manager),
    }

    while True:
        alarm_menu()
        choice = input("Välj ett alternativ: ").lower().strip()

        if choice == "":
            break
        elif choice in menu_actions:
            menu_actions[choice]()
        else:
            print("Ogiltigt val!")
            input("Tryck Enter för att försöka igen...")


def _show_alarms_and_wait(alarm_manager):
    clear_screen()
    alarm_manager.list_alarms()
    input("\nTryck på Enter för att fortsätta...")


def _delete_alarm_and_wait(alarm_manager):
    clear_screen()
    alarm_manager.delete_alarm()
    input("\nTryck på Enter för att fortsätta...")
