from utils import clear_screen


def main_menu():
    clear_screen()
    print(f"{'*'*20}SYSWATCH{'*'*20}\n")
    print("1. Övervaka systemet")
    print("2. Skapa nytt alarm")
    print("q. Avsluta programmet")
    print("-" * 48)
