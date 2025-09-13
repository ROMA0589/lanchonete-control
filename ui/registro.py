# ui/registro.py
# Ventana de registro de entrada/salida para la lanchonete
import tkinter as tk
from tkinter import messagebox

class RegistroWindow(tk.Toplevel):
    def __init__(self, master, tipo, guardar_registro, favicon):
        super().__init__(master)
        self.title(f'Registrar {tipo.capitalize()}')
        self.geometry('370x350')
        self.configure(bg='#23272A')
        try:
            self.iconbitmap(favicon)
        except Exception:
            pass
        style_label = {'font': ('Arial', 11, 'bold'), 'bg': '#23272A', 'fg': '#99AAB5'}
        style_entry = {'font': ('Arial', 11), 'bg': '#2C2F33', 'fg': '#99AAB5', 'insertbackground': '#99AAB5'}
        tk.Label(self, text='Descrição:', **style_label).pack(pady=5)
        self.descricao = tk.Entry(self, width=40, **style_entry)
        self.descricao.pack(pady=5)
        tk.Label(self, text='Valor (R$):', **style_label).pack(pady=5)
        self.valor = tk.Entry(self, width=40, **style_entry)
        self.valor.pack(pady=5)
        tk.Label(self, text='Material (opcional):', **style_label).pack(pady=5)
        self.material = tk.Entry(self, width=40, **style_entry)
        self.material.pack(pady=5)
        tk.Label(self, text='Responsável:', **style_label).pack(pady=5)
        self.responsavel = tk.Entry(self, width=40, **style_entry)
        self.responsavel.pack(pady=5)
        tk.Button(self, text='Salvar', command=self.guardar, font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', activebackground='#388E3C', activeforeground='white', bd=0).pack(pady=18)
        self.tipo = tipo
        self.guardar_registro = guardar_registro
    def guardar(self):
        desc = self.descricao.get()
        val = self.valor.get()
        mat = self.material.get()
        resp = self.responsavel.get()
        if not desc or not val or not resp:
            messagebox.showerror('Erro', 'Descrição, valor e responsável são obrigatórios.')
            return
        try:
            float(val)
        except ValueError:
            messagebox.showerror('Erro', 'O valor deve ser um número.')
            return
        self.guardar_registro(self.tipo, desc, val, mat, resp)
        messagebox.showinfo('Sucesso', 'Registro salvo com sucesso.')
        self.destroy()
