import telebot

bot = telebot.TeleBot("z")

@bot.message_handler(["Start", "Hello"])
def send_welcome(message):
    bot.reply_to(message, "Olá Mundo")

@bot.message_handler(["death"])
def death(message):
    bot.reply_to(message, "Ixi, qué não")
    exit()
    bot.send_message("Ixi, qué não")
# +VTtCnJ7QZIJhOTIx
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message)

bot.send_message(12, "Bom dia")

bot.infinity_polling()
