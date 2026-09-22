import argparse
import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "innova_desktop.db"

NAVY = "#172A3A"
NAVY_DARK = "#102130"
GOLD = "#D4A64A"
BG = "#F4F6F8"
CARD = "#FFFFFF"
TEXT = "#1D2730"
MUTED = "#6D7780"
GREEN = "#1E9B63"
RED = "#D9434E"
BLUE = "#2B6FF2"
BORDER = "#DDE2E7"


def money(value):
    try:
        return f"${float(value):,.0f} MXN"
    except Exception:
        return str(value)


class Database:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.create_schema()
        self.seed()

    def create_schema(self):
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                type TEXT NOT NULL,
                location TEXT NOT NULL,
                operation TEXT NOT NULL,
                price REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Disponible'
            );

            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client TEXT NOT NULL,
                property_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pendiente',
                FOREIGN KEY(property_id) REFERENCES properties(id)
            );
            """
        )
        self.conn.commit()

    def seed(self):
        count = self.conn.execute("SELECT COUNT(*) FROM properties").fetchone()[0]
        if count == 0:
            rows = [
                ("Casa Familiar Cholula", "Casa", "San Pedro Cholula, Puebla", "Venta", 3250000, "Disponible"),
                ("Residencia La Paz", "Casa", "La Paz, Puebla", "Renta", 25000, "Disponible"),
                ("Departamento Angelópolis", "Departamento", "Angelópolis, Puebla", "Renta", 18500, "En proceso"),
                ("Casa Lomas de Angelópolis", "Casa", "Lomas de Angelópolis, Puebla", "Venta", 4890000, "Disponible"),
                ("Loft Centro Histórico", "Departamento", "Centro, Puebla", "Venta", 1650000, "Vendida"),
            ]
            self.conn.executemany(
                "INSERT INTO properties(title,type,location,operation,price,status) VALUES(?,?,?,?,?,?)",
                rows,
            )
            self.conn.commit()
        count = self.conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
        if count == 0:
            rows = [
                ("Mariana López", 1, "2026-09-22", "11:00", "Confirmada"),
                ("Carlos Pérez", 2, "2026-09-22", "16:30", "Pendiente"),
                ("Sofía Ramírez", 4, "2026-09-23", "10:00", "Pendiente"),
                ("Jorge Hernández", 3, "2026-09-24", "13:00", "Cancelada"),
            ]
            self.conn.executemany(
                "INSERT INTO appointments(client,property_id,appointment_date,appointment_time,status) VALUES(?,?,?,?,?)",
                rows,
            )
            self.conn.commit()

    def properties(self, search="", status="Todos"):
        q = "SELECT * FROM properties WHERE 1=1"
        args = []
        if search:
            q += " AND (title LIKE ? OR location LIKE ? OR type LIKE ? OR operation LIKE ?)"
            term = f"%{search}%"
            args += [term, term, term, term]
        if status != "Todos":
            q += " AND status = ?"
            args.append(status)
        q += " ORDER BY id DESC"
        return self.conn.execute(q, args).fetchall()

    def add_property(self, title, type_, location, operation, price, status="Disponible"):
        self.conn.execute(
            "INSERT INTO properties(title,type,location,operation,price,status) VALUES(?,?,?,?,?,?)",
            (title, type_, location, operation, price, status),
        )
        self.conn.commit()

    def set_property_status(self, property_id, status):
        self.conn.execute("UPDATE properties SET status=? WHERE id=?", (status, property_id))
        self.conn.commit()

    def appointments(self):
        return self.conn.execute(
            """
            SELECT a.*, p.title property_title
            FROM appointments a
            JOIN properties p ON p.id=a.property_id
            ORDER BY a.appointment_date, a.appointment_time
            """
        ).fetchall()

    def add_appointment(self, client, property_id, d, t):
        self.conn.execute(
            "INSERT INTO appointments(client,property_id,appointment_date,appointment_time,status) VALUES(?,?,?,?,?)",
            (client, property_id, d, t, "Pendiente"),
        )
        self.conn.commit()

    def set_appointment_status(self, appointment_id, status):
        self.conn.execute("UPDATE appointments SET status=? WHERE id=?", (status, appointment_id))
        self.conn.commit()

    def stats(self):
        total = self.conn.execute("SELECT COUNT(*) FROM properties").fetchone()[0]
        available = self.conn.execute("SELECT COUNT(*) FROM properties WHERE status='Disponible'").fetchone()[0]
        pending = self.conn.execute("SELECT COUNT(*) FROM appointments WHERE status='Pendiente'").fetchone()[0]
        portfolio = self.conn.execute("SELECT COALESCE(SUM(price),0) FROM properties WHERE operation='Venta'").fetchone()[0]
        return total, available, pending, portfolio


class InnovaDesktop(tk.Tk):
    def __init__(self, initial_view="dashboard"):
        super().__init__()
        self.title("INNOVA Desktop - Administrador inmobiliario")
        self.geometry("1220x760")
        self.minsize(1000, 650)
        self.configure(bg=BG)
        self.db = Database()
        self.current_view = None
        self._configure_styles()
        self._build_shell()
        self.show_view(initial_view)

    def _configure_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=TEXT, rowheight=34, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#EEF1F4", foreground=TEXT, font=("Segoe UI Semibold", 10), relief="flat")
        style.map("Treeview", background=[("selected", "#DDEAFF")], foreground=[("selected", TEXT)])
        style.configure("TCombobox", padding=5)

    def _build_shell(self):
        self.sidebar = tk.Frame(self, bg=NAVY, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = tk.Frame(self.sidebar, bg=NAVY, height=105)
        logo.pack(fill="x")
        logo.pack_propagate(False)
        tk.Label(logo, text="▦  INNOVA", bg=NAVY, fg="white", font=("Georgia", 22, "bold")).pack(anchor="w", padx=22, pady=(28, 0))
        tk.Label(logo, text="DESKTOP", bg=NAVY, fg=GOLD, font=("Segoe UI Semibold", 9)).pack(anchor="w", padx=55, pady=(1, 0))

        self.nav_buttons = {}
        items = [
            ("dashboard", "⌂  Resumen"),
            ("properties", "▤  Propiedades"),
            ("appointments", "◷  Citas"),
        ]
        for key, text in items:
            b = tk.Button(
                self.sidebar,
                text=text,
                command=lambda k=key: self.show_view(k),
                anchor="w",
                bd=0,
                relief="flat",
                bg=NAVY,
                fg="#E9EEF2",
                activebackground=NAVY_DARK,
                activeforeground="white",
                font=("Segoe UI", 11),
                padx=22,
                pady=14,
                cursor="hand2",
            )
            b.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[key] = b

        tk.Frame(self.sidebar, bg="#294050", height=1).pack(fill="x", padx=20, pady=(18, 15))
        tk.Label(self.sidebar, text="Administrador", bg=NAVY, fg="white", font=("Segoe UI Semibold", 10)).pack(anchor="w", padx=22)
        tk.Label(self.sidebar, text="Gestión local de propiedades", bg=NAVY, fg="#AAB8C2", font=("Segoe UI", 9)).pack(anchor="w", padx=22, pady=(4, 0))

        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        header = tk.Frame(self.main, bg=CARD, height=78, highlightbackground=BORDER, highlightthickness=1)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Panel de administración", bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 17)).pack(side="left", padx=28)
        tk.Label(header, text="INNOVA", bg="#EEF2F5", fg=NAVY, font=("Segoe UI Semibold", 10), padx=14, pady=7).pack(side="right", padx=28)

        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=28, pady=24)

    def clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def show_view(self, view):
        self.current_view = view
        for key, btn in self.nav_buttons.items():
            btn.configure(bg=NAVY_DARK if key == view else NAVY, fg="white" if key == view else "#E9EEF2")
        self.clear_content()
        if view == "properties":
            self.build_properties()
        elif view == "appointments":
            self.build_appointments()
        else:
            self.build_dashboard()

    def title_block(self, title, subtitle):
        block = tk.Frame(self.content, bg=BG)
        block.pack(fill="x", pady=(0, 18))
        tk.Label(block, text=title, bg=BG, fg=TEXT, font=("Georgia", 25, "bold")).pack(anchor="w")
        tk.Label(block, text=subtitle, bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(5, 0))

    def stat_card(self, parent, title, value, hint, accent):
        card = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Frame(card, bg=accent, height=5).pack(fill="x")
        tk.Label(card, text=title, bg=CARD, fg=MUTED, font=("Segoe UI Semibold", 9)).pack(anchor="w", padx=16, pady=(14, 4))
        tk.Label(card, text=value, bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 22)).pack(anchor="w", padx=16)
        tk.Label(card, text=hint, bg=CARD, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=16, pady=(4, 14))
        return card

    def build_dashboard(self):
        self.title_block("Resumen", "Vista general de la operación inmobiliaria y las próximas actividades.")
        total, available, pending, portfolio = self.db.stats()
        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x")
        self.stat_card(cards, "PROPIEDADES", str(total), "Inventario registrado", BLUE)
        self.stat_card(cards, "DISPONIBLES", str(available), "Listas para negociar", GREEN)
        self.stat_card(cards, "CITAS PENDIENTES", str(pending), "Requieren seguimiento", GOLD)
        self.stat_card(cards, "VALOR EN VENTA", money(portfolio), "Suma del inventario", NAVY)

        lower = tk.Frame(self.content, bg=BG)
        lower.pack(fill="both", expand=True, pady=(22, 0))
        left = tk.Frame(lower, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        right = tk.Frame(lower, bg=CARD, highlightbackground=BORDER, highlightthickness=1, width=310)
        right.pack(side="left", fill="y")
        right.pack_propagate(False)

        tk.Label(left, text="Propiedades recientes", bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 13)).pack(anchor="w", padx=18, pady=(16, 10))
        recent = self.db.properties()[:5]
        for p in recent:
            row = tk.Frame(left, bg=CARD)
            row.pack(fill="x", padx=18, pady=6)
            icon = tk.Label(row, text="⌂", bg="#EEF2F5", fg=NAVY, font=("Segoe UI", 14), width=3, height=1)
            icon.pack(side="left")
            txt = tk.Frame(row, bg=CARD)
            txt.pack(side="left", padx=10, fill="x", expand=True)
            tk.Label(txt, text=p["title"], bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 10)).pack(anchor="w")
            tk.Label(txt, text=f'{p["location"]} · {p["operation"]}', bg=CARD, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w")
            tk.Label(row, text=money(p["price"]), bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 10)).pack(side="right")

        tk.Label(right, text="Próximas citas", bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 13)).pack(anchor="w", padx=18, pady=(16, 10))
        for a in self.db.appointments()[:4]:
            box = tk.Frame(right, bg="#F7F8FA", highlightbackground=BORDER, highlightthickness=1)
            box.pack(fill="x", padx=16, pady=6)
            tk.Label(box, text=a["appointment_date"], bg="#F7F8FA", fg=NAVY, font=("Segoe UI Semibold", 9)).pack(anchor="w", padx=12, pady=(8, 1))
            tk.Label(box, text=f'{a["appointment_time"]} · {a["client"]}', bg="#F7F8FA", fg=TEXT, font=("Segoe UI", 9)).pack(anchor="w", padx=12)
            tk.Label(box, text=a["property_title"], bg="#F7F8FA", fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w", padx=12, pady=(1, 8))

    def build_properties(self):
        self.title_block("Propiedades", "Consulta, registra y actualiza el estado de casas y departamentos.")
        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", pady=(0, 14))
        self.search_var = tk.StringVar()
        search = tk.Entry(top, textvariable=self.search_var, font=("Segoe UI", 10), relief="solid", bd=1)
        search.pack(side="left", ipady=8, ipadx=8, fill="x", expand=True)
        search.insert(0, "Buscar por nombre, ubicación o tipo...")
        search.bind("<FocusIn>", lambda e: self._clear_placeholder(search))
        search.bind("<Return>", lambda e: self.refresh_properties())
        self.status_var = tk.StringVar(value="Todos")
        combo = ttk.Combobox(top, textvariable=self.status_var, values=["Todos", "Disponible", "En proceso", "Vendida", "Rentada"], state="readonly", width=14)
        combo.pack(side="left", padx=10, ipady=5)
        combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_properties())
        tk.Button(top, text="Buscar", command=self.refresh_properties, bg=NAVY, fg="white", bd=0, padx=20, pady=9, font=("Segoe UI Semibold", 10), cursor="hand2").pack(side="left")
        tk.Button(top, text="+ Nueva propiedad", command=self.open_property_dialog, bg=GOLD, fg=NAVY_DARK, bd=0, padx=18, pady=9, font=("Segoe UI Semibold", 10), cursor="hand2").pack(side="left", padx=(10, 0))

        wrap = tk.Frame(self.content, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        wrap.pack(fill="both", expand=True)
        cols = ("id", "title", "type", "location", "operation", "price", "status")
        self.property_tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="browse")
        headings = {"id": "ID", "title": "Propiedad", "type": "Tipo", "location": "Ubicación", "operation": "Operación", "price": "Precio", "status": "Estado"}
        widths = {"id": 45, "title": 190, "type": 100, "location": 210, "operation": 90, "price": 130, "status": 105}
        for c in cols:
            self.property_tree.heading(c, text=headings[c])
            self.property_tree.column(c, width=widths[c], anchor="w" if c not in ("id", "price") else "center")
        self.property_tree.pack(fill="both", expand=True, padx=12, pady=(12, 0))
        actions = tk.Frame(wrap, bg=CARD)
        actions.pack(fill="x", padx=12, pady=12)
        tk.Button(actions, text="Marcar disponible", command=lambda: self.change_property_status("Disponible"), bg="#E9F7F0", fg=GREEN, bd=0, padx=14, pady=8, font=("Segoe UI Semibold", 9)).pack(side="left")
        tk.Button(actions, text="En proceso", command=lambda: self.change_property_status("En proceso"), bg="#FFF5DE", fg="#9A6B00", bd=0, padx=14, pady=8, font=("Segoe UI Semibold", 9)).pack(side="left", padx=8)
        tk.Button(actions, text="Marcar vendida", command=lambda: self.change_property_status("Vendida"), bg="#FDEBED", fg=RED, bd=0, padx=14, pady=8, font=("Segoe UI Semibold", 9)).pack(side="left")
        self.refresh_properties()

    def _clear_placeholder(self, widget):
        if widget.get().startswith("Buscar por"):
            widget.delete(0, "end")

    def refresh_properties(self):
        for i in self.property_tree.get_children():
            self.property_tree.delete(i)
        search = self.search_var.get().strip()
        if search.startswith("Buscar por"):
            search = ""
        for p in self.db.properties(search, self.status_var.get()):
            self.property_tree.insert("", "end", values=(p["id"], p["title"], p["type"], p["location"], p["operation"], money(p["price"]), p["status"]))

    def change_property_status(self, status):
        sel = self.property_tree.selection()
        if not sel:
            messagebox.showinfo("INNOVA", "Selecciona una propiedad de la tabla.")
            return
        pid = self.property_tree.item(sel[0], "values")[0]
        self.db.set_property_status(pid, status)
        self.refresh_properties()

    def open_property_dialog(self):
        win = tk.Toplevel(self)
        win.title("Nueva propiedad")
        win.geometry("540x520")
        win.transient(self)
        win.grab_set()
        win.configure(bg=CARD)
        tk.Label(win, text="Registrar propiedad", bg=CARD, fg=TEXT, font=("Georgia", 21, "bold")).pack(anchor="w", padx=28, pady=(24, 4))
        tk.Label(win, text="Agrega un inmueble al inventario local de INNOVA.", bg=CARD, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=28, pady=(0, 18))
        form = tk.Frame(win, bg=CARD)
        form.pack(fill="both", expand=True, padx=28)
        fields = {}
        def field(label, key):
            tk.Label(form, text=label, bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 9)).pack(anchor="w", pady=(8, 4))
            e = tk.Entry(form, font=("Segoe UI", 10), relief="solid", bd=1)
            e.pack(fill="x", ipady=7)
            fields[key] = e
        field("Nombre de la propiedad", "title")
        field("Ubicación", "location")
        field("Precio", "price")
        row = tk.Frame(form, bg=CARD)
        row.pack(fill="x", pady=(10, 0))
        left = tk.Frame(row, bg=CARD)
        right = tk.Frame(row, bg=CARD)
        left.pack(side="left", fill="x", expand=True, padx=(0, 8))
        right.pack(side="left", fill="x", expand=True, padx=(8, 0))
        tk.Label(left, text="Tipo", bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 9)).pack(anchor="w", pady=(0, 4))
        type_var = tk.StringVar(value="Casa")
        ttk.Combobox(left, textvariable=type_var, values=["Casa", "Departamento", "Terreno", "Local"], state="readonly").pack(fill="x", ipady=4)
        tk.Label(right, text="Operación", bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 9)).pack(anchor="w", pady=(0, 4))
        op_var = tk.StringVar(value="Venta")
        ttk.Combobox(right, textvariable=op_var, values=["Venta", "Renta"], state="readonly").pack(fill="x", ipady=4)
        def save():
            try:
                title = fields["title"].get().strip()
                location = fields["location"].get().strip()
                price = float(fields["price"].get().replace(",", ""))
                if not title or not location:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Datos incompletos", "Captura nombre, ubicación y un precio válido.", parent=win)
                return
            self.db.add_property(title, type_var.get(), location, op_var.get(), price)
            win.destroy()
            if self.current_view == "properties":
                self.refresh_properties()
            else:
                self.show_view("properties")
        tk.Button(form, text="Guardar propiedad", command=save, bg=NAVY, fg="white", bd=0, padx=18, pady=11, font=("Segoe UI Semibold", 10)).pack(fill="x", pady=(22, 8))
        tk.Button(form, text="Cancelar", command=win.destroy, bg="#EEF1F4", fg=TEXT, bd=0, padx=18, pady=10, font=("Segoe UI", 10)).pack(fill="x")

    def build_appointments(self):
        self.title_block("Citas", "Agenda visitas y da seguimiento a las citas relacionadas con las propiedades.")
        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", pady=(0, 14))
        tk.Button(top, text="+ Agendar cita", command=self.open_appointment_dialog, bg=GOLD, fg=NAVY_DARK, bd=0, padx=18, pady=9, font=("Segoe UI Semibold", 10), cursor="hand2").pack(side="right")
        wrap = tk.Frame(self.content, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        wrap.pack(fill="both", expand=True)
        cols = ("id", "client", "property", "date", "time", "status")
        self.appointment_tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="browse")
        headings = {"id": "ID", "client": "Cliente", "property": "Propiedad", "date": "Fecha", "time": "Hora", "status": "Estado"}
        widths = {"id": 45, "client": 180, "property": 260, "date": 110, "time": 85, "status": 120}
        for c in cols:
            self.appointment_tree.heading(c, text=headings[c])
            self.appointment_tree.column(c, width=widths[c], anchor="w" if c not in ("id", "time") else "center")
        self.appointment_tree.pack(fill="both", expand=True, padx=12, pady=(12, 0))
        actions = tk.Frame(wrap, bg=CARD)
        actions.pack(fill="x", padx=12, pady=12)
        tk.Button(actions, text="Confirmar", command=lambda: self.change_appointment_status("Confirmada"), bg="#E9F7F0", fg=GREEN, bd=0, padx=18, pady=8, font=("Segoe UI Semibold", 9)).pack(side="left")
        tk.Button(actions, text="Pendiente", command=lambda: self.change_appointment_status("Pendiente"), bg="#FFF5DE", fg="#9A6B00", bd=0, padx=18, pady=8, font=("Segoe UI Semibold", 9)).pack(side="left", padx=8)
        tk.Button(actions, text="Cancelar", command=lambda: self.change_appointment_status("Cancelada"), bg="#FDEBED", fg=RED, bd=0, padx=18, pady=8, font=("Segoe UI Semibold", 9)).pack(side="left")
        self.refresh_appointments()

    def refresh_appointments(self):
        for i in self.appointment_tree.get_children():
            self.appointment_tree.delete(i)
        for a in self.db.appointments():
            self.appointment_tree.insert("", "end", values=(a["id"], a["client"], a["property_title"], a["appointment_date"], a["appointment_time"], a["status"]))

    def change_appointment_status(self, status):
        sel = self.appointment_tree.selection()
        if not sel:
            messagebox.showinfo("INNOVA", "Selecciona una cita de la tabla.")
            return
        aid = self.appointment_tree.item(sel[0], "values")[0]
        self.db.set_appointment_status(aid, status)
        self.refresh_appointments()

    def open_appointment_dialog(self):
        win = tk.Toplevel(self)
        win.title("Agendar cita")
        win.geometry("540x500")
        win.transient(self)
        win.grab_set()
        win.configure(bg=CARD)
        tk.Label(win, text="Agendar visita", bg=CARD, fg=TEXT, font=("Georgia", 21, "bold")).pack(anchor="w", padx=28, pady=(24, 4))
        tk.Label(win, text="Registra una cita de un cliente con una propiedad disponible.", bg=CARD, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=28, pady=(0, 18))
        form = tk.Frame(win, bg=CARD)
        form.pack(fill="both", expand=True, padx=28)
        tk.Label(form, text="Cliente", bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 9)).pack(anchor="w", pady=(8, 4))
        client = tk.Entry(form, font=("Segoe UI", 10), relief="solid", bd=1)
        client.pack(fill="x", ipady=7)
        tk.Label(form, text="Propiedad", bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 9)).pack(anchor="w", pady=(12, 4))
        props = self.db.properties(status="Disponible")
        prop_map = {f'{p["id"]} - {p["title"]}': p["id"] for p in props}
        prop_var = tk.StringVar(value=next(iter(prop_map), ""))
        ttk.Combobox(form, textvariable=prop_var, values=list(prop_map), state="readonly").pack(fill="x", ipady=4)
        row = tk.Frame(form, bg=CARD)
        row.pack(fill="x", pady=(12, 0))
        left = tk.Frame(row, bg=CARD); left.pack(side="left", fill="x", expand=True, padx=(0, 8))
        right = tk.Frame(row, bg=CARD); right.pack(side="left", fill="x", expand=True, padx=(8, 0))
        tk.Label(left, text="Fecha (AAAA-MM-DD)", bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 9)).pack(anchor="w", pady=(0, 4))
        d = tk.Entry(left, font=("Segoe UI", 10), relief="solid", bd=1); d.pack(fill="x", ipady=7); d.insert(0, date.today().isoformat())
        tk.Label(right, text="Hora (HH:MM)", bg=CARD, fg=TEXT, font=("Segoe UI Semibold", 9)).pack(anchor="w", pady=(0, 4))
        t = tk.Entry(right, font=("Segoe UI", 10), relief="solid", bd=1); t.pack(fill="x", ipady=7); t.insert(0, "12:00")
        def save():
            if not client.get().strip() or not prop_var.get():
                messagebox.showerror("Datos incompletos", "Captura cliente y propiedad.", parent=win)
                return
            self.db.add_appointment(client.get().strip(), prop_map[prop_var.get()], d.get().strip(), t.get().strip())
            win.destroy()
            if self.current_view == "appointments":
                self.refresh_appointments()
        tk.Button(form, text="Guardar cita", command=save, bg=NAVY, fg="white", bd=0, padx=18, pady=11, font=("Segoe UI Semibold", 10)).pack(fill="x", pady=(24, 8))
        tk.Button(form, text="Cancelar", command=win.destroy, bg="#EEF1F4", fg=TEXT, bd=0, padx=18, pady=10, font=("Segoe UI", 10)).pack(fill="x")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", choices=["dashboard", "properties", "appointments"], default="dashboard")
    parser.add_argument("--dialog", choices=["property", "appointment"], default=None)
    args = parser.parse_args()
    app = InnovaDesktop(args.view)
    if args.dialog == "property":
        app.after(500, app.open_property_dialog)
    elif args.dialog == "appointment":
        app.after(500, app.open_appointment_dialog)
    app.mainloop()


if __name__ == "__main__":
    main()
