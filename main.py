from ui import main_menu
from monitor import monitor_system
from alarms import create_alarm, list_alarms, delete_alarm
from logger import syswatch_logger


def main():
    # Logga programstart
    syswatch_logger.log_program_start()

    # Huvudloop för programmet
    while True:
        main_menu()
        choice = input("Välj ett alternativ: ").lower().strip()

        # Logga input direkt
        syswatch_logger.log_input(choice)

        # Logga användarens val
        syswatch_logger.log_user_action("menyval", f"alternativ: {choice}")

        if choice == "1":
            syswatch_logger.log_menu_navigation("Systemövervakning")
            monitor_system()
        elif choice == "2":
            syswatch_logger.log_menu_navigation("Skapa alarm")
            create_alarm()
        elif choice == "3":
            syswatch_logger.log_menu_navigation("Visa alarm")
            list_alarms()
        elif choice == "4":
            syswatch_logger.log_menu_navigation("Ta bort alarm")
            delete_alarm()
        elif choice == "q":
            print("Avslutar programmet...")
            syswatch_logger.log_user_action(
                "programavslut", "användaren valde att avsluta"
            )
            syswatch_logger.log_program_exit()
            break
        else:
            syswatch_logger.log_user_action("ogiltigt val", f"inmatning: '{choice}'")
            input("Ogiltigt val. Tryck på Enter för att försöka igen...")


if __name__ == "__main__":
    main()
