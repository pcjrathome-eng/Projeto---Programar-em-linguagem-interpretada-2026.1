from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# ---------------- DB ----------------
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- LOGIN ----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    conn = get_db()
    user = conn.execute(
        'SELECT * FROM usuarios WHERE email=?',
        (data['email'],)
    ).fetchone()

    if user and user['senha'] == data['senha']:
        return jsonify({"sucesso": True})

    return jsonify({"erro": "Usuário ou senha incorretos"}), 401


# ---------------- USUÁRIOS ----------------

# LISTAR
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_db()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    return jsonify([dict(u) for u in usuarios])

# CRIAR
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    conn = get_db()

    # verifica se já existe
    existente = conn.execute(
        'SELECT * FROM usuarios WHERE email=?',
        (data['email'],)
    ).fetchone()

    if existente:
        return jsonify({"erro": "Email já cadastrado"}), 400

    conn.execute(
        'INSERT INTO usuarios (nome, email, senha, cpf) VALUES (?, ?, ?, ?)',
        (data['nome'], data['email'], data['senha'], data['cpf'])
    )
    conn.commit()

    return jsonify({"msg": "Usuário criado"})

# DETALHE
@app.route('/usuarios/<int:id>', methods=['GET'])
def detalhe_usuario(id):
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM usuarios WHERE id=?', (id,)
    ).fetchone()

    if user:
        return jsonify(dict(user))

    return jsonify({"erro": "Usuário não encontrado"}), 404

# EDITAR
@app.route('/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    data = request.json
    conn = get_db()

    conn.execute(
        'UPDATE usuarios SET nome=?, email=?, senha=?, cpf=? WHERE id=?',
        (data['nome'], data['email'], data['senha'], data['cpf'], id)
    )
    conn.commit()

    return jsonify({"msg": "Usuário atualizado"})

# DELETAR
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    conn = get_db()

    conn.execute('DELETE FROM usuarios WHERE id=?', (id,))
    conn.commit()

    return jsonify({"msg": "Usuário removido"})


# ---------------- PRODUTOS ----------------

# LISTAR
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    conn = get_db()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    return jsonify([dict(p) for p in produtos])

# CRIAR
@app.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.json
    conn = get_db()

    conn.execute(
        '''INSERT INTO produtos 
        (nome, preco, tipo, descricao, validade, promocao, preco_promocional) 
        VALUES (?, ?, ?, ?, ?, 0, NULL)''',
        (data['nome'], data['preco'], data['tipo'], data['descricao'], data['validade'])
    )
    conn.commit()

    return jsonify({"msg": "Produto criado"})

# EDITAR
@app.route('/produtos/<int:id>', methods=['PUT'])
def editar_produto(id):
    data = request.json
    conn = get_db()

    conn.execute(
        '''UPDATE produtos 
        SET nome=?, preco=?, tipo=?, descricao=?, validade=? 
        WHERE id=?''',
        (data['nome'], data['preco'], data['tipo'], data['descricao'], data['validade'], id)
    )
    conn.commit()

    return jsonify({"msg": "Produto atualizado"})

# DELETAR
@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    conn = get_db()

    conn.execute('DELETE FROM produtos WHERE id=?', (id,))
    conn.commit()

    return jsonify({"msg": "Produto removido"})


# ---------------- PROMOÇÕES ----------------

# APLICAR PROMOÇÃO
@app.route('/produtos/<int:id>/promocao', methods=['PUT'])
def aplicar_promocao(id):
    data = request.json
    conn = get_db()

    conn.execute(
        'UPDATE produtos SET promocao=1, preco_promocional=? WHERE id=?',
        (data['preco_promocional'], id)
    )
    conn.commit()

    return jsonify({"msg": "Promoção aplicada"})

# REMOVER PROMOÇÃO
@app.route('/produtos/<int:id>/remover', methods=['PUT'])
def remover_promocao(id):
    conn = get_db()

    conn.execute(
        'UPDATE produtos SET promocao=0, preco_promocional=NULL WHERE id=?',
        (id,)
    )
    conn.commit()

    return jsonify({"msg": "Promoção removida"})


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True, port=3001)