import os
import shutil


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def center_text(text, width=48):
    return text.center(width)
