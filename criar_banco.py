import sqlite3

conn = sqlite3.connect('database.db')

# -------- USUÁRIOS --------
conn.execute('''
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    senha TEXT,
    cpf TEXT
)
''')

# -------- PRODUTOS --------
conn.execute('''
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    preco REAL,
    tipo TEXT,
    descricao TEXT,
    validade TEXT,
    promocao INTEGER DEFAULT 0,
    preco_promocional REAL
)
''')

conn.commit()
conn.close()

print("Banco criado com sucesso!")