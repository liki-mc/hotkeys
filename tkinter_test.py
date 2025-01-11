import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)
 
        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL)
        vscrollbar.pack(fill = tk.Y, side = tk.RIGHT, expand = tk.FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, 
                                width = 200, height = 300,
                                yscrollcommand=vscrollbar.set)
        self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.TRUE)
        vscrollbar.config(command = self.canvas.yview)
 
 
        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = ttk.Frame(self.canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        self.interior_id = self.canvas.create_window(0, 0, window = self.interior, anchor = tk.NW)
        self.canvas.bind('<Configure>', self._configure_canvas)
        
       #  self.canvas.configure(yscrollcommand = self.scrollbar.set)

        # Bind mouse wheel event for scrolling
        self.canvas.bind_all("<MouseWheel>", self._configure_interior)
    
    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width = self.interior.winfo_reqwidth())
    
    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())

def main():
    root = tk.Tk()
    root.title("Scrollable Container Example")

    scrollable_frame = ScrollableFrame(root)
    scrollable_frame.pack(fill=tk.BOTH, expand=True)

    # Add some items to the scrollable frame
    # labels = [tk.Label(scrollable_frame.interior, text=f"Item {i+1}") for i in range(25)]
    # for label in labels:
    #     label.pack(fill = tk.X)
    
    for i in range(25):
        frame = tk.Frame(scrollable_frame.interior, borderwidth = 2, relief = "groove")
        frame.pack(fill = tk.X)
        label = tk.Label(frame, text = f"Item {i+1}")
        label.pack(fill = tk.X)
        text = tk.Label(frame, text = f"Description of item {i+1}")
        text.pack(fill = tk.X)
    

    # Example of showing an item after a delay
    def show_first_item():
        if labels:
            scrollable_frame.show_item(labels[0])

    # Remove the first item after 2 seconds
    # root.after(2000, remove_first_item)
    # Show the first item after 4 seconds
    # root.after(4000, show_first_item)

    root.mainloop()

if __name__ == "__main__":
    main()