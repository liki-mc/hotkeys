import tkinter as tk
from tkinter import scrolledtext as tkst

from typing import Callable, Any, Optional, Literal

class Modify(tk.Toplevel):
    add = "Add"
    edit = "Edit"
    modify = "Modify"
    def __init__(self, *args, callback: Callable[[str, str, Optional[set[str]]], Any], window_title: Literal["Add", "Edit", "Modify"] = "Modify", title: str = "", text: str = "", tags: set[str] = set(), **kwargs):
        super().__init__(*args, **kwargs)
        self.title(window_title)
        self.geometry("500x500")
        self.callback = callback

        self.title_var = tk.StringVar(value = title)
        self.tags_var = tk.StringVar(value = " ".join(tags))

        tk.Label(self, text = "Title:", anchor = tk.W).pack(anchor = tk.W)
        self.title_entry = tk.Entry(self, textvariable = self.title_var)
        self.title_entry.pack(fill = tk.X, padx = 5, pady = 5)

        tk.Label(self, text = "Text:").pack(anchor = tk.W)
        self.text_entry = tkst.ScrolledText(self, wrap = tk.WORD, width = 40, height = 6)
        self.text_entry.insert(tk.INSERT, text)
        self.text_entry.pack(fill = tk.BOTH, padx = 5, pady = 5)
        self.text_entry.bind("<Tab>", self.focus_next_widget)

        tk.Label(self, text = "Tags:").pack(anchor = tk.W)
        self.tags_entry = tk.Entry(self, textvariable = self.tags_var)
        self.tags_entry.pack(fill = tk.X, padx = 5, pady = 5)

        self.add_button = tk.Button(self, text = "Add", command = self.apply)
        self.add_button.pack(pady = 10)

        self.title_entry.focus_set()
    
    def focus_next_widget(self, event: tk.Event) -> str:
        event.widget.tk_focusNext().focus()
        return "break"

    def apply(self):
        title = self.title_var.get()
        text = self.text_entry.get("1.0", tk.END)
        tags = set(self.tags_var.get().split())
        self.callback(title, text, tags)
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