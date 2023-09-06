from flask import Flask
from flask_jwt_extended import JWTManager
from app.models import db
from app.routes import api

app = Flask(__name__, template_folder='app/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta'  # Defina sua própria chave secreta
jwt = JWTManager(app)

# Inicializa a extensão do SQLAlchemy
db.init_app(app)

# Registra as rotas da API
app.register_blueprint(api)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
