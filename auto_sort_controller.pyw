import customtkinter as ctk
import os
import json
import subprocess
from tkinter import filedialog, BooleanVar

CONFIG_FILE = "sort_config.json"
LOG_FILE = "sort_log.txt"

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class HoloToggleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("330x130")
        self.overrideredirect(True)
        self.configure(bg="#2b2b2b")  # приглушенный фон
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-alpha", 0.8)  # лёгкая мутность

        self.is_dragging = False
        self.options_visible = False

        self.config_data = self.load_config()

        # Граница 3px за счёт отступов, цвет совпадает с фоном
        self.frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=12)
        self.frame.pack(expand=True, fill="both", padx=3, pady=3)

        # ВЕРХНЯЯ СТРОКА: ⚙ и название
        self.top_row = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.top_row.pack(fill="x", pady=(5, 0))

        self.gear_btn = ctk.CTkButton(
            self.top_row, width=30, height=30, text="⚙", font=("Segoe UI", 18),
            command=self.toggle_options, fg_color="transparent", hover_color="#1e3a8a")
        self.gear_btn.pack(side="left", padx=(0, 5))

        self.title_label = ctk.CTkLabel(
            self.top_row, text="Auto-Sort", text_color="#67e8f9",
            font=("Consolas", 18))
        self.title_label.pack(side="left")

        # ON/OFF переключатель
        self.status_var = BooleanVar(value=self.get_sort_status())
        self.toggle = ctk.CTkSwitch(
            self.frame, text="ON / OFF", variable=self.status_var,
            command=self.toggle_sort, switch_height=28, switch_width=58,
            fg_color="#0ea5e9", progress_color="#10b981",
            button_color="#1e3a8a", font=("Consolas", 14))
        self.toggle.pack(pady=(10, 0))

        # Кнопки, появляющиеся при ⚙
        self.options_frame = ctk.CTkFrame(self.frame, fg_color="transparent")

        self.select_btn = ctk.CTkButton(self.options_frame, text="📂 Folder", command=self.select_folder, width=100)
        self.select_btn.pack(side="left", padx=5)

        self.types_btn = ctk.CTkButton(self.options_frame, text="✏️ Types", command=self.edit_types, width=100)
        self.types_btn.pack(side="left", padx=5)

        self.log_btn = ctk.CTkButton(self.options_frame, text="📃 Log", command=self.open_log, width=80)
        self.log_btn.pack(side="left", padx=5)

        # Exit-кнопка
        self.exit_btn = ctk.CTkButton(self.frame, text="Exit", command=self.destroy, fg_color="#be123c",
                                      hover_color="#ef4444", font=("Consolas", 14), width=80)
        self.exit_btn.pack(pady=(10, 0))

        # Драг в любой области
        for widget in (self, self.frame):
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)
            widget.bind("<ButtonRelease-1>", self.stop_move)

    def toggle_sort(self):
        enabled = self.status_var.get()
        self.save_sort_status(enabled)
        print("✅ Enabled" if enabled else "❌ Disabled")

    def toggle_options(self):
        if not self.options_visible:
            self.geometry("330x210")
            self.options_frame.pack(pady=5)
        else:
            self.options_frame.pack_forget()
            self.geometry("330x130")
        self.options_visible = not self.options_visible

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return {}

    def get_sort_status(self):
        return self.config_data.get("enabled", True)

    def save_sort_status(self, status):
        self.config_data["enabled"] = status
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config_data, f, indent=2)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.config_data["folder"] = folder
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config_data, f, indent=2)

    def open_log(self):
        if os.path.exists(LOG_FILE):
            try:
                os.startfile(LOG_FILE)
            except:
                subprocess.Popen(["xdg-open", LOG_FILE])
        else:
            print("Log not found.")

    def edit_types(self):
        import tkinter.simpledialog as sd
        types = self.config_data.get("types", {})
        cat = sd.askstring("Add category", "Enter category:")
        if cat:
            ext = sd.askstring("Extension", "Enter extension with dot (e.g. .png):")
            if ext:
                types.setdefault(cat, []).append(ext)
                self.config_data["types"] = types
                with open(CONFIG_FILE, "w") as f:
                    json.dump(self.config_data, f, indent=2)

    def start_move(self, event):
        self.is_dragging = True
        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        if self.is_dragging:
            x = self.winfo_pointerx() - self.offset_x
            y = self.winfo_pointery() - self.offset_y
            self.geometry(f"+{x}+{y}")

    def stop_move(self, event):
        self.is_dragging = False

if __name__ == "__main__":
    app = HoloToggleApp()
    app.mainloop()
