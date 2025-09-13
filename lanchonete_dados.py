import csv
from datetime import datetime
import os


from ui.constantes import ARQUIVO, CAMPOS
# Inicializa el archivo CSV si no existe
def inicializar_csv():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CAMPOS)
            writer.writeheader()

# Guarda un registro en el CSV
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

# Obtiene todos los registros del CSV
def obter_historico():
    registros = []
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                registros.append(row)
    return registros
