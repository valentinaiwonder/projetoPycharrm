from flask import Flask, jsonify, request
from main import app, con


@app.route('/livro', methods=['GET'])
def livro():
    cur = con.cursor()
    cur.execute('SELECT id_livro, titulo, autor, ano_publicacao FROM livros')
    livros = cur.fetchall()

    livros_dic = []
    for livro in livros:
        livros_dic.append({
            'id_livro': livro[0],
            'titulo': livro[1],
            'autor': livro[2],
            'ano_publicacao': livro[3]
        })
    return jsonify(mensagem='Lista de livros', livros=livros_dic)

@app.route ('/livro', methods=['POST'])
def livro_post():
    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    ano_publicacao= data.get('ano_publicacao')

    cursor = con.cursor()

    cursor.execute("SELECT 1 FROM LIVROS WHERE TITULO= ?", (titulo,))

    if cursor.fetchone():
        return jsonify("Livro já cadastrado.")

    cursor.execute("INSERT INTO LIVROS( TITULO, AUTOR, ANO_PUBLICACAO) VALUES (?, ?, ?)",
                   (titulo, autor, ano_publicacao))

    con.commit()
    cursor.close()

    return jsonify({
        'message' : "Livro cadastrado com sucesso!",
        'livro': {
            'titulo': titulo,
            'autor': autor,
            'ano_publicacao': ano_publicacao
        }
    })

from flask import Flask, request, jsonify
from main import app, con

@app.route('/livro/<int:id>', methods=['PUT'])
def livro_put(id):
    cursor = con.cursor()

    # Verifica se o livro existe
    cursor.execute("SELECT id_livro, titulo, autor, ano_publicacao FROM livros WHERE id_livro = ?", (id,))
    livro_data = cursor.fetchone()

    if not livro_data:
        cursor.close()
        return jsonify({"message": "Livro não foi encontrado"}), 404

    # Obtém os novos dados do JSON recebido
    data = request.get_json()
    titulo = data.get('titulo', livro_data[1])  # Mantém o título original se não for informado
    autor = data.get('autor', livro_data[2])  # Mantém o autor original se não for informado
    ano_publicacao = data.get('ano_publicacao', livro_data[3])  # Mantém o ano original se não for informado

    # Atualiza os dados do livro
    cursor.execute(
        "UPDATE livros SET titulo = ?, autor = ?, ano_publicacao = ? WHERE id_livro = ?",
        (titulo, autor, ano_publicacao, id)
    )

    con.commit()
    cursor.close()

    return jsonify({
        'message': "Livro atualizado com sucesso!",
        'livro': {
            'id_livro': id,
            'titulo': titulo,
            'autor': autor,
            'ano_publicacao': ano_publicacao
        }
    })

