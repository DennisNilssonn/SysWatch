from ui import main_menu
from monitor import monitor_system
from alarms import create_alarm, list_alarms, delete_alarm


def main():
    # Huvudloop för programmet
    while True:
        main_menu()
        choice = input("Välj ett alternativ: ").lower().strip()

        if choice == "1":
            monitor_system()
        elif choice == "2":
            create_alarm()
        elif choice == "3":
            list_alarms()
        elif choice == "4":
            delete_alarm()
        elif choice == "q":
            print("Avslutar programmet...")
            break
        else:
            input("Ogiltigt val. Tryck på Enter för att försöka igen...")


if __name__ == "__main__":
    main()
