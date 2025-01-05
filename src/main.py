import tkinter as tk
import keyboard

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My Application")
        self.root.geometry("900x600")  # Set the size of the window
        self.root.after(50, self.check)

        # Bind the close event to hide the window
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        # Bind the Esc key to hide the window
        self.root.bind('<Escape>', lambda e: self.hide_window())

        # Initially hide the window
        self.root.withdraw()

    def show_window(self):
        self.root.deiconify()  # Show the window

    def hide_window(self):
        self.root.withdraw()  # Hide the window

    def run(self):
        # Set up the hotkey (e.g., Ctrl + Alt + G)
        keyboard.add_hotkey('ctrl+alt+g', self.toggle_window)

        # Start the Tkinter main loop
        self.root.mainloop()

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