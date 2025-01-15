from __future__ import annotations

import keyboard
import pickle
import tkinter as tk

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
        self.geometry("500x500")
        self.app = app
        
        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        self.add_button = tk.Button(self, text = "Save", command = lambda *_: self.save() or self.withdraw())
        self.add_button.pack(pady = 10)
        self.filename = filename
        try:
            if filename:
                with open(filename, "rb") as file:
                    self.config = pickle.load(file)
            
            else:
                self.config = Config()

        except FileNotFoundError:
            self.config = Config()

        self.recording = False
        self.record_button = tk.Button(self, text = "Start Recording", command = self.start_recording)
        self.record_button.pack(pady = 10)

        self.first_key_hook : Optional[function] = None

        self.apply_settings()
    
    def apply_settings(self):
        # Set up the hotkey (e.g., Ctrl + Y)
        self.hotkey_handler = keyboard.add_hotkey(self.config.hotkey, self.app.toggle_window)
    
    def save(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.config, file)
        

    def start_recording(self):
        self.recording = True
        self.record_button.config(text = "Stop Recording", command = self.stop_recording)
        keyboard.start_recording()
        self.first_key_hook = keyboard.hook(self.record_first_key)

    def stop_recording(self, event = None):
        if self.recording:
            self.recording = False
            recorded = keyboard.stop_recording()
            self.record_button.config(text = "Start Recording", command = self.start_recording)
            keyboard.unhook_all()
            self.set_hotkey(recorded)
            print(recorded)
            print(set((key.name, keyboard.is_modifier(key.name)) for key in recorded))
    
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
        print("new hotkey:", hotkey)
        self.save()
        self.apply_settings()

    def record_first_key(self, event: keyboard.KeyboardEvent):
        if self.first_key_hook:
            keyboard.unhook(self.first_key_hook)
            self.first_key_hook = None
        keyboard.on_release_key(event.name, self.stop_recording)
    
    def show(self):
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