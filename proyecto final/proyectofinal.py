
# ══════════════════════════════════════════════════════════════
# DOCUMENTACIÓN GENERAL DEL SISTEMA
# ══════════════════════════════════════════════════════════════
#
# ENTRADAS:
# - Nombre de productos
# - Precio
# - Cantidad
# - Pago del cliente
#
# PROCESOS:
# - Registro de productos
# - Actualización de inventario
# - Gestión de ventas
# - Cálculo de cambio
# - Validación de datos
#
# SALIDAS:
# - Ticket de venta
# - Catálogo actualizado
# - Cambio calculado
# - Confirmaciones visuales
#
"""
PUNTO DE VENTA — TKINTER + SQLITE

DESCRIPCIÓN:
Sistema de punto de venta desarrollado en Python utilizando Tkinter
para la interfaz gráfica y SQLite como base de datos local.

FUNCIONES PRINCIPALES:
- Gestión de productos
- Control de inventario
- Registro de ventas
- Cálculo de cambio
- Administración de catálogo

La interfaz gráfica (GUI) fue desarrollada con apoyo de herramientas
de Inteligencia Artificial para mejorar el diseño visual y experiencia
del usuario.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# ══════════════════════════════════════════════════════════════
#  BASE DE DATOS
# ══════════════════════════════════════════════════════════════

DB_PATH = "tienda.db"


# ══════════════════════════════════════════════════════════════
# FUNCIÓN: INICIALIZAR BASE DE DATOS
# ══════════════════════════════════════════════════════════════
#
# ENTRADA:
# No recibe parámetros.
#
# PROCESO:
# - Crea la base de datos SQLite.
# - Genera la tabla productos si no existe.
#
# SALIDA:
# - Base de datos lista para utilizar.
#

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre   TEXT    NOT NULL,
            precio   REAL    NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ── CRUD productos ────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════
# FUNCIÓN: AGREGAR PRODUCTO
# ══════════════════════════════════════════════════════════════
#
# ENTRADA:
# - Nombre
# - Precio
# - Cantidad
#
# PROCESO:
# - Inserta un producto en la base de datos.
#
# SALIDA:
# - Producto almacenado correctamente.
#
def db_agregar(nombre, precio, cantidad):
    conn = db_conn()
    conn.execute(
        "INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)",
        (nombre, float(precio), int(cantidad))
    )
    conn.commit()
    conn.close()

def db_editar(pid, nombre, precio, cantidad):
    conn = db_conn()
    conn.execute(
        "UPDATE productos SET nombre=?, precio=?, cantidad=? WHERE id=?",
        (nombre, float(precio), int(cantidad), pid)
    )
    conn.commit()
    conn.close()

def db_eliminar(pid):
    conn = db_conn()
    conn.execute("DELETE FROM productos WHERE id=?", (pid,))
    conn.commit()
    conn.close()

def db_listar(busqueda=""):
    conn = db_conn()
    if busqueda:
        rows = conn.execute(
            "SELECT * FROM productos WHERE nombre LIKE ? ORDER BY nombre",
            (f"%{busqueda}%",)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM productos ORDER BY nombre").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def db_descontar_stock(pid, cantidad):
    conn = db_conn()
    conn.execute(
        "UPDATE productos SET cantidad = cantidad - ? WHERE id=?",
        (cantidad, pid)
    )
    conn.commit()
    conn.close()

def db_restaurar_stock(pid, cantidad):
    conn = db_conn()
    conn.execute(
        "UPDATE productos SET cantidad = cantidad + ? WHERE id=?",
        (cantidad, pid)
    )
    conn.commit()
    conn.close()

# ══════════════════════════════════════════════════════════════
#  ESTILOS / PALETA
# ══════════════════════════════════════════════════════════════

C = {
    "bg":         "#F5F7FA",
    "surface":    "#FFFFFF",
    "blue":       "#1565C0",
    "blue_light": "#1976D2",
    "blue_pale":  "#E3F0FF",
    "yellow":     "#F9A825",
    "red":        "#C62828",
    "red_light":  "#FFEBEE",
    "green":      "#2E7D32",
    "green_light":"#E8F5E9",
    "border":     "#D8DEE9",
    "text":       "#1A2533",
    "muted":      "#6B7A8D",
    "white":      "#FFFFFF",
}

FONT_TITLE  = ("Segoe UI", 13, "bold")
FONT_HEADER = ("Segoe UI", 10, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_BIG    = ("Segoe UI", 18, "bold")
FONT_MONO   = ("Consolas", 10)

# ══════════════════════════════════════════════════════════════
#  WIDGETS HELPER
# ══════════════════════════════════════════════════════════════

def make_btn(parent, text, command, color=None, fg="white", width=None):
    bg = color or C["blue"]
    kw = dict(text=text, command=command, bg=bg, fg=fg,
              font=FONT_HEADER, relief="flat", cursor="hand2",
              padx=14, pady=7, bd=0)
    if width:
        kw["width"] = width
    b = tk.Button(parent, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=_darken(bg)))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b

def _darken(hex_color):
    """Oscurece un color hex un poco para hover."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    r, g, b = max(0,r-25), max(0,g-25), max(0,b-25)
    return f"#{r:02x}{g:02x}{b:02x}"

