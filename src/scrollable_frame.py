import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create a canvas
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient = "vertical", command = self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Configure the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window = self.scrollable_frame, anchor = "nw")

        # Pack the canvas and scrollbar
        self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand=True)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        self.canvas.configure(yscrollcommand = self.scrollbar.set)

        # Bind mouse wheel event for scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.bind_all("a", lambda e: self.add_item(tk.Label(self.scrollable_frame, text = "New Item")))
        self.bind_all("r", lambda e: self.remove_item(self.scrollable_frame.winfo_children()[0]))

    def on_mouse_wheel(self, event: tk.Event):
        # Scroll the canvas based on the mouse wheel movement
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def add_item(self, item: tk.Widget):
        # Add a new item to the scrollable frame
        item.pack(in_ = self.scrollable_frame, fill = tk.X)

    def set_widgets(self, *args):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.pack_forget()  # Use pack_forget instead of destroy
        
        # Add new widgets
        for widget in args:
            self.add_item(widget)

    def remove_item(self, item: tk.Widget):
        # Remove the item from the frame without destroying it
        item.pack_forget()  # Use pack_forget to remove it from the layout

    def show_item(self, item: tk.Widget):
        # Re-add the item to the frame
        item.pack(in_ = self.scrollable_frame, fill = tk.X)

def test_scrollable_frame():
    root = tk.Tk()
    root.title("Scrollable Container Example")

    scrollable_frame = ScrollableFrame(root)
    scrollable_frame.pack(fill = tk.BOTH, expand = True)

    # Add some items to the scrollable frame
    labels = [tk.Label(scrollable_frame.scrollable_frame, text = f"Item {i+1}") for i in range(5)]
    for label in labels:
        scrollable_frame.add_item(label)

    # Example of removing an item after a delay
    def remove_first_item():
        if scrollable_frame.scrollable_frame.winfo_children():
            scrollable_frame.remove_item(scrollable_frame.scrollable_frame.winfo_children()[0])

    # Example of showing an item after a delay
    def show_first_item():
        if labels:
            scrollable_frame.show_item(labels[0])

    # Remove the first item after 2 seconds
    root.after(2000, remove_first_item)
    
    # Show the first item after 4 seconds
    root.after(4000, show_first_item)

    root.mainloop()

class ListScrollabelFrame(ScrollableFrame):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items
        self.set_widgets(*items)


if __name__ == "__main__":
    test_scrollable_frame()