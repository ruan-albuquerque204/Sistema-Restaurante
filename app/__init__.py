# app/__init__.py
from flask import Flask, redirect, url_for
from . import routes as rt
from .models import db

def create_app():
    app = Flask(__name__)

    # Registrando o Blueprint
    app.register_blueprint(rt.bp_views)
    app.register_blueprint(rt.bp_produto)
    app.register_blueprint(rt.bp_pedido)
    app.register_blueprint(rt.bp_funcionario)
    
    # Criação do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    @app.route('/')
    def homepage():
        return redirect(url_for('views.homepage'))

    return app
