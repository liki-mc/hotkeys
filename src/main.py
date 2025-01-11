import tkinter as tk
import keyboard

from .scrollable_frame import ListBox

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hotkeys")
        self.root.geometry("900x600")
        self.root.after(50, self.check)

        # Bind the close event to hide the window
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        
        self.listbox = ListBox(self.root)

        self.listbox.create("Item 10", "This is the tenth item.", tags = ["tenth", "model"])
        self.listbox.create("Item 1", "This is the first item.", tags = ["first", "example"])
        self.listbox.create("Itemdqsfqsdfqsdfqs 2", "This is the second item.", tags = ["second", "sample"])
        self.listbox.create("Item 3", "This is the third item.", tags = ["third", "demo"])
        self.listbox.create("Item 4", "This is the fourth item.", tags = ["fourth", "test"])
        self.listbox.create("Item 5", "This is the fifth item.", tags = ["fifth", "trial"])
        self.listbox.create("Item 6", "This is the sixth item.", tags = ["sixth", "experiment"])
        self.listbox.create("Item 7", "This is the seventh item.", tags = ["seventh", "prototype"])
        self.listbox.create("Item 8", "This is the eighth item.", tags = ["eighth", "pilot"])
        self.listbox.create("Item 9", "This is the ninth item.", tags = ["ninth", "mockup"])

        # Entry widget for filtering
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.root, textvariable = self.search_var)
        self.search_entry.pack(pady = 10, padx = 10, fill = tk.X)
        self.listbox.pack(fill = tk.BOTH, expand = True)

        # Bind on enter
        self.search_entry.bind('<Return>', self.on_enter)

        self.search_var.trace("w", lambda name, index, mode, sv = self.search_var: self.listbox.filter(sv.get()))

        # Bind the Esc key to hide the window
        self.root.bind('<Escape>', lambda e: self.hide_window())

        # Initially hide the window
        self.root.withdraw()

    def show_window(self):
        self.root.deiconify()  # Show the window
        self.search_entry.focus_set()

    def hide_window(self):
        self.root.withdraw()  # Hide the window

    def run(self):
        # Set up the hotkey (e.g., Ctrl + Alt + G)
        keyboard.add_hotkey('ctrl+alt+g', self.toggle_window)

        # Start the Tkinter main loop
        self.root.mainloop()
    
    def on_enter(self, event):
        if self.search_entry.get() in ["quit", "exit"]:
            self.root.quit()
            return
        text = self.listbox.get_top().text
        self.search_entry.delete(0, tk.END)
        self.hide_window()
        self.root.after(100, lambda: keyboard.write(text))

    def toggle_window(self):
        if self.root.winfo_viewable():
            self.hide_window()
        else:
            self.show_window()
    
    def check(self):
        self.root.after(50, self.check)

if __name__ == "__main__":
    app = App()
    app.run()