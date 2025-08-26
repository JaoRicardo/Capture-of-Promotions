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
        return ("erro na URL", "URL não existe ou está errada")
    
    html = page.read().decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    caixa = soup.find("div", class_="w-full p-8 rounded-8 border-solid border border-black-400")
    caixa2 = soup.find("div", class_="col-span-4 tablet:col-span-6 desktop:col-span-3 desktop:mt-16 order-1 desktop:order-2")
    nome_produto = caixa2.find_next("h1", class_="text-sm desktop:text-xl text-black-800 font-bold desktop:font-bold")
    if caixa and nome_produto:
        preco = (caixa.find_next("h4", class_="duration-500"))
        if preco:
            preco_float = formatar_preco(preco)
            return ("sucesso", {"nome" : (nome_produto.string), "preco": preco_float})
        else:
            return ("erro no preço", "preço não pode ser encontrado")
    else:
        return ("erro nos dados", "Não foi possivel encontrar os dados")

def ler_produto_antigo(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode="r", encoding="utf-8") as read_file:
            produto = json.load(read_file)
            produto["preco"] = float(produto["preco"])
            return produto
    except FileNotFoundError:
        return None

def enviar_mensagem_telegram(id_do_chat, messagem):
     bot.send_message(id_do_chat, messagem)

def salvar_produto_novo(caminho_arquivo, produto):
    with open(caminho_arquivo, mode="w", encoding="utf-8") as file:
        json.dump(produto, file, indent=0)

while True:

    status, dados = buscar_produto(url)
    match status:
        case "sucesso":
            produto = dados
        case "erro na URL":
            enviar_mensagem_telegram(meu_id, f"{dados}\n {url}.\nTentando reconexão em 25 min")
            time.sleep(60)
            continue
        case "erro nos dados":
            enviar_mensagem_telegram(meu_id, f"{dados}\n {url}.\nTentando reconexão em 25 min")
            time.sleep(60)
            continue
        case "erro no preço":
            enviar_mensagem_telegram(meu_id, f"{dados}\n {url}.\nTentando reconexão em 25 min")
            time.sleep(60)
            continue
    
    produto_ant = ler_produto_antigo("produto.json")

    if produto_ant is None:
        enviar_mensagem_telegram(grupo_id, f"{produto['nome']} está custando R$ {produto['preco']}\n {url}")   
        salvar_produto_novo("produto.json", produto)
    elif produto_ant == produto:
        None
    else:
        if produto_ant != produto:
            enviar_mensagem_telegram(grupo_id, f"{produto['nome']} está custando R$ {produto['preco']}\n {url}")
            if produto_ant["preco"] < produto["preco"]:
                enviar_mensagem_telegram(grupo_id, f"O preço aumentou R$ {produto['preco'] - produto_ant['preco']}")
            elif produto_ant["preco"] > produto["preco"]:
                enviar_mensagem_telegram(grupo_id, f"O preço diminuiu R$ {produto_ant['preco'] - produto['preco']}")
            salvar_produto_novo("produto.json", produto)
    time.sleep(600)
