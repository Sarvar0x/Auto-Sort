import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
from datetime import datetime

CONFIG_FILE = "sort_config.json"
LOG_FILE = "sort_log.txt"

# --------------------- Загрузка конфигурации --------------------- #
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "enabled": True,
            "folder": os.path.join(os.path.expanduser("~"), "Desktop"),
            "types": {
                "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
                "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
                "Videos": [".mp4", ".avi", ".mkv", ".mov"],
                "Music": [".mp3", ".wav", ".flac"],
                "Archives": [".zip", ".rar", ".7z"],
                "Programs": [".exe", ".msi", ".bat", ".py"],
                "Codes": [".html", ".scss", ".php",".js",],
                "Others": []
                
            }
        }

# --------------------- Сохранение лога --------------------- #
def log_action(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

# --------------------- Сортировка файла --------------------- #
def sort_file(file_path):
    cfg = load_config()
    folder = cfg["folder"]
    types = cfg["types"]

    filename = os.path.basename(file_path)
    extension = os.path.splitext(filename)[1].lower()

    for category, extensions in types.items():
        if extension in extensions:
            target_folder = os.path.join(folder, category)
            os.makedirs(target_folder, exist_ok=True)
            target_path = os.path.join(target_folder, filename)
            try:
                shutil.move(file_path, target_path)
                log_action(f"Moved: {filename} -> {category}/")
            except Exception as e:
                log_action(f"Failed to move {filename}: {e}")
            return

    # Если расширение не найдено
    others_folder = os.path.join(folder, "Others")
    os.makedirs(others_folder, exist_ok=True)
    try:
        shutil.move(file_path, os.path.join(others_folder, filename))
        log_action(f"Moved: {filename} -> Others/")
    except Exception as e:
        log_action(f"Failed to move {filename}: {e}")

# --------------------- Обработчик событий --------------------- #
class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            try:
                cfg = load_config()
                if cfg.get("enabled", True):
                    sort_file(event.src_path)
            except Exception as e:
                log_action(f"Error handling file: {e}")

# --------------------- Основной запуск --------------------- #
if __name__ == '__main__':
    cfg = load_config()
    watch_folder = cfg.get("folder", os.path.join(os.path.expanduser("~"), "Desktop"))

    observer = Observer()
    observer.schedule(Watcher(), path=watch_folder, recursive=False)
    observer.start()

    print(f"Watching folder: {watch_folder}")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
