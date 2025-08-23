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
            return nome_produto, preco_float
        else:
            return None
    else:
        return None

def ler_preco_antigo(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode="r", encoding="utf-8") as read_file:
            nome_salvo = json.load(read_file)["Nome"]
            preco_salvo = float(json.load(read_file)["Valor"])
            return nome_salvo, preco_salvo
    except FileNotFoundError:
        return "Arquivo não encontrado"

def enviar_messagem_telegram(messagem):
     bot.send_message(grupo_id, messagem)

def salvar_preco_novo(caminho_arquivo, produto):
    with open(caminho_arquivo, mode="w", encoding="utf-8") as file:
                    json.dump(produto, file, indent=0)

while True:
    try:
        page = urlopen(url)
    except urllib.error.URLError:
        print("URL não existe ou está incorreta")
        print("Tentando reconexão em 25 min")
        time.sleep(1500)
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
            produto = {"Nome": nome_produto.string, "Valor": f"{(preco_float)}"}
            preco_ant = None    
            try:
                with open("preco_produto.json", mode="r", encoding="utf-8") as read_file:
                    preco_ant = float(json.load(read_file)["Valor"])
            except FileNotFoundError:
                bot.send_message(grupo_id, "Arquivo não encontrado")
            if preco_ant is None or preco_ant == preco_float:
                bot.send_message(grupo_id, f"{produto['Nome']} está custando R$ {produto['Valor']}\n {url}")
            elif preco_ant < preco_float:
                bot.send_message(grupo_id, f"O preço do {produto['Nome']} aumentou R$ {preco_float - preco_ant} está custando R$ {produto['Valor']}.\n {url}")
            else:
                bot.send_message(grupo_id, f"O preço do {produto['Nome']} diminuiu R$ { preco_ant - preco_float} está custando R$ {produto['Valor']}.\n {url}")
            if preco_ant is None or preco_ant != preco_float:
                with open("preco_produto.json", mode="w", encoding="utf-8") as file:
                    json.dump(produto, file, indent=0)
        else:
            bot.send_message(grupo_id, "Não Foi possivel encontrar o preço do produto \n {url}")
    else:
        bot.send_message(grupo_id, "Não foi possivel encontrar o conteudo da pagina")
    time.sleep(3600)
