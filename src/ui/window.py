import tkinter as tk

from ..config import ConfigManager
from .frames import LoginFrame
from .frames import RegisterFrame


class MainWindow(tk.Frame):
    def __init__(self, parent, config: ConfigManager):
        super().__init__(parent)
        self.controller = parent  # App
        self.config = config
        self.theme = config.get_theme()
        self.cliente_actual = None  # se llena al guardar

        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg=self.theme["bg"])

        # Contenedor donde se apilan los frames
        container = tk.Frame(self, bg=self.theme["bg"])
        container.pack(fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.current_frame = None

        for F in (LoginFrame, RegisterFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)

    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.on_exit()

        frame = self.frames[frame_class]
        self.current_frame = frame
        frame.on_enter()
        frame.tkraise()
