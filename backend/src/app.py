from flask import Flask
from src.settings.config import Config
from src.settings.extensions import db, jwt, migrate, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicialização das extensões
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)


    # Importar os Models
    from src.models.usuario_model import User
    from src.models.registry_model import Registry
    
    # Registar as routes
    from src.routes.resgitry_routes import registry_bp
    from src.routes.pdf_routes import pdf_bp
    
    app.register_blueprint(registry_bp)
    app.register_blueprint(pdf_bp)

    return app
