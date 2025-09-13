# ui/historico.py
# Ventana para mostrar el histórico de registros
import tkinter as tk
from tkinter import ttk

class HistoricoWindow(tk.Toplevel):
    def __init__(self, master, campos, obter_historico, favicon):
        super().__init__(master)
        self.title('Histórico de Registros')
        self.geometry('600x350')
        try:
            self.iconbitmap(favicon)
        except Exception:
            pass
        tree = ttk.Treeview(self, columns=campos, show='headings')
        for campo in campos:
            tree.heading(campo, text=campo.capitalize())
            tree.column(campo, width=100)
        tree.pack(fill='both', expand=True)
        registros = obter_historico()
        for reg in registros:
            valores = [reg.get(c, '') for c in campos]
            tree.insert('', 'end', values=valores)
