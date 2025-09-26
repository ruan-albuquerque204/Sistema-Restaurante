# app/routes/views.py
from flask import Blueprint

# Criando o Blueprint
views = Blueprint('views', __name__, url_prefix='/')

# Definindo uma rota
@views.route('/')
def home():
    return "Bem-vindo à página inicial!"

@views.route('/sobre')
def sobre():
    return "Esta é a página sobre."
