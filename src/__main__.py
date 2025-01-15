
from .main import App

from .config import Config


if __name__ == "__main__":
    with App() as app:
        app.run()