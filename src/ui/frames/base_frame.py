import tkinter as tk


class BaseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # MainWindow
        self.app = controller.controller  # App (Tk root)
        self.config = controller.config  # ConfigManager
        self.theme = controller.theme

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def refresh(self):
        pass

    def apply_bg(self):
        self.configure(bg=self.theme["bg"])
