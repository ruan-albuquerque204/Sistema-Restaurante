# app/routes/views.py
from decimal import Decimal

from flask import Blueprint, render_template, request

from ..models import db, Produto, Pedido, ItemPedido

# Criando o Blueprint
bp_views = Blueprint('views', __name__, url_prefix='/views')

# Definindo uma rota
@bp_views.route('/')
def homepage():
    return render_template('homepage.html', title='Homepage')

# PEDIDOS
@bp_views.route('/pedidos/comanda')
def comandas():
    produtos = db.session.query(Produto).all()
    return render_template('pedido/comanda.html', title='Comanda', produtos=produtos)

@bp_views.route('/pedidos')
def pedidos():
    pedidos = db.session.query(Pedido).all()
    return render_template('pedido/lista.html', title='Pedidos', pedidos=pedidos)

# PRODUTOS
@bp_views.route('/produtos/cadastro')
def cadastro_produto():
    produtos = db.session.query(Produto).all()
    return render_template('produto/cadastro.html', title='Produto', produtos=produtos)

@bp_views.route('/produto/<int:id>')
def produtos_pedido(id: int):
    montante = Decimal(0)
    itens = []
    for i in db.session.query(ItemPedido).filter_by(pedido_fk=id).all():
        total = Decimal(i.quantidade) * i.valor
        i.montante = f'{total:.2f}'
        montante += total
        itens.append(i)
    
    return render_template('pedido/pedido.html', title=f'Pedido {id}', itens=itens, montante=f'{montante:.2f}')
