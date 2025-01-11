import tkinter as tk

from dataclasses import dataclass
from typing import Iterable

class ScrollableFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scrollbar = tk.Scrollbar(self, orient = tk.VERTICAL)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y, expand = tk.FALSE)
        self.canvas = tk.Canvas(self, bd = 0, 
                                highlightthickness = 0, 
                                yscrollcommand = self.scrollbar.set,
                                width = 200, height = 300)
        self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.TRUE)
        self.scrollbar.config(command = self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", self._configure_scrollable_frame)
        self.scrollable_frame_id = self.canvas.create_window(0, 0, window = self.scrollable_frame, anchor = tk.NW)
        self.canvas.bind("<Configure>", self._configure_canvas)

        # Bind the mouse wheel event to the on_mouse_wheel method
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
    
    def _configure_scrollable_frame(self, event: tk.Event):
        # Update the scrollregion of the canvas to encompass the frame
        size = (self.scrollable_frame.winfo_reqwidth(), self.scrollable_frame.winfo_reqheight())
        self.canvas.config(scrollregion = (0, 0, size[0], size[1]))
        if self.scrollable_frame.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.itemconfigure(self.scrollable_frame_id, width = self.canvas.winfo_width())
    
    def _configure_canvas(self, event: tk.Event):
        if self.scrollable_frame.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.scrollable_frame_id, width = self.canvas.winfo_width())

    def on_frame_configure(self, event):
        # Update the scrollregion of the canvas to encompass the frame
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def on_mouse_wheel(self, event: tk.Event):
        # Scroll the canvas based on the mouse wheel movement
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def add_item(self, item: tk.Widget):
        # Add a new item to the scrollable frame
        item.pack(in_ = self.scrollable_frame, fill = tk.X)

    def set_widgets(self, *widgets: tk.Widget):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.pack_forget()  # Use pack_forget instead of destroy
        
        # Add new widgets
        for widget in widgets:
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

@dataclass
class Item:
    title: str
    tags: set[str]
    widget: tk.Widget

    def __post_init__(self):
        self.title = self.title.lower()
        self.tags = set([tag.lower() for tag in self.tags])
        self.tags.add(self.title)

class ListBox(ScrollableFrame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.items: list[Item] = []
        self.current_query = ""
    
    def create_widget(self, title: str, text: str) -> tk.Widget:
        # frame = tk.Frame(self.scrollable_frame, bd = 2, relief = tk.RAISED, height = 100, width = self.scrollable_frame.winfo_width())
        # frame.pack_propagate(False)

        # title_label = tk.Label(frame, text = title, font = ("Helvetica", 10, "bold"))
        # text_label = tk.Label(frame, text = text, wraplength = 200, anchor = tk.N)
        
        # title_label.pack(fill = tk.X, padx = 5, pady = 5)
        # text_label.pack(fill = tk.X, padx = 5, pady = 5)
        
        # # frame.pack(fill = tk.X, padx = 5, pady = 5)
        # return frame
        return tk.Label(self.scrollable_frame, relief = tk.RAISED, text = title, font = ("Helvetica", 10, "bold"), height = 2)
    
    def create(self, title: str, text: str, tags: Iterable[str] = set()) -> None:
        widget = self.create_widget(title, text)
        new_item = Item(title, tags, widget)
        self._create(new_item)
    
    def _create(self, new_item: Item) -> None:
        self.items.append(new_item)
        self.items.sort(key = lambda item: item.title)

        self._display()
    
    def _display(self) -> None:
        if not self.current_query:
            self.set_widgets(*[item.widget for item in self.items])
        else:
            self.set_widgets(*[item.widget for item in self.items if [tag for tag in item.tags if self.current_query in tag]])
    
    def filter(self, query: str) -> None:
        self.current_query = query.lower()
        self._display()

def test_listbox():
    root = tk.Tk()
    root.title("ListBox Test")
    root.geometry("400x400")

    listbox = ListBox(root)

    # Add some items to the listbox
    listbox.create("Item 1", "This is the first item.", tags = ["first", "example"])
    listbox.create("Itemdqsfqsdfqsdfqs 2", "This is the second item.", tags = ["second", "sample"])
    listbox.create("Item 3", "This is the third item.", tags = ["third", "demo"])
    listbox.create("Item 4", "This is the fourth item.", tags = ["fourth", "test"])
    listbox.create("Item 5", "This is the fifth item.", tags = ["fifth", "trial"])
    listbox.create("Item 6", "This is the sixth item.", tags = ["sixth", "experiment"])
    listbox.create("Item 7", "This is the seventh item.", tags = ["seventh", "prototype"])
    listbox.create("Item 8", "This is the eighth item.", tags = ["eighth", "pilot"])
    listbox.create("Item 9", "This is the ninth item.", tags = ["ninth", "mockup"])
    listbox.create("Item 10", "This is the tenth item.", tags = ["tenth", "model"])


    # Entry widget for filtering
    search_var = tk.StringVar()
    search_entry = tk.Entry(root, textvariable = search_var)
    search_entry.pack(pady = 10, padx = 10, fill = tk.X)
    listbox.pack(fill = tk.BOTH, expand = True)

    # Bind the entry widget to the filter method
    search_var.trace("w", lambda name, index, mode, sv = search_var: listbox.filter(sv.get()))

    root.mainloop()

if __name__ == "__main__":
    test_listbox()