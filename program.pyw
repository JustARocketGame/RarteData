import requests
from tkinter import *
import time
import threading
import os
import subprocess

root = Tk()
root = root
root.title("Rarte")
root.resizable(False, False)

# Задаём размеры окна
window_width = 400
window_height = 200

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Вычисляем координаты для центрирования
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)

# Устанавливаем геометрию окна
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
