from __future__ import annotations

import tkinter as tk
from tkinter import scrolledtext as tkst

from typing import Callable, Any, Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from .scrollable_frame import Item

class Modify(tk.Toplevel):
    add = "Add"
    edit = "Edit"
    modify = "Modify"
    def __init__(self, *args, callback: Callable[[str, str, Optional[set[str]]], Any], window_title: Literal["Add", "Edit", "Modify"] = "Modify", item: Item = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(window_title)
        self.geometry("500x500")
        self.callback = callback

        self.title_var = tk.StringVar(value = item.title if item else "")
        self.tags_var = tk.StringVar(value = " ".join(item.tags) if item else "")

        tk.Label(self, text = "Title:", anchor = tk.W).pack(anchor = tk.W)
        self.title_entry = tk.Entry(self, textvariable = self.title_var)
        self.title_entry.pack(fill = tk.X, padx = 5, pady = 5)

        tk.Label(self, text = "Text:").pack(anchor = tk.W)
        self.text_entry = tkst.ScrolledText(self, wrap = tk.WORD, width = 40, height = 6)
        self.text_entry.insert(tk.INSERT, item.text if item else "")
        self.text_entry.pack(fill = tk.BOTH, padx = 5, pady = 5)
        self.text_entry.bind("<Tab>", self.focus_next_widget)

        tk.Label(self, text = "Tags:").pack(anchor = tk.W)
        self.tags_entry = tk.Entry(self, textvariable = self.tags_var)
        self.tags_entry.pack(fill = tk.X, padx = 5, pady = 5)

        tk.Label(self, text = "Priority:").pack(anchor = tk.W)
        self.priority_var = tk.StringVar(value = item.priority if item else 10)

        # Validation function to ensure only integers are entered
        vcmd = (self.register(self.validate_int), '%P')
        self.priority_entry = tk.Entry(self, textvariable = self.priority_var, validate = 'key', validatecommand = vcmd)
        self.priority_entry.pack(fill = tk.X, padx = 5, pady = 5)

        self.add_button = tk.Button(self, text = "Save", command = self.apply)
        self.add_button.pack(pady = 10)

        self.title_entry.focus_set()
    
    def focus_next_widget(self, event: tk.Event) -> str:
        event.widget.tk_focusNext().focus()
        return "break"

    def validate_int(self, value_if_allowed: str) -> bool:
        if value_if_allowed == "" or value_if_allowed.isdigit():
            return True
        else:
            return False

    def apply(self):
        title = self.title_var.get()
        text = self.text_entry.get("1.0", tk.END).strip()
        tags = set(self.tags_var.get().split())
        priority = int(self.priority_var.get())
        self.callback(title, text, tags, priority)
        self.destroy()

def test_add():
    root = tk.Tk()
    root.title("Modify Test")
    root.geometry("400x400")

    def callback(title: str, text: str, tags: Optional[set[str]]):
        print(title, text, tags)

    Modify(root, callback = callback)

    root.mainloop()


if __name__ == "__main__":
    test_add()