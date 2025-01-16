import tkinter as tk
import keyboard
import screeninfo

from .config import ConfigWindow
from .modify import Modify
from .scrollable_frame import ListBox

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
        self.search_entry.bind('<Control-BackSpace>', self.ctrl_backspace)
        self.search_var.trace_add("write", self.search)

        # Bind the Esc key to hide the window
        self.root.bind('<Escape>', lambda _: self.search_entry.delete(0, tk.END) or self.hide_window())

        # Initially hide the window
        self.root.withdraw()

        # load config
        self.config = ConfigWindow(self)
        self.config.withdraw()
    
    def __enter__(self):
        self.listbox.__enter__()
        return self

    def __exit__(self, *args):
        self.config.save()
        self.listbox.__exit__(*args)
    
    def ctrl_backspace(self, event: tk.Event):
        entry = event.widget
        if not isinstance(entry, tk.Entry):
            return
        cursor_pos = entry.index(tk.INSERT)
        text = entry.get()
        if cursor_pos == 0:
            return
        # Find the position of the previous word
        new_pos = text.rfind(' ', 0, cursor_pos)
        if new_pos == -1:
            new_pos = 0
        else:
            new_pos += 2
        entry.delete(new_pos, cursor_pos)
    
    def search(self, *_):
        text = self.search_var.get()
        if text.startswith("edit"):
            self.listbox.filter(text[5:])
        
        elif text.startswith("remove"):
            self.listbox.filter(text[7:])
        
        else:
            self.listbox.filter(self.search_var.get())

    def show_window(self):
        # Get the current mouse position
        mouse_x = self.root.winfo_pointerx()
        mouse_y = self.root.winfo_pointery()

        # Calculate the desired position of the window
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        x = mouse_x - window_width // 4
        y = mouse_y - window_height // 4

        # Position on the screen
        for monitor in screeninfo.get_monitors():
            if monitor.x <= mouse_x <= monitor.x + monitor.width:
                if x < monitor.x:
                    x = monitor.x
                elif x + window_width > monitor.x + monitor.width:
                    x = monitor.x + monitor.width - window_width
            
            if monitor.y <= mouse_y <= monitor.y + monitor.height:
                if y < monitor.y:
                    y = monitor.y
                elif y + window_height > monitor.y + monitor.height:
                    y = monitor.y + monitor.height - window_height

        # Set the position of the root window
        self.root.geometry(f"+{x}+{y}")
        self.root.deiconify()  # Show the window
        self.search_entry.focus_set()

    def hide_window(self):
        self.root.withdraw()  # Hide the window

    def run(self):
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

        if text == "config":
            self.config.show()
            return

        try:
            text = self.listbox.get_top().text
            self.search_entry.delete(0, tk.END)
            self.hide_window()
            self.root.after(10, lambda: self.write(text))
        
        except IndexError:
            self.search_entry.delete(0, tk.END)
            self.hide_window()
    
    def write(self, text):
        lines = text.split("\n")
        for line in lines[:-1]:
            if len(line):
                keyboard.write(line)
                keyboard.press_and_release("shift+enter")
        
        if lines[-1]:
            keyboard.write(lines[-1])
    
    def add(self):
        add = Modify(self.root, window_title = Modify.add, callback = self.listbox.create)

        add.transient(self.root)
        add.geometry(f"+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")
        add.grab_set()
        add.wait_window()
        self.search_entry.delete(0, tk.END)
    
    def edit(self):
        item = self.listbox.get_top()
        
        edit = Modify(self.root, callback = lambda *args: self.listbox.edit(item.title, *args), window_title = Modify.edit, item = item)

        edit.transient(self.root)
        edit.geometry(f"+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")
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