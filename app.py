from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import posts_bp

app = Flask(__name__, template_folder='app/templates')

# Configuração do banco de dados SQLite temporário para testes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use o SQLite em memória para testes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Registra o Blueprint para as rotas de posts
app.register_blueprint(posts_bp)

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)
