import tkinter as tk

class MyText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tag_configure("bold", font = ("Helvetica", 12, "bold"))
        self.tag_configure("normal", font = ("Helvetica", 12))
        self.tag_configure("title", font = ("Helvetica", 16, "bold"))

    def insert_text(self, text: str, tag: str = "normal"):
        self.insert(tk.END, text, tag)


def main():
    root = tk.Tk()
    root.title("Tkinter Text Example")

    text_widget = MyText(root, wrap="word", height=4, width=40)
    text_widget.pack()

    text_widget.insert_text("This is", "title")
    text_widget.insert_text(" bold ", "bold")
    text_widget.insert_text("and this is normal text.\n", "normal")
    text_widget.insert_text("Here is the second line with ", "normal")
    text_widget.insert_text("bold text", "bold")
    text_widget.insert_text(" and normal text.", "normal")

    text_widget.config(state=tk.DISABLED)

    root.mainloop()

if __name__ == "__main__":
    main()