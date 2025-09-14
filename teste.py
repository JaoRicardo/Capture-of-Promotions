import sqlite3

def iniciar_db():
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        create_table="""
        create table if not exists produtos (
            idp INTEGER PRIMARY KEY AUTOINCREMENT,
            apelido TEXT,
            url TEXT NOT NULL,
            seletor_nome TEXT,
            seletor_preco TEXT,
            seletor_disponibilidade TEXT,
            ultimo_preco REAL,
            ultima_verificacao TEXT,
            em_estoque BOOLEAN,
            fonte varchar(25)
            );
            """
        cursor.execute(create_table)

def listar_produtos():
    lista_prodrutos = []
    seleciona = "SELECT * FROM produtos;"
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(seleciona)
        all_produtos = cursor.fetchall()
        nome_colunas = [descricao[0] for descricao in cursor.description]
        if cursor.description:
            for produtos in all_produtos:
                produto = {}
                for i, nome_coluna in enumerate(nome_colunas):
                    produto[nome_coluna] = produtos[i]
                lista_prodrutos.append(produto)
    return lista_prodrutos

a = listar_produtos()
print(a)
# create_produto = """
# insert into produtos (
#     apelido, url, seletor_nome, seletor_preco, seletor_disponibilidade, ultimo_preco, ultima_verificacao, em_estoque, fonte)
#     values (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

# info_produto = (('ssd kingston', 'www.kington.com', 'cssnome', 'csspreco', 'cssdisponivel', 1200.50, '2025-08-25', 1, 'Kabum'))

# cursor.execute(create_produto, info_produto)

# connection.commit()