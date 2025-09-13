from lanchonete_dados import inicializar_csv, guardar_registro, obter_historico
from ui.constantes import CAMPOS, ERRO_DIA_NAO_INICIADO, FORMATO_REAIS, TITULO_LANCHONETE, FAVICON, DIA_NAO_INICIADO
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITULO_LANCHONETE)
        self.geometry('650x420')
        self.resizable(False, False)
        try:
            self.iconbitmap(FAVICON)
        except Exception:
            pass
        inicializar_csv()
        self.dia_iniciado = False
        self.data_dia = None
        self.criar_widgets()

    def criar_widgets(self):
        self.configure(bg='#23272A')
        style_btn = {
            'font': ('Arial', 12, 'bold'),
            'bg': '#23272A',
            'fg': 'white',
            'activebackground': '#2C2F33',
            'activeforeground': 'white',
            'bd': 3,
            'relief': 'raised',
            'highlightthickness': 2,
            'highlightbackground': '#99AAB5'
        }
        frame1 = tk.Frame(self, bg='#23272A')
        frame1.pack(pady=10, fill="x", expand=False)
        frame2 = tk.Frame(self, bg='#23272A')
        frame2.pack(pady=5, fill="x", expand=False)
        btns = []
        # Tres botones arriba
        btn_comecar = tk.Button(frame1, text='Começar Dia', width=15, command=self.comecar_dia, **style_btn)
        btn_comecar.grid(row=0, column=0, padx=8, pady=4)
        btns.append(btn_comecar)
        btn_fechar = tk.Button(frame1, text='Fechar Dia', width=15, command=self.fechar_dia, **style_btn)
        btn_fechar.grid(row=0, column=1, padx=8, pady=4)
        btns.append(btn_fechar)
        btn_historico = tk.Button(frame1, text='Ver Histórico', width=15, command=self.janela_historico, **style_btn)
        btn_historico.grid(row=0, column=2, padx=8, pady=4)
        btns.append(btn_historico)
        # Dos botones juntos debajo del estado
        btn_entrada = tk.Button(frame2, text='Registrar Entrada', width=15, command=self.janela_registro_entrada, **style_btn)
        btn_entrada.grid(row=0, column=0, padx=8, pady=4)
        btns.append(btn_entrada)
        btn_saida = tk.Button(frame2, text='Registrar Saída', width=15, command=self.janela_registro_saida, **style_btn)
        btn_saida.grid(row=0, column=1, padx=8, pady=4)
        btns.append(btn_saida)
        # Animación hover para todos los botones
        def on_enter(e):
            e.widget['bg'] = '#99AAB5'
            e.widget['font'] = ('Arial', 13, 'bold')
            e.widget['highlightbackground'] = '#FFD700'
        def on_leave(e):
            e.widget['bg'] = '#23272A'
            e.widget['font'] = ('Arial', 12, 'bold')
            e.widget['highlightbackground'] = '#99AAB5'
        for b in btns:
            b.bind('<Enter>', on_enter)
            b.bind('<Leave>', on_leave)
        self.lbl_estado = tk.Label(self, text=DIA_NAO_INICIADO, fg='#99AAB5', font=('Arial', 13, 'bold'), bg='#23272A')
        self.lbl_estado.pack(pady=10)
        titulo = tk.Label(self, text=TITULO_LANCHONETE, font=('Arial', 20, 'bold'), fg='#99AAB5', bg='#23272A')
        titulo.pack(pady=5)
    def comecar_dia(self):
        if self.dia_iniciado:
            messagebox.showinfo('Info', 'O dia já foi iniciado.')
            return
        self.dia_iniciado = True
        self.data_dia = datetime.now().strftime('%d/%m/%Y')
        self.lbl_estado.config(text=f'Dia iniciado: {self.data_dia}', fg='green')
        messagebox.showinfo('Dia iniciado', f'Dia {self.data_dia} iniciado.')

    def fechar_dia(self):
        if not self.dia_iniciado or self.data_dia is None:
            messagebox.showerror('Erro', ERRO_DIA_NAO_INICIADO)
            return
        from ui.exportacao import exportar_excel, resumo_dia
        resumo = resumo_dia(self.data_dia, obter_historico)
        try:
            nome_arquivo = exportar_excel(self.data_dia, obter_historico)
            msg_excel = f"Arquivo Excel criado: {nome_arquivo}"
        except Exception as e:
            msg_excel = f"Erro ao exportar Excel: {e}"
        self.dia_iniciado = False
        self.data_dia = None
        self.lbl_estado.config(text=DIA_NAO_INICIADO, fg='red')
        messagebox.showinfo('Fechamento do Dia', resumo + "\n\n" + msg_excel)

    # Las funciones exportar_excel y resumo_dia ahora están en ui/exportacao.py

    def janela_registro_entrada(self):
        if not self.dia_iniciado:
            messagebox.showerror('Erro', ERRO_DIA_NAO_INICIADO)
            return
        self.janela_registro('entrada')

    def janela_registro_saida(self):
        if not self.dia_iniciado:
            messagebox.showerror('Erro', ERRO_DIA_NAO_INICIADO)
            return
        self.janela_registro('saida')

    def janela_registro(self, tipo):
        from ui.registro import RegistroWindow
        RegistroWindow(self, tipo, guardar_registro, FAVICON)

    def janela_historico(self):
        from ui.historico import HistoricoWindow
        HistoricoWindow(self, CAMPOS, obter_historico, FAVICON)

