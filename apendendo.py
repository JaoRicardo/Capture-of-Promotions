import telebot
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(token)

bot.send_message(-1003083634589, "Bom dia")


