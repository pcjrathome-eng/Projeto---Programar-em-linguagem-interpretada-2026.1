import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    senha TEXT,
    cpf TEXT
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    preco REAL,
    tipo TEXT,
    descricao TEXT,
    validade TEXT,
    preco_promocao REAL
)
''')

conn.commit()
conn.close()

print("Banco criado com sucesso!")