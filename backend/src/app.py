from flask import Flask
from src.settings.config import Config
from src.settings.extensions import db, jwt, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicialização das extensões
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


    # Importar os Models
    from src.models.usuario_model import User
    
    # Registar as routes
    

    return app
