from __future__ import annotations

import keyboard
import pickle
import tkinter as tk

from tkinter import font
from tkinter import messagebox


from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.main import App

@dataclass
class Config:
    hotkey: str = "ctrl+y"

class ConfigWindow(tk.Toplevel):
    def __init__(self, app: App, *args, filename: str = "data/config.pkl", **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Configuration")
        self.geometry("250x400")
        self.app = app
        
        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        self.filename = filename
        try:
            if filename:
                with open(filename, "rb") as file:
                    self.config = pickle.load(file)
            
            else:
                self.config = Config()

        except FileNotFoundError:
            self.config = Config()
        
        
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12) 


        self.recording = False
        self.first_key_hook : Optional[function] = None

        self.hotkey_label = tk.Label(self, text = "Hotkey")
        self.hotkey_label.pack(pady = 5)
        self.hotkey_frame = tk.Frame(self)
        self.hotkey_frame.pack(pady = 5)
        self.display_hotkey()
        self.add_button = tk.Button(self, text = "Save", command = lambda *_: self.save() or self.withdraw())
        self.add_button.pack(pady = 10)

        self.apply_settings()
    
    def display_hotkey(self):
        for widget in self.hotkey_frame.winfo_children():
            widget.destroy()

        for key in self.config.hotkey.split("+"):
            label = tk.Label(self.hotkey_frame, text = key, border = 2, relief = tk.RIDGE)
            label.pack(side = tk.LEFT, pady = 5, anchor = tk.CENTER)
        self.hotkey_button = tk.Button(self.hotkey_frame, text = "Record hotkey", command = self.start_recording)
        self.hotkey_button.pack(pady = 5, side = tk.RIGHT)

    
    def apply_settings(self):
        # Set up the hotkey (e.g., Ctrl + Y)
        self.hotkey_handler = keyboard.add_hotkey(self.config.hotkey, self.app.toggle_window)
    
    def save(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.config, file)
        

    def start_recording(self):
        self.recording = True
        self.hotkey_button.config(text = "Stop Recording", command = self.stop_recording)
        keyboard.start_recording()
        self.first_key_hook = keyboard.hook(self.record_first_key)

    def stop_recording(self, event = None):
        if self.recording:
            self.recording = False
            recorded = keyboard.stop_recording()
            self.hotkey_button.config(text = "Record hotkey", command = self.start_recording)
            keyboard.unhook_all()
            self.set_hotkey(recorded)
        
    def set_hotkey(self, recorded: list[keyboard.KeyboardEvent]):
        keys = set((key.name, keyboard.is_modifier(key.name)) for key in recorded)
        has_non_modifier = False
        hotkey = ""
        for key in keys:
            if key[1]:
                hotkey = key[0] + "+" + hotkey
            else:
                if has_non_modifier:
                    # only one non-modifier key allowed
                    messagebox.showerror("Error", "Only one non-modifier key allowed")
                    return
                hotkey += key[0]
                has_non_modifier = True
        
        self.config.hotkey = hotkey
        # print("new hotkey:", hotkey)
        self.save()
        self.apply_settings()
        self.display_hotkey()

    def record_first_key(self, event: keyboard.KeyboardEvent):
        if self.first_key_hook:
            keyboard.unhook(self.first_key_hook)
            self.first_key_hook = None
        keyboard.on_release_key(event.name, self.stop_recording)
    
    def show(self):
        self.geometry(f"+{self.app.root.winfo_x() + 50}+{self.app.root.winfo_y() + 50}")
        self.deiconify()
        self.lift()


def test_config():
    root = tk.Tk()
    root.title("Config Test")
    root.geometry("400x400")

    with ConfigWindow(root):

        root.mainloop()

if __name__ == "__main__":
    test_config()