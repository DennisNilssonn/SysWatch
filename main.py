from ui import main_menu
from monitor import monitor_system
from alarm import set_alarm


def main():
    while True:
        main_menu()
        choice = input("Välj ett alternativ: ").lower().strip()
        if choice == "1":
            monitor_system()
        elif choice == "2":
            set_alarm()
        elif choice == "q":
            print("Avslutar programmet...")
            break
        else:
            input("Ogiltigt val. Tryck på Enter för att försöka igen...")


if __name__ == "__main__":
    main()
