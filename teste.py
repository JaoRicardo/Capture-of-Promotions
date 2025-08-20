from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.error
import json

url = "https://www.kabum.com.br/produto/235984/placa-de-video-rx-6600-cld-8g-asrock-amd-radeon-8gb-gddr6-90-ga2rzz-00uanf"

try:
    page = urlopen(url)
except urllib.error.URLError:
    print("URL não existe ou está incorreta")
    exit()

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
        with open("Preco_Fone", mode="r", encoding="utf-8") as read_file:
            x = json.load(read_file)
            preco_ant = float(x["Valor"])
        if  preco_ant == preco_float:
            print(f"O {produto['Nome']} está custando R$ {produto['Valor']}.")
        elif preco_ant < preco_float:
            print(f"O preço do {produto['Nome']} aumentou R$ {preco_float - preco_ant} está custando R$ {produto['Valor']}.")
            with open("Preco_Fone", mode="w", encoding="utf-8") as file:
                json.dump(produto, file, indent=0)
        else:
            print(f"O preço do {produto['Nome']} diminuiu R$ { preco_ant - preco_float} está custando R$ {produto['Valor']}.")
            with open("Preco_Fone", mode="w", encoding="utf-8") as file:
                json.dump(produto, file, indent=0)
    else:
        print("Não Foi possivel encontrar o preço do produto")
else:
    print("Não foi possivel encontrar o conteudo da pagina")

