import tkinter as tk
from tkinter import messagebox
from .base_frame import BaseFrame

from .register_frame import RegisterFrame


class LoginFrame(BaseFrame):

    PASSWORD = "Caja"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.apply_bg()
        self._build()

    def _build(self):
        # Menú
        self.menubar = tk.Menu(
            self.app,
            bg=self.theme["secondary"],
            fg=self.theme["fg"],
        )
        about_menu = tk.Menu(self.menubar, tearoff=0)
        about_menu.add_command(label="Acerca de", command=self._show_about)
        self.menubar.add_cascade(label="Acerca de", menu=about_menu)
        self.app.config(menu=self.menubar)

        tk.Label(
            self,
            text="Compensándote",
            font=("Segoe UI", 22, "bold"),
            bg=self.theme["bg"],
            fg=self.theme["fg"],
        ).pack(pady=15)

        tk.Label(
            self,
            text="Contraseña:",
            font=("Segoe UI", 11),
            bg=self.theme["bg"],
            fg=self.theme["fg"],
        ).pack()

        self.pwd_var = tk.StringVar()
        self.pwd_entry = tk.Entry(
            self,
            textvariable=self.pwd_var,
            show="*",  # enmascarada
            font=("Segoe UI", 12),
            width=20,
            justify="center",
        )
        self.pwd_entry.pack(pady=10)
        self.pwd_entry.focus_set()
        self.pwd_entry.bind("<Return>", lambda e: self._validar())

        btn_frame = tk.Frame(
            self,
            bg=self.theme["bg"],
        )
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Ingresar",
            bg=self.theme["primary"],
            fg="white",
            activebackground=self.theme["secondary"],
            font=("Segoe UI", 11, "bold"),
            width=8,
            command=self._validar,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Salir",
            bg=self.theme["red"],
            fg="white",
            activebackground=self.theme["secondary"],
            font=("Segoe UI", 11, "bold"),
            width=8,
            command=self.app.quit,
        ).pack(side=tk.LEFT, padx=5)

    def _validar(self):
        if self.pwd_var.get() == self.PASSWORD:
            from ..window import RegisterFrame

            self.controller.show_frame(RegisterFrame)
        else:
            messagebox.showerror("Acceso denegado", "Contraseña incorrecta")
            self.pwd_var.set("")
            self.pwd_entry.focus_set()

    def _show_about(self):
        messagebox.showinfo(
            "Acerca de",
            "Curso: Estructura de Datos\n"
            "Estudiante: Juan David Velasco Valderrama\n"
            "Grupo: 301305A_2204",
        )

    def on_enter(self):
        self.app.title("Login - Compensándote")
        self.app.geometry("350x250")
        self.app.resizable(False, False)

        self.app.config(menu=self.menubar)

        self.pwd_var.set("")
        self.pwd_entry.focus_set()

    def on_exit(self):
        self.app.config(menu="")
