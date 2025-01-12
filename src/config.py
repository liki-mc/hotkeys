import keyboard
import pickle
import tkinter as tk


from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    hotkey: str = "ctrl+y"

class ConfigWindow(tk.Toplevel):
    def __init__(self, *args, filename: str = "data/config.pkl", **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Configuration")
        self.geometry("500x500")

        self.add_button = tk.Button(self, text = "Save", command = self.save)
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
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.save()
    
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
            print(recorded)
            print(set((key.name, keyboard.is_modifier(key.name)) for key in recorded))

    def record_first_key(self, event: keyboard.KeyboardEvent):
        if self.first_key_hook:
            keyboard.unhook(self.first_key_hook)
            self.first_key_hook = None
        keyboard.on_release_key(event.name, self.stop_recording)


def test_config():
    root = tk.Tk()
    root.title("Config Test")
    root.geometry("400x400")

    with ConfigWindow(root):

        root.mainloop()

if __name__ == "__main__":
    test_config()