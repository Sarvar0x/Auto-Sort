import os
import sys
import winshell
from win32com.client import Dispatch

# Путь к скрипту auto_sort_controller.pyw
script_path = os.path.abspath("auto_sort_controller.pyw")

# Папка автозагрузки
startup = winshell.startup()

# Имя ярлыка
shortcut_path = os.path.join(startup, "AutoSort Controller.lnk")

# Создание ярлыка
shell = Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = sys.executable  # путь к pythonw.exe
shortcut.Arguments = f'"{script_path}"'
shortcut.WorkingDirectory = os.path.dirname(script_path)
shortcut.IconLocation = sys.executable
shortcut.save()

print("✅ Controller GUI added to Windows startup.")
