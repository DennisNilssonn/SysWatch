import json
import os
from datetime import datetime
from utils import clear_screen
from ui import alarm_menu


class AlarmManager:
    def __init__(self, filename="alarms.json"):
        self.filename = filename

    def load_alarms(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {"cpu": [], "memory": []}
        return {"cpu": [], "memory": []}

    def save_alarms(self, alarms):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(alarms, f, ensure_ascii=False, indent=2)

    def alarm_exists(self, alarm_type, alarm_value):
        alarms = self.load_alarms()
        if alarm_type in alarms:
            for existing_alarm in alarms[alarm_type]:
                if existing_alarm["value"] == alarm_value:
                    return True
        return False

    def get_next_id(self, alarm_type):
        """Hämtar nästa ID för alarmtypen"""
        alarms = self.load_alarms()
        if alarm_type in alarms and alarms[alarm_type]:
            return max([alarm["id"] for alarm in alarms[alarm_type]]) + 1
        return 1

    def create_new_alarm(self, alarm_type):
        try:
            alarm_value = float(input("Ange alarm-värde (0-100%): "))
            if 0 <= alarm_value <= 100:
                if self.alarm_exists(alarm_type, alarm_value):
                    print(f"Det finns redan ett {alarm_type}-alarm vid {alarm_value}%!")
                    input("Tryck Enter för att försöka igen...")
                    return False

                alarms = self.load_alarms()

                new_alarm = {
                    "id": self.get_next_id(alarm_type),
                    "value": alarm_value,
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                if alarm_type not in alarms:
                    alarms[alarm_type] = []
                alarms[alarm_type].append(new_alarm)

                self.save_alarms(alarms)

                print(f"{alarm_type}-alarm satt vid {alarm_value}% och sparat!")
                input("Tryck Enter för att fortsätta...")
                return True
            else:
                print("Ogiltigt värde. Använd 0-100.")
                input("Tryck Enter för att försöka igen...")
                return False
        except ValueError:
            print("Ogiltigt värde. Använd endast siffror.")
            input("Tryck Enter för att försöka igen...")
            return False

    def get_alarms_by_type(self, alarm_type):
        alarms = self.load_alarms()
        return alarms.get(alarm_type, [])

    def get_all_alarms(self):
        return self.load_alarms()

    def list_alarms(self):
        alarms = self.load_alarms()

        if not alarms or (not alarms.get("cpu") and not alarms.get("memory")):
            print("Inga alarm sparade.")
            return

        for alarm_type in ["cpu", "memory"]:
            if alarm_type in alarms and alarms[alarm_type]:
                print(f"\n{alarm_type.upper()}-ALARM:")
                for alarm in alarms[alarm_type]:
                    print(
                        f"  ID: {alarm['id']} | Värde: {alarm['value']}% | Skapat: {alarm['created']}"
                    )

    def delete_alarm(self):
        """Tar bort ett alarm baserat på typ och ID"""
        alarm_type = input("Ange typ (cpu/memory): ").lower().strip()

        if alarm_type not in ["cpu", "memory"]:
            print("Ogiltig typ. Använd 'cpu' eller 'memory'.")
            return

        alarms = self.load_alarms()

        if alarm_type not in alarms or not alarms[alarm_type]:
            print(f"Inga {alarm_type}-alarm hittades.")
            return

        print(f"\nBefintliga {alarm_type}-alarm:")
        for alarm in alarms[alarm_type]:
            print(f"  ID: {alarm['id']} | Värde: {alarm['value']}%")

        try:
            alarm_id = int(input(f"\nAnge ID för {alarm_type}-alarm att ta bort: "))

            # Ta bort alarmet
            original_count = len(alarms[alarm_type])
            alarms[alarm_type] = [
                alarm for alarm in alarms[alarm_type] if alarm["id"] != alarm_id
            ]

            if len(alarms[alarm_type]) < original_count:
                self.save_alarms(alarms)
                print(f"{alarm_type}-alarm ID {alarm_id} borttaget!")
            else:
                print(f"Alarm ID {alarm_id} hittades inte.")

        except ValueError:
            print("Ogiltigt ID. Använd endast siffror.")


def set_alarm():
    alarm_manager = AlarmManager()

    while True:
        alarm_menu()
        choice = input("Välj ett alternativ: ").lower().strip()
        if choice == "1":
            if alarm_manager.create_new_alarm("cpu"):
                break
        elif choice == "2":
            if alarm_manager.create_new_alarm("memory"):
                break
        elif choice == "3":
            alarm_manager.list_alarms()
            input("Tryck på Enter för att fortsätta...")
        elif choice == "4":
            alarm_manager.delete_alarm()
            input("Tryck på Enter för att fortsätta...")
        elif choice == "":
            break
        else:
            input("Ogiltigt val. Tryck på Enter för att försöka igen...")
