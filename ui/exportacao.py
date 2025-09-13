# ui/exportacao.py
# Funciones para exportar a Excel y resumen del día
from openpyxl import Workbook
from ui.constantes import FORMATO_REAIS, CAMPOS

def exportar_excel(data, obter_historico):
    registros = obter_historico()
    wb = Workbook()
    ws = wb.active
    ws.title = "Fechamento {}".format(data.replace('/', '-'))
    ws.append(["Fechamento do dia {}".format(data)])
    ws.append([""])
    entradas = sum(float(r['valor']) for r in registros if r['tipo']=='entrada' and r['data'].startswith(data))
    saidas = sum(float(r['valor']) for r in registros if r['tipo']=='saida' and r['data'].startswith(data))
    saldo = entradas - saidas
    ws.append(["Entradas", FORMATO_REAIS.format(entradas)])
    ws.append(["Saídas", FORMATO_REAIS.format(saidas)])
    ws.append(["Saldo", FORMATO_REAIS.format(saldo)])
    ws.append([""])
    ws.append(CAMPOS)
    for r in registros:
        if r['data'].startswith(data):
            ws.append([r.get(c, '') for c in CAMPOS])
    nome_arquivo = "fechamento_{}.xlsx".format(data.replace('/', '-'))
    wb.save(nome_arquivo)
    return nome_arquivo

def resumo_dia(data, obter_historico):
    registros = obter_historico()
    entradas = sum(float(r['valor']) for r in registros if r['tipo']=='entrada' and r['data'].startswith(data))
    saidas = sum(float(r['valor']) for r in registros if r['tipo']=='saida' and r['data'].startswith(data))
    saldo = entradas - saidas
    resumo = f"Resumo do dia {data}:\nEntradas: {FORMATO_REAIS.format(entradas)}\nSaídas: {FORMATO_REAIS.format(saidas)}\nSaldo: {FORMATO_REAIS.format(saldo)}"
    return resumo
