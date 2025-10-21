import os
import shutil


def clear_screen():
    # Rensar terminalen
    os.system("cls" if os.name == "nt" else "clear")


def center_text(text, width=48):
    # Centrerar text inom en given bredd
    return text.center(width)
