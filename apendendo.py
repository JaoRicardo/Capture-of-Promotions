from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.error
import json
import time
import os
import telebot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")
grupo_id = os.getenv("GRUPO_ID")
meu_id = os.getenv("MEU_ID")
bot = telebot.TeleBot(token)

url = "https://www.kabum.com.br/produto/621162/ssd-kingston-nv3-1-tb-m-2-2280-pcie-4-0-x4-nvme-leitura-6000-mb-s-gravacao-4000-mb-s-azul-snv3s-1000g"

def formatar_preco(preco):
    preco_formatado = float((preco.string).replace("R$", "").replace("\u00a0", "").replace(".", "").replace(",", "."))
    return preco_formatado

def buscar_produto(url):
    try:
        page = urlopen(url)
    except urllib.error.URLError:
        return None
    
    html = page.read().decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    caixa = soup.find("div", class_="w-full p-8 rounded-8 border-solid border border-black-400")
    caixa2 = soup.find("div", class_="col-span-4 tablet:col-span-6 desktop:col-span-3 desktop:mt-16 order-1 desktop:order-2")
    nome_produto = caixa2.find_next("h1", class_="text-sm desktop:text-xl text-black-800 font-bold desktop:font-bold")
    if caixa and nome_produto:
        preco = (caixa.find_next("h4", class_="duration-500"))
        if preco:
            preco_float = formatar_preco(preco)
            return {"nome" : (nome_produto.string), "preco": preco_float}
        else:
            return 0
    else:
        return 0

def ler_produto_antigo(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode="r", encoding="utf-8") as read_file:
            produto = json.load(read_file)
            produto["preco"] = float(produto["preco"])
            return produto
    except FileNotFoundError:
        return None

def enviar_messagem_telegram(id_do_chat, messagem):
     bot.send_message(id_do_chat, messagem)

def salvar_produto_novo(caminho_arquivo, produto):
    with open(caminho_arquivo, mode="w", encoding="utf-8") as file:
        json.dump(produto, file, indent=0)

while True:

    produto = buscar_produto(url)
    if produto is None:
        enviar_messagem_telegram(meu_id, f"A {url} não existe ou está incorreta\n tentando reconexão em 25 min")
        time.sleep(1500)
        continue
    elif produto == 0:
        enviar_messagem_telegram(meu_id, f"Não foi possivel encontrar o conteudo da pagina {url}.\n Tentando novamente em 5 min")
        time.sleep(300)
        continue
    
    produto_ant = ler_produto_antigo("produto.json")

    if produto_ant is None or produto_ant != produto:
        enviar_messagem_telegram(grupo_id, f"{produto['nome']} está custando R$ {produto['preco']}\n {url}")
        salvar_produto_novo("produto.json", produto)
    elif produto_ant["preco"] < produto["preco"]:
        enviar_messagem_telegram(grupo_id, f"O preço aumentou R$ {produto['preco'] - produto_ant['preco']}")
    elif produto_ant["preco"] > produto["preco"]:
        enviar_messagem_telegram(grupo_id, f"O preço diminuiu R$ {produto_ant['preco'] - produto['preco']}")
    time.sleep(3600)
