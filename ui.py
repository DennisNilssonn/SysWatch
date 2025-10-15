from utils import clear_screen


def main_menu():
    clear_screen()
    print(f"{'*'*20}SYSWATCH{'*'*20}\n")
    print("1. Övervaka systemet")
    print("2. Skapa nytt alarm")
    print("q. Avsluta programmet")
    print("-" * 48)


def alarm_menu():
    clear_screen()
    print("=== SKAPA NYTT ALARM ===")
    print("1. Skapa CPU-alarm")
    print("2. Skapa minnes-alarm")
    print("3. Visa sparade alarm")
    print("4. Ta bort alarm")
    print("Enter. Tillbaka till huvudmeny")
    print("-" * 48)
