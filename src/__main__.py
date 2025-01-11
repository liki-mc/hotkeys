
from .main import App


if __name__ == "__main__":
    with App() as app:
        app.run()