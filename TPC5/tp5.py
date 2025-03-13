import json
import re
from datetime import date

STOCK_FILE = "stock.json"

def carregar_stock():
    try:
        with open(STOCK_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_stock(stock):
    with open(STOCK_FILE, 'w') as file:
        json.dump(stock, file, indent=4)

def listar_produtos(stock):
    print("maq:\n cod | nome | quantidade | preço")
    print("---------------------------------")
    for produto in stock:
        print(f"{produto['cod']} {produto['nome']} {produto['quant']} {produto['preco']}€")

def verificar_moeda(moeda):
    return re.match(r'^[125]|10|20|50+[cC]$', moeda) or re.match(r'^[12]+[eE]$', moeda)

def processar_moedas(comando, saldo):
    moedas = re.findall(r'\b\d+[eEcC]?\b', comando)
    for moeda in moedas:
        if verificar_moeda(moeda):
            if moeda.endswith('E'):
                saldo += int(moeda.strip('E')) * 100
            elif moeda.endswith('C'):
                saldo += int(moeda.strip('C'))
        else:
            print("maq: Moeda inválida.")
    print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c")
    return saldo

def selecionar_produto(codigo, saldo, stock):
    for produto in stock:
        if produto["cod"] == codigo:
            if produto["quant"] == 0:
                print("maq: Produto esgotado.")
                return saldo
            preco = int(produto["preco"] * 100)
            if saldo < preco:
                print(f"maq: Saldo insuficiente para satisfazer o seu pedido")
                print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c; Pedido = {preco // 100}e{preco % 100}c")
                return saldo
            saldo -= preco
            produto["quant"] -= 1
            print(f"maq: Pode retirar o produto dispensado \"{produto['nome']}\"")
            print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c")
            return saldo
    print("maq: Produto inexistente.")
    return saldo

def calcular_troco(saldo):
    moedas = [200, 100, 50, 20, 10, 5, 2, 1]
    troco = {}
    for moeda in moedas:
        if saldo >= moeda:
            troco[moeda] = saldo // moeda
            saldo %= moeda
    return troco

def vending_machine():
    stock = carregar_stock()
    print(f"maq: {date.today()}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    saldo = 0

    while True:
        comando = input(">> ").upper()
        if comando == "LISTAR":
            listar_produtos(stock)
        elif comando.startswith("MOEDA"):
            saldo = processar_moedas(comando, saldo)
        elif comando.startswith("SELECIONAR"):
            partes = comando.split()
            if len(partes) < 2:
                print("maq: Comando inválido.")
                continue
            codigo = partes[1]
            saldo = selecionar_produto(codigo, saldo, stock)
        elif comando == "SAIR":
            troco = calcular_troco(saldo)
            troco_str = ", ".join(f"{v}x {k}c" for k, v in troco.items())
            print(f"maq: Pode retirar o troco: {troco_str}.")
            print("maq: Até à próxima")
            salvar_stock(stock)
            break
        else:
            print("maq: Comando inválido.")

if __name__ == "__main__":
    vending_machine()
