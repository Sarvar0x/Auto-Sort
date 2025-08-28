import os
import winshell
from win32com.client import Dispatch

# Путь к pythonw.exe (без окна)
pythonw_path = r"C:\Users\LENOVO\AppData\Local\Programs\Python\Python311\pythonw.exe"

# Путь к твоему скрипту
controller_path = r"E:\sorter\auto_sort_controller.pyw"

# Путь к папке автозагрузки
startup_folder = winshell.startup()

# Путь к ярлыку
shortcut_path = os.path.join(startup_folder, "AutoSort Controller.lnk")

# Создание ярлыка
shell = Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = pythonw_path
shortcut.Arguments = f'"{controller_path}"'
shortcut.WorkingDirectory = os.path.dirname(controller_path)
shortcut.IconLocation = pythonw_path
shortcut.save()

print("✅ Clean controller shortcut added to startup (no black window).")
