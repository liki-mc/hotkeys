import arcade

class ArcadeWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_update_rate(1/60)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Hello, Arcade!", self.width // 2, self.height // 2, arcade.color.WHITE, 24, anchor_x="center")

    def on_update(self, delta_time):
        pass

def main():
    window = ArcadeWindow(800, 600, "Arcade Window")
    window.set_visible(False)

    def show_window():
        window.set_visible(True)
        # window.activate()

    def hide_window():
        window.set_visible(False)
        # window.minimize()

    while True:
        command = input("Enter 'show' to show the window, 'hide' to hide the window, or 'exit' to exit: ").strip().lower()
        if command == 'show':
            show_window()
        elif command == 'hide':
            hide_window()
        elif command == 'exit':
            hide_window()
            break

if __name__ == "__main__":
    main()