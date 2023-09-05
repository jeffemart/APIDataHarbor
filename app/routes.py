from flask import Blueprint, jsonify, request, render_template
from .models import db, Post
import requests

# Crie um Blueprint para as rotas
posts_bp = Blueprint('posts', __name__)


@posts_bp.route('/')
def home():
    return render_template('home.html')


@posts_bp.route('/api/posts', methods=['GET'])
def get_and_posts():
    # Faz a solicitação GET à API externa
    response = requests.get('https://jsonplaceholder.typicode.com/posts')

    if response.status_code == 200:
        posts_data = response.json()
        return jsonify(posts_data)

    else:
        return jsonify({'error': 'Falha ao buscar posts da API'}), 500


@posts_bp.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    # Crie um novo post com base nos dados fornecidos
    new_post = Post(
        id=data['id'],
        title=data['title'],
        body=data['body']
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'Post criado com sucesso!'}), 201
