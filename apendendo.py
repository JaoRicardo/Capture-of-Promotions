import json

thisdict = {
"Nome": "casa",
"Valor": 100
}

with open("Preco_Fone", mode="w", encoding="utf-8") as write_file:
    json.dump(thisdict, write_file)

