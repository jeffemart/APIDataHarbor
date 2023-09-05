import os
from flask import Flask
from app.models import db, Post
from app.routes import posts_bp  # Importe a blueprint

app = Flask(__name__, template_folder='app/templates')

# Defina o caminho absoluto para a pasta 'instance'
base_dir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(base_dir, 'instance')

# Configuração do banco de dados SQLite temporário para testes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

# Registre a blueprint para as rotas de posts
app.register_blueprint(posts_bp)

if __name__ == '__main__':
    app.run(debug=True)
