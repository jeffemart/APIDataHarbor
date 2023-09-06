from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, render_template
from .models import db, Post, User

api = Blueprint('api', __name__)


# Rota para autenticação básica
@api.route('/auth', methods=['POST'])
def login():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Credenciais de login inválidas'}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Credenciais de login inválidas'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Dados de registro inválidos'}), 400

    username = data['username']
    password = data['password']

    # Verifica se o nome de usuário já está em uso
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Nome de usuário já em uso'}), 400

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registro bem-sucedido'}), 201

# Rota para exibir template básico
@api.route('/')
def home():
    return render_template('index.html')

# Rota para buscar todos os registros (método GET)
@api.route('/post/get', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    post_list = []

    for post in posts:
        post_data = {
            'id': post.id,
            'title': post.title,
            'body': post.body
        }
        post_list.append(post_data)

    return jsonify(post_list), 200

# Rota para inserir registros (método POST)
@api.route('/post/insert', methods=['POST'])
@jwt_required()
def insert_posts():
    # Se o código chegar aqui, o usuário está autenticado
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({'error': 'Formato JSON inválido - Deve ser uma lista de posts'}), 400

    for post_data in data:
        if 'id' not in post_data or 'title' not in post_data or 'body' not in post_data:
            return jsonify({'error': 'Formato JSON inválido para um ou mais posts'}), 400

        new_post = Post(id=post_data['id'], title=post_data['title'], body=post_data['body'])
        db.session.add(new_post)

    db.session.commit()

    return jsonify({'message': 'Posts inseridos com sucesso'}), 201

# Rota para editar registros (método PUT)
@api.route('/post/put/<int:id>', methods=['PUT'])
@jwt_required()
def edit_post(id):
    # Se o código chegar aqui, o usuário está autenticado
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if 'title' not in data or 'body' not in data:
        return jsonify({'error': 'Formato JSON inválido'}), 400

    post = Post.query.get(id)

    if not post:
        return jsonify({'error': 'Post não encontrado'}), 404

    post.title = data['title']
    post.body = data['body']
    
    db.session.commit()

    return jsonify({'message': 'Post editado com sucesso'}), 200

# Rota para excluir registros (método DELETE)
@api.route('/post/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    # Se o código chegar aqui, o usuário está autenticado
    current_user_id = get_jwt_identity()
    post = Post.query.get(id)

    if not post:
        return jsonify({'error': 'Post não encontrado'}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post excluído com sucesso'}), 200