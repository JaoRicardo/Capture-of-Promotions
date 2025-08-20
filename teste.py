from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.error
import json
import time

url = "https://www.kabum.com.br/produto/782142/placa-de-video-msi-rtx-5070-12g-shadow-2x-oc-nvdia-geforce-12gb-gddr7-opengl-4-6-g-sync-g5070-12s2c"

while True:
    try:
        page = urlopen(url)
    except urllib.error.URLError:
        print("URL não existe ou está incorreta")
        print("Tentando reconexão em 25 min")
        time.sleep(4)
        continue

    html = page.read().decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    caixa = soup.find("div", class_="w-full p-8 rounded-8 border-solid border border-black-400")
    caixa2 = soup.find("div", class_="col-span-4 tablet:col-span-6 desktop:col-span-3 desktop:mt-16 order-1 desktop:order-2")
    nome_produto = caixa2.find_next("h1", class_="text-sm desktop:text-xl text-black-800 font-bold desktop:font-bold")

    if caixa and nome_produto:
        preco = (caixa.find_next("h4", class_="duration-500"))
        if preco:
            preco_float = float((preco.string).replace("R$", "").replace("\u00a0", "").replace(".", "").replace(",", "."))
            produto = {"Nome": nome_produto.string, "Valor": f"{(preco_float)}" }
            preco_ant = None    
            try:
                with open("preco_produto.json", mode="r", encoding="utf-8") as read_file:
                    preco_ant = float(json.load(read_file)["Valor"])
            except FileNotFoundError:
                print("Arquivo não encontrado")
            if preco_ant is None or preco_ant == preco_float:
                print(f"{produto['Nome']} está custando R$ {produto['Valor']}")
            elif preco_ant < preco_float:
                print(f"O preço do {produto['Nome']} aumentou R$ {preco_float - preco_ant} está custando R$ {produto['Valor']}.")
            else:
                print(f"O preço do {produto['Nome']} diminuiu R$ { preco_ant - preco_float} está custando R$ {produto['Valor']}.")
            if preco_ant is None or preco_ant != preco_float:
                with open("preco_produto.json", mode="w", encoding="utf-8") as file:
                    json.dump(produto, file, indent=0)
        else:
            print("Não Foi possivel encontrar o preço do produto")
    else:
        print("Não foi possivel encontrar o conteudo da pagina")
    time.sleep(30)
