from flask import Flask, jsonify, request
from db import Database

app = Flask(__name__)
db = Database()

@app.route('/api/filmes', methods=['GET'])
def get_filmes():
    filmes = db.get_filmes()
    resultado = [{"id": f[0], "titulo": f[1], "diretor": f[2], "ano": f[3], "categoria": f[4]} for f in filmes]
    return jsonify(resultado)

@app.route('/api/filmes', methods=['POST'])
def add_filme():
    data = request.json
    if not data or 'titulo' not in data:
        return jsonify({"erro": "Dados inválidos"}), 400
    
    db.add_filme(data['titulo'], data['diretor'], data['ano'], data['categoria_id'])
    return jsonify({"mensagem": "Filme adicionado com sucesso"}), 201

@app.route('/api/filmes/<int:id>', methods=['DELETE'])
def delete_filme(id):
    db.delete_filme(id)
    return jsonify({"mensagem": "Filme deletado"})

@app.route('/api/filmes/<int:id>', methods=['PUT'])
def update_filme(id):
    data = request.json
    db.update_filme(id, data['titulo'], data['diretor'], data['ano'], data['categoria_id'])
    return jsonify({"mensagem": "Filme atualizado"})

def run_api():
    app.run(debug=False, use_reloader=False)