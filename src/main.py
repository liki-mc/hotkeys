import tkinter as tk
import keyboard

from .scrollable_frame import ListBox
from .modify import Modify

class App:
    def __init__(self, filename: str = "data/items.pkl"):
        self.root = tk.Tk()
        self.root.title("Hotkeys")
        self.root.geometry("900x600")
        self.root.after(50, self.check)

        # Bind the close event to hide the window
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        
        self.listbox = ListBox(self.root, filename = filename)

        # Entry widget for filtering
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.root, textvariable = self.search_var)
        self.search_entry.pack(pady = 10, padx = 10, fill = tk.X)
        self.listbox.pack(fill = tk.BOTH, expand = True)

        # Bind on enter
        self.search_entry.bind('<Return>', self.on_enter)

        self.search_var.trace_add("write", self.search)

        # Bind the Esc key to hide the window
        self.root.bind('<Escape>', lambda _: self.hide_window())

        # Initially hide the window
        self.root.withdraw()
    
    def __enter__(self):
        self.listbox.__enter__()
        return self

    def __exit__(self, *args):
        self.listbox.__exit__(*args)
    
    def search(self, *_):
        text = self.search_var.get()
        if text.startswith("edit"):
            self.listbox.filter(text[5:])
        
        elif text.startswith("remove"):
            self.listbox.filter(text[7:])
        
        else:
            self.listbox.filter(self.search_var.get())

    def show_window(self):
        self.root.deiconify()  # Show the window
        self.search_entry.focus_set()

    def hide_window(self):
        self.root.withdraw()  # Hide the window

    def run(self):
        # Set up the hotkey (e.g., Ctrl + G)
        keyboard.add_hotkey('ctrl+g', self.toggle_window)

        # Start the Tkinter main loop
        self.root.mainloop()
    
    def on_enter(self, event):
        text = self.search_entry.get()
        if text in ["quit", "exit"]:
            return self.exit()
        
        if text == "add":
            return self.add()
        
        if text.startswith("edit"):
            return self.edit()
        
        if text.startswith("remove"):
            return self.remove()
        
        text = self.listbox.get_top().text
        self.search_entry.delete(0, tk.END)
        self.hide_window()
        self.root.after(100, lambda: self.write(text))
    
    def write(self, text):
        lines = text.split("\n")
        for line in lines[:-1]:
            if line:
                keyboard.write(line)
                keyboard.press_and_release("shift+enter")
        
        if lines[-1]:
            keyboard.write(lines[-1])
    
    def add(self):
        def callback(title: str, text: str, tags: set[str]):
            self.listbox.create(title, text, tags)
        
        add = Modify(self.root, window_title = Modify.add, callback = callback)
        add.transient(self.root)
        add.grab_set()
        add.wait_window()
        self.search_entry.delete(0, tk.END)
    
    def edit(self):
        item = self.listbox.get_top()
        def callback(title: str, text: str, tags: set[str]):
            self.listbox.edit(item.title, title, text, tags)
        
        
        edit = Modify(self.root, callback = callback, window_title = Modify.edit, title = item.title, text = item.text, tags = item.tags)
        edit.transient(self.root)
        edit.grab_set()
        edit.wait_window()
        self.search_entry.delete(0, tk.END)
    
    def remove(self):
        item = self.listbox.get_top()
        self.listbox.remove(item.title)
        self.search_entry.delete(0, tk.END)
    
    def exit(self):
        self.listbox.save("data/items.pkl")
        self.root.quit()

    def toggle_window(self):
        if self.root.winfo_viewable():
            self.hide_window()
        else:
            self.show_window()
    
    def check(self):
        self.root.after(50, self.check)

if __name__ == "__main__":
    with App() as app:
        app.run()