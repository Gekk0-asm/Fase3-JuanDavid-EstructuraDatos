import tkinter as tk

from src.config import ConfigManager
from src.ui.window import MainWindow


class App:
    def __init__(self, config_path: str = None):
        self.root = tk.Tk()
        self.root.title("Compensándote")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        self.config = ConfigManager(config_path)

        # Aplicar color de fondo del tema a la ventana raíz
        theme = self.config.get_theme()
        self.root.configure(bg=theme["bg"])

        self.window = MainWindow(self.root, self.config)
        self.window.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()
