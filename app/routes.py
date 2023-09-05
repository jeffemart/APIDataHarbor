from flask import Blueprint, jsonify, request, render_template
from app.models import db, Post
import requests

# Crie um Blueprint para as rotas
posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/')
def home():
    return render_template('home.html')

@posts_bp.route('/api/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    post_list = [post.to_dict() for post in posts]
    return jsonify(post_list)

@posts_bp.route('/api/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get(id)
    if post:
        return jsonify(post.to_dict())
    else:
        return jsonify({'error': 'Post não encontrado'}), 404

@posts_bp.route('/api/posts', methods=['GET'])
def get_and_insert_posts():
    # Faz a solicitação GET à API externa
    response = requests.get('https://jsonplaceholder.typicode.com/posts')

    if response.status_code == 200:
        posts_data = response.json()

        # Insere os dados no banco de dados SQLite
        for post_data in posts_data:
            post = Post(
                userId=post_data['userId'],
                title=post_data['title'],
                body=post_data['body']
            )
            db.session.add(post)

        db.session.commit()
        return jsonify({'message': 'Posts inseridos com sucesso!'})

    else:
        return jsonify({'error': 'Falha ao buscar posts da API'}), 500

# @posts_bp.route('/api/posts', methods=['POST'])
# def create_post():
#     data = request.get_json()
#     post = Post(**data)

#     db.session.add(post)
#     db.session.commit()

#     return jsonify({'message': 'Post criado com sucesso!'}), 201

@posts_bp.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({'error': 'Post não encontrado'}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(post, key, value)

    db.session.commit()

    return jsonify({'message': 'Post atualizado com sucesso!'})

@posts_bp.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({'error': 'Post não encontrado'}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post excluído com sucesso!'})