if __name__ == '__main__':
    app = App()
    app.mainloop()
import csv
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox

ARQUIVO = 'registros.csv'
CAMPOS = ['data', 'tipo', 'descricao', 'valor', 'material', 'responsavel']
ERRO_DIA_NAO_INICIADO = 'Você precisa começar o dia primeiro.'
FORMATO_REAIS = "R$ {:.2f}"

def inicializar_csv():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CAMPOS)
            writer.writeheader()

def guardar_registro(tipo, descricao, valor, material, responsavel):
    data = datetime.now().strftime('%d/%m/%Y %H:%M')
    with open(ARQUIVO, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writerow({
            'data': data,
            'tipo': tipo,
            'descricao': descricao,
            'valor': valor,
            'material': material,
            'responsavel': responsavel
        })

def obter_historico():
    registros = []
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                registros.append(row)
    return registros

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITULO_LANCHONETE)
        self.geometry('650x420')
        self.title(TITULO_LANCHONETE)
        self.geometry('650x420')
        self.resizable(False, False)
        # Agregar ícono personalizado (logo.ico)
        try:
            self.iconbitmap(FAVICON)
        except Exception:
            pass  # Si no existe el arquivo, não dá erro
        self.data_dia = None
        self.criar_widgets()

    def criar_widgets(self):
        self.configure(bg='#23272A')

        style_btn = {
            'font': ('Arial', 12, 'bold'),
            'bg': '#23272A',  # negro grisoso
            'fg': 'white',
            'activebackground': '#2C2F33',
            'activeforeground': 'white',
            'bd': 3,
            'relief': 'raised',
            'highlightthickness': 2,
            'highlightbackground': '#99AAB5'
        }

        frame1 = tk.Frame(self, bg='#23272A')
        frame1.pack(pady=10)
        frame2 = tk.Frame(self, bg='#23272A')
        frame2.pack(pady=5)

        btns = []
        btn_comecar = tk.Button(frame1, text='Começar Dia', width=15, command=self.comecar_dia, **style_btn)
        btn_comecar.grid(row=0, column=0, padx=8, pady=4)
        btns.append(btn_comecar)

        btn_fechar = tk.Button(frame1, text='Fechar Dia', width=15, command=self.fechar_dia, **style_btn)
        btn_fechar.grid(row=0, column=1, padx=8, pady=4)
        btns.append(btn_fechar)

        btn_entrada = tk.Button(frame2, text='Registrar Entrada', width=15, command=self.janela_registro_entrada, **style_btn)
        btn_entrada.grid(row=0, column=0, padx=8, pady=4)
        btns.append(btn_entrada)

        btn_saida = tk.Button(frame2, text='Registrar Saída', width=15, command=self.janela_registro_saida, **style_btn)
        btn_saida.grid(row=0, column=1, padx=8, pady=4)
        btns.append(btn_saida)

        btn_historico = tk.Button(frame2, text='Ver Histórico', width=15, command=self.janela_historico, **style_btn)
        btn_historico.grid(row=0, column=2, padx=8, pady=4)
        btns.append(btn_historico)

        # Animación hover para todos los botones
        def on_enter(e):
            e.widget['bg'] = '#99AAB5'
            e.widget['font'] = ('Arial', 13, 'bold')
            e.widget['highlightbackground'] = '#FFD700'
        def on_leave(e):
            e.widget['bg'] = '#23272A'
            e.widget['font'] = ('Arial', 12, 'bold')
            e.widget['highlightbackground'] = '#99AAB5'
        for b in btns:
            b.bind('<Enter>', on_enter)
            b.bind('<Leave>', on_leave)
        self.lbl_estado = tk.Label(self, text=DIA_NAO_INICIADO, fg='#99AAB5', font=('Arial', 13, 'bold'), bg='#23272A')
        self.lbl_estado.pack(pady=10)

    
        # Título con fuente grande y color
        titulo = tk.Label(self, text=TITULO_LANCHONETE, font=('Arial', 20, 'bold'), fg='#99AAB5', bg='#23272A')
        titulo.pack(pady=5)
        if self.dia_iniciado:
            messagebox.showinfo('Info', 'O dia já foi iniciado.')
            return
        self.dia_iniciado = True
        self.data_dia = datetime.now().strftime('%d/%m/%Y')
        self.lbl_estado.config(text=f'Dia iniciado: {self.data_dia}', fg='green')
        messagebox.showinfo('Dia iniciado', f'Dia {self.data_dia} iniciado.')

    def fechar_dia(self):
        if not self.dia_iniciado:
            messagebox.showerror('Erro', ERRO_DIA_NAO_INICIADO)
            return
        resumo = self.resumo_dia(self.data_dia)
        # Exportar a Excel
        try:
            self.exportar_excel(self.data_dia)
            msg_excel = f"Arquivo Excel criado: fechamento_{self.data_dia.replace('/', '-')}.xlsx"
        except Exception as e:
            msg_excel = f"Erro ao exportar Excel: {e}"
        self.dia_iniciado = False
        self.data_dia = None
        self.lbl_estado.config(text='Dia não iniciado', fg='red')
        messagebox.showinfo('Fechamento do Dia', resumo + "\n\n" + msg_excel)

    def exportar_excel(self, data):
        from openpyxl import Workbook
        registros = obter_historico()
        wb = Workbook()
        ws = wb.active
        ws.title = "Fechamento {}".format(data)
        # Título
        ws.append(["Fechamento do dia {}".format(data)])
        ws.append([""])
        # Resumo
        entradas = sum(float(r['valor']) for r in registros if r['tipo']=='entrada' and r['data'].startswith(data))
        saidas = sum(float(r['valor']) for r in registros if r['tipo']=='saida' and r['data'].startswith(data))
        saldo = entradas - saidas
        ws.append(["Entradas", FORMATO_REAIS.format(entradas)])
        ws.append(["Saídas", FORMATO_REAIS.format(saidas)])
        ws.append(["Saldo", FORMATO_REAIS.format(saldo)])
        ws.append([""])
        # Registros do dia
        ws.append(CAMPOS)
        for r in registros:
            if r['data'].startswith(data):
                ws.append([r.get(c, '') for c in CAMPOS])
        # Salvar arquivo
        nome_arquivo = "fechamento_{}.xlsx".format(data.replace('/', '-'))
        wb.save(nome_arquivo)

    def resumo_dia(self, data):
        registros = obter_historico()
        entradas = sum(float(r['valor']) for r in registros if r['tipo']=='entrada' and r['data'].startswith(data))
        saidas = sum(float(r['valor']) for r in registros if r['tipo']=='saida' and r['data'].startswith(data))
        saldo = entradas - saidas
        resumo = f"Resumo do dia {data}:\nEntradas: {FORMATO_REAIS.format(entradas)}\nSaídas: {FORMATO_REAIS.format(saidas)}\nSaldo: {FORMATO_REAIS.format(saldo)}"
        return resumo

    def janela_registro_entrada(self):
        if not self.dia_iniciado:
            messagebox.showerror('Erro', ERRO_DIA_NAO_INICIADO)
            return
        self.janela_registro('entrada')

    def janela_registro_saida(self):
        if not self.dia_iniciado:
            messagebox.showerror('Erro', ERRO_DIA_NAO_INICIADO)
            return
        self.janela_registro('saida')

    def janela_registro(self, tipo):
        win = tk.Toplevel(self)
        win.title(f'Registrar {tipo.capitalize()}')
        win.geometry('370x350')
        win.configure(bg='#23272A')
        try:
            win.iconbitmap(FAVICON)
        except Exception:
            pass

        style_label = {'font': ('Arial', 11, 'bold'), 'bg': '#23272A', 'fg': '#99AAB5'}
        style_entry = {'font': ('Arial', 11), 'bg': '#2C2F33', 'fg': '#99AAB5', 'insertbackground': '#99AAB5'}

        tk.Label(win, text='Descrição:', **style_label).pack(pady=5)
        descricao = tk.Entry(win, width=40, **style_entry)
        descricao.pack(pady=5)

        tk.Label(win, text='Valor (R$):', **style_label).pack(pady=5)
        valor = tk.Entry(win, width=40, **style_entry)
        valor.pack(pady=5)

        tk.Label(win, text='Material (opcional):', **style_label).pack(pady=5)
        material = tk.Entry(win, width=40, **style_entry)
        material.pack(pady=5)

        tk.Label(win, text='Responsável:', **style_label).pack(pady=5)
        responsavel = tk.Entry(win, width=40, **style_entry)
        responsavel.pack(pady=5)

        def guardar():
            desc = descricao.get()
            val = valor.get()
            mat = material.get()
            resp = responsavel.get()
            if not desc or not val or not resp:
                messagebox.showerror('Erro', 'Descrição, valor e responsável são obrigatórios.')
                return
            try:
                float(val)
            except ValueError:
                messagebox.showerror('Erro', 'O valor deve ser um número.')
                return
            guardar_registro(tipo, desc, val, mat, resp)
            messagebox.showinfo('Sucesso', 'Registro salvo com sucesso.')
            win.destroy()

        tk.Button(win, text='Salvar', command=guardar, font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', activebackground='#388E3C', activeforeground='white', bd=0).pack(pady=18)

    def janela_historico(self):
        win = tk.Toplevel(self)
        win.title('Histórico de Registros')
        win.geometry('600x350')
        try:
            win.iconbitmap('favicon.ico')
        except Exception:
            pass

        tree = ttk.Treeview(win, columns=CAMPOS, show='headings')
        for campo in CAMPOS:
            tree.heading(campo, text=campo.capitalize())
            tree.column(campo, width=100)
        tree.pack(fill='both', expand=True)

        registros = obter_historico()
        for reg in registros:
            # Si el registro no tiene el campo 'responsavel', mostrar vacío
            valores = [reg.get(c, '') for c in CAMPOS]
            tree.insert('', 'end', values=valores)

if __name__ == '__main__':
    app = App()
    app.mainloop()
