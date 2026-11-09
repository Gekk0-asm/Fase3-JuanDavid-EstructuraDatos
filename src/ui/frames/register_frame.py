import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from .base_frame import BaseFrame
from src.models import Affiliate, DataStructureManager


class RegisterFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.manager = DataStructureManager()
        self.apply_bg()
        self._configure_ttk_styles() # Configurar estilos de ttk primero
        self._build()

    def _configure_ttk_styles(self):
        """Configura los colores para los widgets de ttk (Treeview, Combobox)"""
        style = ttk.Style()
        style.theme_use("default")
        
        # Estilo del Treeview
        style.configure(
            "Treeview",
            background=self.theme["bg"],
            foreground=self.theme["fg"],
            fieldbackground=self.theme["bg"],
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=self.theme["secondary"],
            foreground=self.theme["primary"],
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        style.map("Treeview", background=[("selected", self.theme["selection"])])
        
        # Estilo del Combobox
        style.configure(
            "TCombobox",
            fieldbackground=self.theme["secondary"],
            background=self.theme["secondary"],
            foreground=self.theme["fg"],
            arrowcolor=self.theme["fg"],
            borderwidth=0
        )

    def _build(self):
        # Título
        tk.Label(
            self,
            text="Caja Compensándote - Control de Afiliados",
            font=("Segoe UI", 16, "bold"),
            bg=self.theme["bg"],
            fg=self.theme["accent"],
        ).pack(pady=15)

        # Frame de selección de estructura
        top_frame = tk.Frame(self, bg=self.theme["bg"])
        top_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            top_frame,
            text="Estructura:",
            bg=self.theme["bg"],
            fg=self.theme["fg"],
            font=("Segoe UI", 10),
        ).pack(side=tk.LEFT)
        
        self.structure_var = tk.StringVar(value="Pila")
        self.structure_combo = ttk.Combobox(
            top_frame,
            textvariable=self.structure_var,
            values=["Pila", "Cola", "Lista"],
            state="readonly",
            width=15,
        )
        self.structure_combo.pack(side=tk.LEFT, padx=5)
        self.structure_combo.bind("<<ComboboxSelected>>", self._on_structure_change)

        # Treeview
        columns = (
            "Tipo ID", "Número ID", "Nombre", "Ingresos",
            "Servicio", "Modalidad", "Tarifa", "Fecha",
        )
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Formulario
        form_frame = tk.Frame(self, bg=self.theme["bg"])
        form_frame.pack(fill="x", padx=10, pady=5)
        form_frame.columnconfigure(3, weight=1) # Para que los campos se expandan

        # --- Fila 1: Tipo ID, Número ID ---
        tk.Label(form_frame, text="Tipo ID:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=0, column=0, sticky="e", pady=3)
        self.id_type_var = tk.StringVar(value="CC")
        self.id_type_combo = ttk.Combobox(
            form_frame,
            textvariable=self.id_type_var,
            values=["CC", "CE", "NUIP", "PAS"],
            state="readonly",
            width=10,
        )
        self.id_type_combo.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        tk.Label(form_frame, text="Número ID:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=0, column=2, sticky="e", pady=3)
        self.id_number_entry = tk.Entry(
            form_frame,
            validate="key",
            validatecommand=(self.register(self._validate_numeric), "%S"),
            bg=self.theme["secondary"],
            fg=self.theme["fg"],
            insertbackground=self.theme["fg"],
            relief="flat",
            width=20
        )
        self.id_number_entry.grid(row=0, column=3, padx=5, pady=3, sticky="w")

        # --- Fila 2: Nombre completo ---
        tk.Label(form_frame, text="Nombre completo:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=1, column=0, sticky="e", pady=3)
        self.name_entry = tk.Entry(
            form_frame,
            validate="key",
            validatecommand=(self.register(self._validate_alpha), "%S"),
            bg=self.theme["secondary"],
            fg=self.theme["fg"],
            insertbackground=self.theme["fg"],
            relief="flat"
        )
        self.name_entry.grid(row=1, column=1, columnspan=3, sticky="we", padx=5, pady=3)

        # --- Fila 3: Ingresos actuales, Servicio deseado ---
        tk.Label(form_frame, text="Ingresos actuales:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=2, column=0, sticky="e", pady=3)
        self.income_entry = tk.Entry(
            form_frame,
            validate="key",
            validatecommand=(self.register(self._validate_numeric), "%S"),
            bg=self.theme["secondary"],
            fg=self.theme["fg"],
            insertbackground=self.theme["fg"],
            relief="flat",
            width=20
        )
        self.income_entry.grid(row=2, column=1, padx=5, pady=3, sticky="w")

        tk.Label(form_frame, text="Servicio deseado:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=2, column=2, sticky="e", pady=3)
        self.service_var = tk.StringVar(value="Subsidio de desempleo")
        self.service_combo = ttk.Combobox(
            form_frame,
            textvariable=self.service_var,
            values=[
                "Subsidio de desempleo",
                "Ingreso a parque",
                "Curso de formación",
                "Paquete de viaje",
                "Medicina preventiva",
            ],
            state="readonly",
        )
        self.service_combo.grid(row=2, column=3, padx=5, pady=3, sticky="w")

        # --- Fila 4: Modalidad de empleo ---
        tk.Label(form_frame, text="Modalidad:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=3, column=0, sticky="e", pady=3)
        self.modality_var = tk.StringVar(value="Empleado")
        modal_frame = tk.Frame(form_frame, bg=self.theme["bg"])
        modal_frame.grid(row=3, column=1, columnspan=3, sticky="w", padx=5, pady=3)
        
        tk.Radiobutton(
            modal_frame, text="Empleado", variable=self.modality_var, value="Empleado",
            command=self._calculate_fee, bg=self.theme["bg"], fg=self.theme["fg"],
            selectcolor=self.theme["secondary"], activebackground=self.theme["bg"], activeforeground=self.theme["fg"]
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Radiobutton(
            modal_frame, text="Independiente", variable=self.modality_var, value="Independiente",
            command=self._calculate_fee, bg=self.theme["bg"], fg=self.theme["fg"],
            selectcolor=self.theme["secondary"], activebackground=self.theme["bg"], activeforeground=self.theme["fg"]
        ).pack(side=tk.LEFT)

        # --- Fila 5: Tarifa de afiliación ---
        tk.Label(form_frame, text="Tarifa afiliación:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=4, column=0, sticky="e", pady=3)
        self.fee_entry = tk.Entry(
            form_frame, state="readonly", relief="flat",
            readonlybackground=self.theme["secondary"], fg=self.theme["primary"],
            width=20
        )
        self.fee_entry.grid(row=4, column=1, padx=5, pady=3, sticky="w")

        # --- Fila 6: Fecha ---
        tk.Label(form_frame, text="Fecha afiliación:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=5, column=0, sticky="e", pady=3)
        date_frame = tk.Frame(form_frame, bg=self.theme["bg"])
        date_frame.grid(row=5, column=1, columnspan=3, sticky="w", padx=5, pady=3)
        
        spin_opts = {"bg": self.theme["secondary"], "fg": self.theme["fg"], "buttonbackground": self.theme["selection"], "relief": "flat"}
        
        self.day_spin = tk.Spinbox(date_frame, from_=1, to=31, width=3, **spin_opts)
        self.day_spin.pack(side=tk.LEFT)
        tk.Label(date_frame, text="/", bg=self.theme["bg"], fg=self.theme["fg"]).pack(side=tk.LEFT, padx=2)
        self.month_spin = tk.Spinbox(date_frame, from_=1, to=12, width=3, **spin_opts)
        self.month_spin.pack(side=tk.LEFT)
        tk.Label(date_frame, text="/", bg=self.theme["bg"], fg=self.theme["fg"]).pack(side=tk.LEFT, padx=2)
        self.year_spin = tk.Spinbox(date_frame, from_=2000, to=2100, width=5, **spin_opts)
        self.year_spin.pack(side=tk.LEFT)
        
        # Valores por defecto
        today = datetime.now()
        self.day_spin.delete(0, tk.END)
        self.day_spin.insert(0, today.day)
        self.month_spin.delete(0, tk.END)
        self.month_spin.insert(0, today.month)
        self.year_spin.delete(0, tk.END)
        self.year_spin.insert(0, today.year)

        # --- Campo Reporte ---
        tk.Label(form_frame, text="Reporte:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=6, column=0, sticky="e", pady=5)
        self.report_entry = tk.Entry(
            form_frame, state="readonly", relief="flat",
            readonlybackground=self.theme["bg"], fg=self.theme["green"],
            font=("Segoe UI", 10, "bold")
        )
        self.report_entry.grid(row=6, column=1, columnspan=3, sticky="we", padx=5, pady=5)

        # --- Botones ---
        btn_frame = tk.Frame(self, bg=self.theme["bg"])
        btn_frame.pack(pady=15)
        
        btn_opts = {"font": ("Segoe UI", 10, "bold"), "width": 10, "relief": "flat", "cursor": "hand2"}
        
        tk.Button(btn_frame, text="Registrar", bg=self.theme["primary"], fg="#1a1b26", activebackground=self.theme["blue"], command=self._register, **btn_opts).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar", bg=self.theme["yellow"], fg="#1a1b26", activebackground=self.theme["orange"], command=self._clear_form, **btn_opts).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reporte", bg=self.theme["cyan"], fg="#1a1b26", activebackground=self.theme["teal"], command=self._show_report, **btn_opts).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eliminar", bg=self.theme["red"], fg="#1a1b26", activebackground=self.theme["pink"], command=self._delete, **btn_opts).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Salir", bg=self.theme["secondary"], fg=self.theme["fg"], activebackground=self.theme["selection"], command=self.app.quit, **btn_opts).pack(side=tk.LEFT, padx=5)

        # Eventos y carga inicial
        self.income_entry.bind("<KeyRelease>", lambda e: self._calculate_fee())
        self.service_combo.bind("<<ComboboxSelected>>", lambda e: self._calculate_fee())
        self.modality_var.trace_add("write", lambda *args: self._calculate_fee())

        self._refresh_tree()

    # --- Validaciones ---
    def _validate_numeric(self, char):
        return char.isdigit()

    def _validate_alpha(self, char):
        return char.isalpha() or char.isspace()

    # --- Lógica de negocio ---
    def _calculate_fee(self):
        try:
            income = int(self.income_entry.get() or 0)
        except ValueError:
            income = 0
        modality = self.modality_var.get()
        service = self.service_var.get()

        base_fee = 0
        if modality == "Empleado":
            if 1_000_000 <= income <= 2_000_000:
                base_fee = 45_000
            elif 2_000_000 < income <= 3_000_000:
                base_fee = 60_000
            elif 3_000_000 < income <= 4_000_000:
                base_fee = 75_000
            elif 4_000_000 < income <= 5_000_000:
                base_fee = 90_000
            elif income > 5_000_000:
                base_fee = 150_000
        else:
            if 1_000_000 <= income <= 2_000_000:
                base_fee = 10_000
            elif 2_000_000 < income <= 3_000_000:
                base_fee = 20_000
            elif 3_000_000 < income <= 4_000_000:
                base_fee = 30_000
            elif 4_000_000 < income <= 5_000_000:
                base_fee = 40_000
            elif income > 5_000_000:
                base_fee = 80_000

        if service == "Ingreso a parque":
            base_fee += 2_500
        elif service == "Curso de formación":
            base_fee += 7_500
        elif service == "Paquete de viaje":
            base_fee += 10_000
        elif service == "Medicina preventiva":
            base_fee += income * 0.10

        self.fee_entry.config(state="normal")
        self.fee_entry.delete(0, tk.END)
        self.fee_entry.insert(0, f"{int(base_fee)}")
        self.fee_entry.config(state="readonly")

    def _get_affiliate_data(self):
        day = self.day_spin.get()
        month = self.month_spin.get()
        year = self.year_spin.get()
        date_str = f"{day}/{month}/{year}"

        return Affiliate(
            identification_type=self.id_type_var.get(),
            identification_number=int(self.id_number_entry.get() or 0),
            full_name=self.name_entry.get(),
            current_income=int(self.income_entry.get() or 0),
            desired_service=self.service_var.get(),
            employment_modality=self.modality_var.get(),
            affiliation_fee=int(self.fee_entry.get() or 0),
            affiliation_date=date_str,
        )

    # --- Acciones de botones ---
    def _register(self):
        if (not self.id_number_entry.get() or not self.name_entry.get() or not self.income_entry.get()):
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
            return
        try:
            affiliate = self._get_affiliate_data()
        except ValueError:
            messagebox.showerror("Error", "Verifique los datos ingresados.")
            return

        structure = self.structure_var.get()
        self.manager.add_affiliate(structure, affiliate)
        self._refresh_tree()
        self._clear_form()
        messagebox.showinfo("Registro exitoso", f"Afiliado registrado en {structure}.")

    def _clear_form(self):
        self.id_number_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.income_entry.delete(0, tk.END)
        self.fee_entry.config(state="normal")
        self.fee_entry.delete(0, tk.END)
        self.fee_entry.config(state="readonly")
        self.report_entry.config(state="normal")
        self.report_entry.delete(0, tk.END)
        self.report_entry.config(state="readonly")

    def _show_report(self):
        structure = self.structure_var.get()
        report = self.manager.get_report(structure)
        self.report_entry.config(state="normal")
        self.report_entry.delete(0, tk.END)
        self.report_entry.insert(0, report)
        self.report_entry.config(state="readonly")

    def _delete(self):
        structure = self.structure_var.get()
        if structure == "Lista":
            # Corregido: simpledialog en lugar de tk.simpledialog
            id_str = simpledialog.askstring("Eliminar", "Ingrese el número de identificación:")
            if not id_str:
                return
            try:
                id_num = int(id_str)
            except ValueError:
                messagebox.showerror("Error", "Número inválido")
                return
            if not self.manager.list.find_by_id(id_num):
                messagebox.showwarning("No encontrado", "No existe un afiliado con ese número de ID.")
                return
            if messagebox.askyesno("Confirmar", f"¿Eliminar afiliado con ID {id_num}?"):
                self.manager.remove_affiliate("Lista", id_num)
        else:
            if messagebox.askyesno("Confirmar", f"¿Eliminar el último registro de la {structure}?"):
                self.manager.remove_affiliate(structure)
        self._refresh_tree()

    def _refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        structure = self.structure_var.get()
        affiliates = self.manager.get_affiliates(structure)
        for a in affiliates:
            self.tree.insert(
                "", tk.END,
                values=(
                    a.identification_type,
                    a.identification_number,
                    a.full_name,
                    a.current_income,
                    a.desired_service,
                    a.employment_modality,
                    a.affiliation_fee,
                    a.affiliation_date,
                ),
            )

    def _on_structure_change(self, event=None):
        self._refresh_tree()
        self.report_entry.config(state="normal")
        self.report_entry.delete(0, tk.END)
        self.report_entry.config(state="readonly")

    # --- Ciclo de vida ---
    def on_enter(self):
        self.app.title("Caja Compensándote - Control de Afiliados")
        self.app.geometry("1150x680")
        self.app.resizable(False, False)
        self.app.config(menu="") # Quita el menubar del login
        self._refresh_tree()