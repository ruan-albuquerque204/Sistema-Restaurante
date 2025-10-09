from flask import Blueprint, jsonify, request

from ..models import db, IntegrityError
from ..models.funcionario import Funcionario

bp_funcionario = Blueprint('funcionario', __name__, url_prefix='/api/funcionario')

@bp_funcionario.route('/', methods=['GET'])
def lista_produto():
    produtos = Produto.query.all()
    return jsonify([produto.to_json() for produto in produtos])

@bp_funcionario.route('/cadastrar', methods=['POST'])
def cria_produto():
    data: dict = request.get_json()
    
    nome = data.get('nome')
    
    if not nome:
        return jsonify({'error': 'nome é inválido'}), 400
    
    funcionario = Funcionario(nome=nome)
    
    try:
        db.session.add(funcionario)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        mensagem_error = str(e)
        
        return jsonify({'error': str(e.args)}), 400        
    
    return jsonify({'status': 'ok', 'funcionario': funcionario.to_json()}), 201

@bp_funcionario.route('/remover/<int:id>', methods=['POST'])
def remover_item(id: int):
    quant = request.args.get('quant')
    
    produto = db.session.query(Produto).filter_by(id=id).first()
    if not produto:
        return jsonify({'error': 'produto não existe'}), 400
    elif quant is None:
        quant = 1
    elif quant.isdecimal():
        quant = int(quant)
    
    if quant <= 0: quant = 1
    
    if produto.quantidade - quant < 0:
        return jsonify({'error': 'produto não pode ficar negativo'}), 400
    
    produto.quantidade -= quant
    db.session.commit()

    return jsonify({'status': 'ok', 'produto': produto.to_json()}), 201

@bp_funcionario.route('/adicionar/<int:id>', methods=['POST'])
def adicionar_item(id: int):
    quant = request.args.get('quant')
    
    produto = db.session.query(Produto).filter_by(id=id).first()
    if not produto:
        return jsonify({'error': 'produto não existe'}), 400
    elif quant is None:
        quant = 1
    elif quant.isdecimal():
        quant = int(quant)
    
    if quant <= 0: quant = 1
    
    produto.quantidade += quant
    db.session.commit()

    return jsonify({'status': 'ok', 'produto': produto.to_json()}), 201
