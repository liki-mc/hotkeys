import tkinter as tk

from typing import Callable, Any, Optional

class Add(tk.Toplevel):
    def __init__(self, *args, callback: Callable[[str, str, Optional[set[str]]], Any], **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Add")
        self.geometry("200x300")
        self.callback = callback

        self.title_var = tk.StringVar()
        self.text_var = tk.StringVar()
        self.tags_var = tk.StringVar()

        tk.Label(self, text = "Title:", anchor = tk.W).pack(anchor = tk.W)
        self.title_entry = tk.Entry(self, textvariable = self.title_var)
        self.title_entry.pack(fill = tk.X, padx = 5, pady = 5)

        tk.Label(self, text = "Text:").pack(anchor = tk.W)
        self.text_entry = tk.Entry(self, textvariable = self.text_var)
        self.text_entry.pack(fill = tk.X, padx = 5, pady = 5)

        tk.Label(self, text = "Tags:").pack(anchor = tk.W)
        self.tags_entry = tk.Entry(self, textvariable = self.tags_var)
        self.tags_entry.pack(fill = tk.X, padx = 5, pady = 5)

        self.add_button = tk.Button(self, text = "Add", command = self.add)
        self.add_button.pack(pady = 10)

        self.title_entry.focus_set()

    def add(self):
        title = self.title_var.get()
        text = self.text_var.get()
        tags = set(self.tags_var.get().split())
        self.callback(title, text, tags)
        self.destroy()

def test_add():
    root = tk.Tk()
    root.title("Add Test")
    root.geometry("400x400")

    def callback(title: str, text: str, tags: Optional[set[str]]):
        print(title, text, tags)

    Add(root, callback = callback)

    root.mainloop()


if __name__ == "__main__":
    test_add()