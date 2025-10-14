from utils import clear_screen


def create_new_alarm(alarm_type):
    try:
        alarm_value = float(input("Ange alarm-värde (0-100%): "))
        if 0 <= alarm_value <= 100:
            print(f"{alarm_type}-alarm satt vid {alarm_value}%")
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


def alarm_menu():
    while True:
        clear_screen()
        print("=== SKAPA NYTT ALARM ===")
        print("1. Skapa CPU-alarm")
        print("2. Skapa minnes-alarm")
        print("Enter. Tillbaka till huvudmeny")
        print("-" * 48)
        choice = input("Välj ett alternativ: ").lower().strip()
        if choice == "1":
            if create_new_alarm("cpu"):
                break
        elif choice == "2":
            if create_new_alarm("memory"):
                break
        elif choice == "":
            break
        else:
            input("Ogiltigt val. Tryck på Enter för att försöka igen...")