def make_entry(parent, textvariable=None, width=22, placeholder=""):
    e = tk.Entry(parent, textvariable=textvariable, width=width,
                 font=FONT_BODY, relief="flat", bg=C["surface"],
                 fg=C["text"], insertbackground=C["blue"],
                 highlightthickness=1, highlightbackground=C["border"],
                 highlightcolor=C["blue"])
    return e

def make_label(parent, text, bold=False, color=None, size=10):
    font = ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)
    return tk.Label(parent, text=text, bg=C["bg"],
                    fg=color or C["text"], font=font)

def card(parent, **kw):
    """Frame con apariencia de card blanca con borde."""
    f = tk.Frame(parent, bg=C["surface"], relief="flat",
                 highlightthickness=1, highlightbackground=C["border"], **kw)
    return f

def section_title(parent, text):
    f = tk.Frame(parent, bg=C["surface"])
    tk.Label(f, text=text, font=FONT_TITLE, bg=C["surface"],
             fg=C["blue"]).pack(side="left")
    tk.Frame(f, bg=C["yellow"], height=3).pack(
        side="bottom", fill="x", pady=(4,0))
    return f

# ══════════════════════════════════════════════════════════════
#  APLICACIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
# CLASE PRINCIPAL DEL SISTEMA
# ══════════════════════════════════════════════════════════════
#
# RESPONSABILIDAD:
# - Controlar toda la aplicación.
# - Construir interfaz gráfica.
# - Administrar módulos de caja y catálogo.
#
class PuntoDeVenta(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Punto de Venta")
        self.geometry("1100x680")
        self.minsize(900, 580)
        self.configure(bg=C["bg"])
        self.resizable(True, True)

        init_db()
        self._build_ui()

    # ── UI principal ──────────────────────────────────────────

    
    # ══════════════════════════════════════════════════════════
    # FUNCIÓN: CONSTRUIR INTERFAZ GRÁFICA
    # ══════════════════════════════════════════════════════════
    #
    # ENTRADA:
    # No recibe parámetros.
    #
    # PROCESO:
    # - Construye ventanas, botones y pestañas.
    # - Inicializa módulos visuales.
    #
    # SALIDA:
    # - Interfaz gráfica funcional.
    #
    def _build_ui(self):
        # Topbar
        topbar = tk.Frame(self, bg=C["blue"], height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="★  Punto de Venta",
                 font=("Segoe UI", 16, "bold"),
                 bg=C["blue"], fg=C["white"]).pack(side="left", padx=20, pady=10)

        # Tabs
        self.tab_var = tk.StringVar(value="caja")
        for label, val in [("🧾  Caja", "caja"), ("📦  Catálogo", "catalogo")]:
            b = tk.Button(topbar, text=label,
                          command=lambda v=val: self._switch_tab(v),
                          font=("Segoe UI", 10, "bold"),
                          relief="flat", cursor="hand2",
                          padx=18, pady=14, bd=0)
            b.pack(side="left")
            b._tab_val = val
            b._tab_btn = True

        # Guardar referencias a botones de tab
        self._tab_buttons = [w for w in topbar.winfo_children()
                             if isinstance(w, tk.Button)]

        # Contenedor de páginas
        self.pages = tk.Frame(self, bg=C["bg"])
        self.pages.pack(fill="both", expand=True, padx=16, pady=14)

        self.page_caja     = tk.Frame(self.pages, bg=C["bg"])
        self.page_catalogo = tk.Frame(self.pages, bg=C["bg"])

        self._build_caja(self.page_caja)
        self._build_catalogo(self.page_catalogo)

        self._switch_tab("caja")

    def _switch_tab(self, val):
        self.tab_var.set(val)
        for b in self._tab_buttons:
            if b._tab_val == val:
                b.config(bg=C["yellow"], fg=C["text"])
            else:
                b.config(bg=C["blue"], fg=C["white"])

        self.page_caja.pack_forget()
        self.page_catalogo.pack_forget()

        if val == "caja":
            self.page_caja.pack(fill="both", expand=True)
            self._caja_actualizar_lista_desplegable()
        else:
            self.page_catalogo.pack(fill="both", expand=True)
            self._catalogo_cargar()

    # ══════════════════════════════════════════════════════════
    #  PÁGINA: CAJA
    # ══════════════════════════════════════════════════════════

    def _build_caja(self, parent):
        parent.columnconfigure(0, weight=3)
        parent.columnconfigure(1, weight=2)
        parent.rowconfigure(0, weight=1)

        # ── Panel izquierdo: búsqueda + ticket ────────────────
        left = tk.Frame(parent, bg=C["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)

        # Card búsqueda
        c_busq = card(left)
        c_busq.grid(row=0, column=0, sticky="ew", pady=(0,10))

        tk.Label(c_busq, text="Agregar producto a la venta",
                 font=FONT_TITLE, bg=C["surface"], fg=C["blue"]).pack(
                 anchor="w", padx=14, pady=(12,6))
        tk.Frame(c_busq, bg=C["yellow"], height=2).pack(fill="x", padx=14)

        busq_row = tk.Frame(c_busq, bg=C["surface"])
        busq_row.pack(fill="x", padx=14, pady=10)

        # Búsqueda por texto
        tk.Label(busq_row, text="Buscar:", font=FONT_BODY,
                 bg=C["surface"], fg=C["muted"]).grid(row=0, column=0, sticky="w")
        self.caja_busq_var = tk.StringVar()
        self.caja_busq_var.trace_add("write", self._caja_filtrar)
        self.caja_busq_entry = make_entry(busq_row, self.caja_busq_var, width=24)
        self.caja_busq_entry.grid(row=0, column=1, padx=(6,10))

        # Lista desplegable
        tk.Label(busq_row, text="Producto:", font=FONT_BODY,
                 bg=C["surface"], fg=C["muted"]).grid(row=0, column=2, sticky="w")
        self.caja_combo_var = tk.StringVar()
        self.caja_combo = ttk.Combobox(busq_row, textvariable=self.caja_combo_var,
                                        width=22, font=FONT_BODY, state="readonly")
        self.caja_combo.grid(row=0, column=3, padx=(6,10))
        self.caja_combo.bind("<<ComboboxSelected>>", self._caja_combo_seleccionar)

        # Cantidad
        tk.Label(busq_row, text="Cant.:", font=FONT_BODY,
                 bg=C["surface"], fg=C["muted"]).grid(row=0, column=4, sticky="w")
        self.caja_cant_var = tk.StringVar(value="1")
        cant_e = make_entry(busq_row, self.caja_cant_var, width=5)
        cant_e.grid(row=0, column=5, padx=(6,10))

        make_btn(busq_row, "＋ Agregar", self._caja_agregar_item).grid(
            row=0, column=6, padx=(4,0))

        self.caja_busq_msg = tk.Label(c_busq, text="", font=FONT_SMALL,
                                       bg=C["surface"], fg=C["red"])
        self.caja_busq_msg.pack(anchor="w", padx=14, pady=(0,8))

        # Card ticket
        c_ticket = card(left)
        c_ticket.grid(row=1, column=0, sticky="nsew")
        c_ticket.rowconfigure(1, weight=1)
        c_ticket.columnconfigure(0, weight=1)

        tk.Label(c_ticket, text="Ticket de venta",
                 font=FONT_TITLE, bg=C["surface"], fg=C["blue"]).grid(
                 row=0, column=0, sticky="w", padx=14, pady=(12,4))
        tk.Frame(c_ticket, bg=C["yellow"], height=2).grid(
            row=0, column=0, sticky="sew", padx=14, pady=(36,0))

        # Tabla ticket
        cols = ("#", "Producto", "P. Unit.", "Cant.", "Subtotal", "")
        self.ticket_tree = ttk.Treeview(c_ticket, columns=cols,
                                         show="headings", height=12)
        widths = [30, 220, 90, 60, 90, 60]
        for col, w in zip(cols, widths):
            self.ticket_tree.heading(col, text=col)
            self.ticket_tree.column(col, width=w, anchor="center" if col not in ("Producto",) else "w")
        self.ticket_tree.column("Producto", anchor="w")

        self._style_tree(self.ticket_tree)
        self.ticket_tree.grid(row=1, column=0, sticky="nsew", padx=14, pady=(6,0))

        sb = ttk.Scrollbar(c_ticket, orient="vertical",
                           command=self.ticket_tree.yview)
        self.ticket_tree.configure(yscroll=sb.set)
        sb.grid(row=1, column=1, sticky="ns", pady=(6,0))

        # Botón quitar del ticket
        make_btn(c_ticket, "✕ Quitar seleccionado",
                 self._caja_quitar_item,
                 color=C["red"], width=20).grid(
                 row=2, column=0, sticky="w", padx=14, pady=8)

        # Datos internos del ticket
        self._ticket_items = []   # lista de dicts {id, nombre, precio, cantidad}

        # ── Panel derecho: resumen + cobro ────────────────────
        right = tk.Frame(parent, bg=C["bg"])
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)

        c_res = card(right)
        c_res.pack(fill="both", expand=True)
        c_res.columnconfigure(0, weight=1)
        c_res.columnconfigure(1, weight=1)

        tk.Label(c_res, text="Resumen de venta",
                 font=FONT_TITLE, bg=C["surface"], fg=C["blue"]).grid(
                 row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(14,4))
        tk.Frame(c_res, bg=C["yellow"], height=2).grid(
            row=0, column=0, columnspan=2, sticky="sew", padx=16, pady=(40,0))

        # Filas de resumen
        def res_row(row, label, var, big=False):
            font = FONT_BIG if big else FONT_BODY
            color = C["blue"] if big else C["text"]
            tk.Label(c_res, text=label, font=FONT_BODY if not big else FONT_HEADER,
                     bg=C["surface"], fg=C["muted"]).grid(
                     row=row, column=0, sticky="w", padx=16, pady=4)
            tk.Label(c_res, textvariable=var, font=font,
                     bg=C["surface"], fg=color).grid(
                     row=row, column=1, sticky="e", padx=16, pady=4)

        self.r_articulos = tk.StringVar(value="0")
        self.r_total     = tk.StringVar(value="$0.00")
        self.r_cambio    = tk.StringVar(value="—")

        res_row(1, "Artículos:",  self.r_articulos)
        tk.Frame(c_res, bg=C["border"], height=1).grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=16)
        res_row(3, "TOTAL:", self.r_total, big=True)

        # Separador
        tk.Frame(c_res, bg=C["border"], height=1).grid(
            row=4, column=0, columnspan=2, sticky="ew", padx=16, pady=6)

        # Cobro
        tk.Label(c_res, text="Pago del cliente ($):",
                 font=FONT_HEADER, bg=C["surface"], fg=C["text"]).grid(
                 row=5, column=0, columnspan=2, sticky="w", padx=16, pady=(6,2))

        self.pago_var = tk.StringVar()
        pago_e = make_entry(c_res, self.pago_var, width=16)
        pago_e.grid(row=6, column=0, columnspan=2, sticky="ew", padx=16, pady=(0,8))
        pago_e.bind("<KeyRelease>", lambda e: self._caja_calcular_cambio())

        make_btn(c_res, "💰  Calcular cambio",
                 self._caja_calcular_cambio).grid(
                 row=7, column=0, columnspan=2, sticky="ew", padx=16, pady=(0,6))

        # Cambio
        tk.Label(c_res, text="Cambio a devolver:",
                 font=FONT_HEADER, bg=C["surface"], fg=C["text"]).grid(
                 row=8, column=0, sticky="w", padx=16)
        tk.Label(c_res, textvariable=self.r_cambio,
                 font=("Segoe UI", 22, "bold"),
                 bg=C["surface"], fg=C["green"]).grid(
                 row=8, column=1, sticky="e", padx=16)

        tk.Frame(c_res, bg=C["border"], height=1).grid(
            row=9, column=0, columnspan=2, sticky="ew", padx=16, pady=10)

        make_btn(c_res, "✔  Cobrar y nueva venta",
                 self._caja_cobrar,
                 color=C["green"]).grid(
                 row=10, column=0, columnspan=2, sticky="ew", padx=16, pady=(0,6))

        make_btn(c_res, "🗑  Limpiar ticket",
                 self._caja_limpiar,
                 color=C["red"]).grid(
                 row=11, column=0, columnspan=2, sticky="ew", padx=16, pady=(0,14))

    # ── Lógica Caja ───────────────────────────────────────────

    def _caja_actualizar_lista_desplegable(self):
        prods = db_listar()
        self._caja_prods_cache = {p["nombre"]: p for p in prods}
        nombres = [p["nombre"] for p in prods]
        self.caja_combo["values"] = nombres

    def _caja_filtrar(self, *args):
        busq  = self.caja_busq_var.get().strip()
        prods = db_listar(busq)
        self._caja_prods_cache = {p["nombre"]: p for p in prods}
        self.caja_combo["values"] = [p["nombre"] for p in prods]
        if prods:
            self.caja_combo.current(0)

    def _caja_combo_seleccionar(self, event):
        self.caja_busq_msg.config(text="")

    def _caja_agregar_item(self):
        nombre = self.caja_combo_var.get().strip()
        if not nombre:
            self.caja_busq_msg.config(text="⚠ Selecciona un producto.")
            return

        prod = self._caja_prods_cache.get(nombre)
        if not prod:
            self.caja_busq_msg.config(text="⚠ Producto no encontrado.")
            return

        try:
            cant = int(self.caja_cant_var.get())
            if cant <= 0:
                raise ValueError
        except ValueError:
            self.caja_busq_msg.config(text="⚠ Cantidad debe ser un número entero positivo.")
            return

        if prod["cantidad"] < cant:
            self.caja_busq_msg.config(
                text=f"⚠ Stock insuficiente (disponible: {prod['cantidad']}).")
            return

        # Si ya está en el ticket, sumar cantidad
        for item in self._ticket_items:
            if item["id"] == prod["id"]:
                nueva = item["cantidad"] + cant
                if prod["cantidad"] < nueva:
                    self.caja_busq_msg.config(
                        text=f"⚠ Stock insuficiente (disponible: {prod['cantidad']}).")
                    return
                item["cantidad"] = nueva
                self._caja_render_ticket()
                self.caja_busq_msg.config(text="")
                return

        self._ticket_items.append({
            "id":       prod["id"],
            "nombre":   prod["nombre"],
            "precio":   prod["precio"],
            "cantidad": cant,
        })
        self._caja_render_ticket()
        self.caja_busq_msg.config(text="")
        self.caja_cant_var.set("1")

    def _caja_render_ticket(self):
        for row in self.ticket_tree.get_children():
            self.ticket_tree.delete(row)

        total     = 0
        articulos = 0
        for i, item in enumerate(self._ticket_items, 1):
            sub = item["precio"] * item["cantidad"]
            total     += sub
            articulos += item["cantidad"]
            self.ticket_tree.insert("", "end", iid=str(item["id"]), values=(
                i,
                item["nombre"],
                f"${item['precio']:.2f}",
                item["cantidad"],
                f"${sub:.2f}",
                "✕"
            ))

        self.r_articulos.set(str(articulos))
        self.r_total.set(f"${total:.2f}")
        self.r_cambio.set("—")
        self.pago_var.set("")

    def _caja_quitar_item(self):
        sel = self.ticket_tree.selection()
        if not sel:
            messagebox.showinfo("Atención", "Selecciona un producto del ticket primero.")
            return
        iid = int(sel[0])
        self._ticket_items = [i for i in self._ticket_items if i["id"] != iid]
        self._caja_render_ticket()

    def _caja_calcular_cambio(self):
        try:
            pago = float(self.pago_var.get())
        except ValueError:
            self.r_cambio.set("—")
            return

        total_str = self.r_total.get().replace("$", "")
        try:
            total = float(total_str)
        except ValueError:
            return

        if total == 0:
            self.r_cambio.set("—")
            return

        cambio = pago - total
        if cambio < 0:
            self.r_cambio.set(f"−${abs(cambio):.2f}  ⚠")
        else:
            self.r_cambio.set(f"${cambio:.2f}")

    
    # ══════════════════════════════════════════════════════════
    # FUNCIÓN: COBRAR VENTA
    # ══════════════════════════════════════════════════════════
    #
    # ENTRADA:
    # - Productos en ticket
    # - Pago del cliente
    #
    # PROCESO:
    # - Verifica pago suficiente.
    # - Descuenta stock.
    # - Calcula cambio.
    #
    # SALIDA:
    # - Venta completada.
    #
    def _caja_cobrar(self):
        if not self._ticket_items:
            messagebox.showinfo("Atención", "El ticket está vacío.")
            return

        try:
            pago = float(self.pago_var.get())
        except ValueError:
            messagebox.showwarning("Atención", "Ingresa el monto recibido del cliente.")
            return

        total_str = self.r_total.get().replace("$", "")
        total = float(total_str)

        if pago < total:
            messagebox.showwarning("Pago insuficiente",
                f"El pago (${pago:.2f}) es menor al total (${total:.2f}).")
            return

        # Descontar stock
        for item in self._ticket_items:
            db_descontar_stock(item["id"], item["cantidad"])

        cambio = pago - total
        messagebox.showinfo("✔ Venta realizada",
            f"Total:   ${total:.2f}\n"
            f"Pago:    ${pago:.2f}\n"
            f"Cambio:  ${cambio:.2f}\n\n"
            f"¡Gracias por su compra!")

        self._caja_limpiar()
        self._caja_actualizar_lista_desplegable()

    def _caja_limpiar(self):
        self._ticket_items = []
        self._caja_render_ticket()
        self.pago_var.set("")
        self.r_cambio.set("—")

    # ══════════════════════════════════════════════════════════
    #  PÁGINA: CATÁLOGO
    # ══════════════════════════════════════════════════════════

    def _build_catalogo(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=2)
        parent.rowconfigure(0, weight=1)

        # ── Formulario ────────────────────────────────────────
        c_form = card(parent)
        c_form.grid(row=0, column=0, sticky="nsew", padx=(0,10))

        tk.Label(c_form, text="Producto",
                 font=FONT_TITLE, bg=C["surface"], fg=C["blue"]).pack(
                 anchor="w", padx=16, pady=(14,2))
        tk.Frame(c_form, bg=C["yellow"], height=2).pack(fill="x", padx=16, pady=(0,12))

        self._form_modo  = "agregar"   # o "editar"
        self._form_pid   = None

        fields_frame = tk.Frame(c_form, bg=C["surface"])
        fields_frame.pack(fill="x", padx=16)

        def field(label, var, tipo="text"):
            tk.Label(fields_frame, text=label, font=FONT_SMALL,
                     bg=C["surface"], fg=C["muted"]).pack(anchor="w", pady=(8,2))
            e = make_entry(fields_frame, var, width=28)
            e.pack(fill="x")
            return e

        self.f_nombre   = tk.StringVar()
        self.f_precio   = tk.StringVar()
        self.f_cantidad = tk.StringVar()

        field("Nombre del producto", self.f_nombre)
        field("Precio ($)",          self.f_precio)
        field("Cantidad en stock",   self.f_cantidad)

        self.form_msg = tk.Label(c_form, text="", font=FONT_SMALL,
                                  bg=C["surface"], fg=C["red"], wraplength=220)
        self.form_msg.pack(anchor="w", padx=16, pady=(10,4))

        self.btn_guardar = make_btn(c_form, "💾  Guardar producto",
                                    self._catalogo_guardar)
        self.btn_guardar.pack(fill="x", padx=16, pady=(0,6))

        self.btn_cancelar = make_btn(c_form, "✖  Cancelar edición",
                                      self._catalogo_cancelar,
                                      color="#607D8B")
        self.btn_cancelar.pack(fill="x", padx=16, pady=(0,14))
        self.btn_cancelar.pack_forget()   # oculto al inicio

        # ── Tabla catálogo ────────────────────────────────────
        c_tabla = card(parent)
        c_tabla.grid(row=0, column=1, sticky="nsew")
        c_tabla.rowconfigure(2, weight=1)
        c_tabla.columnconfigure(0, weight=1)

        # Cabecera con búsqueda
        head = tk.Frame(c_tabla, bg=C["surface"])
        head.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(14,4))

        tk.Label(head, text="Catálogo de productos",
                 font=FONT_TITLE, bg=C["surface"], fg=C["blue"]).pack(side="left")

        self.cat_busq_var = tk.StringVar()
        self.cat_busq_var.trace_add("write", lambda *a: self._catalogo_cargar())
        busq_e = make_entry(head, self.cat_busq_var, width=18)
        busq_e.pack(side="right")
        tk.Label(head, text="🔍", font=FONT_BODY,
                 bg=C["surface"]).pack(side="right", padx=(0,4))

        tk.Frame(c_tabla, bg=C["yellow"], height=2).grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=16)

        cols = ("Nombre", "Precio", "Stock", "Editar", "Eliminar")
        self.cat_tree = ttk.Treeview(c_tabla, columns=cols,
                                      show="headings", height=18)
        widths = [250, 100, 80, 80, 80]
        for col, w in zip(cols, widths):
            self.cat_tree.heading(col, text=col)
            self.cat_tree.column(col, width=w,
                                  anchor="w" if col == "Nombre" else "center")

        self._style_tree(self.cat_tree)
        self.cat_tree.grid(row=2, column=0, sticky="nsew", padx=16, pady=(8,0))
        self.cat_tree.bind("<ButtonRelease-1>", self._catalogo_click)

        sb2 = ttk.Scrollbar(c_tabla, orient="vertical",
                             command=self.cat_tree.yview)
        self.cat_tree.configure(yscroll=sb2.set)
        sb2.grid(row=2, column=1, sticky="ns", pady=(8,0))

        # Mapa de IDs por fila
        self._cat_ids = {}

    # ── Lógica Catálogo ───────────────────────────────────────

    def _catalogo_cargar(self):
        busq = self.cat_busq_var.get().strip()
        prods = db_listar(busq)

        for row in self.cat_tree.get_children():
            self.cat_tree.delete(row)

        self._cat_ids = {}
        for p in prods:
            iid = self.cat_tree.insert("", "end", values=(
                p["nombre"],
                f"${p['precio']:.2f}",
                p["cantidad"],
                "✏ Editar",
                "✕ Eliminar"
            ))
            self._cat_ids[iid] = p

    def _catalogo_click(self, event):
        region = self.cat_tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        col  = self.cat_tree.identify_column(event.x)
        iid  = self.cat_tree.identify_row(event.y)
        prod = self._cat_ids.get(iid)
        if not prod:
            return

        if col == "#4":   # Editar
            self._catalogo_editar(prod)
        elif col == "#5": # Eliminar
            self._catalogo_eliminar(prod)

    
    # ══════════════════════════════════════════════════════════
    # FUNCIÓN: GUARDAR PRODUCTO
    # ══════════════════════════════════════════════════════════
    #
    # ENTRADA:
    # - Nombre
    # - Precio
    # - Cantidad
    #
    # PROCESO:
    # - Valida datos.
    # - Guarda o actualiza productos.
    #
    # SALIDA:
    # - Catálogo actualizado.
    #
    def _catalogo_guardar(self):
        nombre   = self.f_nombre.get().strip()
        precio   = self.f_precio.get().strip()
        cantidad = self.f_cantidad.get().strip()

        if not nombre or not precio or not cantidad:
            self.form_msg.config(text="⚠ Completa todos los campos.", fg=C["red"])
            return
        try:
            p = float(precio)
            q = int(cantidad)
            if p < 0 or q < 0:
                raise ValueError
        except ValueError:
            self.form_msg.config(text="⚠ Precio y cantidad deben ser números positivos.", fg=C["red"])
            return

        if self._form_modo == "agregar":
            db_agregar(nombre, p, q)
            self.form_msg.config(text="✔ Producto agregado.", fg=C["green"])
        else:
            db_editar(self._form_pid, nombre, p, q)
            self.form_msg.config(text="✔ Producto actualizado.", fg=C["green"])
            self._catalogo_cancelar()

        self.f_nombre.set("")
        self.f_precio.set("")
        self.f_cantidad.set("")
        self._catalogo_cargar()
        self.after(2500, lambda: self.form_msg.config(text=""))

    def _catalogo_editar(self, prod):
        self._form_modo = "editar"
        self._form_pid  = prod["id"]
        self.f_nombre.set(prod["nombre"])
        self.f_precio.set(str(prod["precio"]))
        self.f_cantidad.set(str(prod["cantidad"]))
        self.btn_cancelar.pack(fill="x", padx=16, pady=(0,14))
        self.form_msg.config(text="Modo edición activo.", fg=C["blue"])

    def _catalogo_cancelar(self):
        self._form_modo = "agregar"
        self._form_pid  = None
        self.f_nombre.set("")
        self.f_precio.set("")
        self.f_cantidad.set("")
        self.btn_cancelar.pack_forget()
        self.form_msg.config(text="")

    def _catalogo_eliminar(self, prod):
        ok = messagebox.askyesno("Confirmar",
            f"¿Eliminar '{prod['nombre']}' del catálogo?")
        if ok:
            db_eliminar(prod["id"])
            self._catalogo_cargar()

    # ── Estilo Treeview ───────────────────────────────────────

    def _style_tree(self, tree):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
            background=C["surface"],
            foreground=C["text"],
            rowheight=32,
            fieldbackground=C["surface"],
            font=FONT_BODY,
            borderwidth=0,
        )
        style.configure("Treeview.Heading",
            background=C["blue"],
            foreground="white",
            font=FONT_HEADER,
            relief="flat",
        )
        style.map("Treeview",
            background=[("selected", C["blue_pale"])],
            foreground=[("selected", C["blue"])],
        )
        style.map("Treeview.Heading",
            background=[("active", C["blue_light"])],
        )
        tree.tag_configure("odd",  background="#F8FAFD")
        tree.tag_configure("even", background=C["surface"])


# ══════════════════════════════════════════════════════════════
#  ARRANQUE
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = PuntoDeVenta()
    app.mainloop()
