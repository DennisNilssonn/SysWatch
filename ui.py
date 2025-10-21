from utils import clear_screen, center_text


def main_menu():
    # Rensar skärmen och visar huvudmenyn
    clear_screen()
    divider("=")
    print(center_text("SYSWATCH"))
    divider("=")
    print("1. Övervaka systemet")
    print("2. Skapa nytt alarm")
    print("3. Visa aktiva alarm")
    print("4. Ta bort alarm")
    print("q. Avsluta programmet")
    print("-" * 48)


def alarm_menu():
    # Visar alarmmenyn
    clear_screen()
    divider("=")
    print(center_text("ALARM MENY"))
    divider("=")
    print("1. Skapa alarm")
    print("2. Visa sparade alarm")
    print("3. Ta bort alarm")
    print("Enter. Tillbaka till huvudmeny")
    print("-" * 48)


def terminal_header(header_text):
    # Skapar en header med text
    clear_screen()
    divider("=")
    print(center_text(header_text.upper()))
    divider("=")


def divider(icon):
    # Skapar en linje med valfritt tecken
    print(icon * 48)
