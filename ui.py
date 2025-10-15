from utils import clear_screen, center_text


def main_menu():
    clear_screen()
    divider("=")
    print(center_text("SYSWATCH"))
    divider("=")
    print("1. Övervaka systemet")
    print("2. Skapa nytt alarm")
    print("q. Avsluta programmet")
    print("-" * 48)


def alarm_menu():
    clear_screen()
    divider("=")
    print(center_text("ALARM MENY"))
    divider("=")
    print("1. Skapa alarm")
    print("2. Visa sparade alarm")
    print("3. Ta bort alarm")
    print("Enter. Tillbaka till huvudmeny")
    print("-" * 48)


def divider(icon):
    print(icon * 48)
