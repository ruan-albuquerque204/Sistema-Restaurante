from flask import Blueprint, jsonify, request

from ..models import db, IntegrityError
from ..models.produto import Produto

estoque = Blueprint('estoque', __name__, url_prefix='/api/estoque')

@estoque.route('/', methods=['GET'])
def lista_produto():
    produtos = Produto.query.all()
    return jsonify([produto.to_json() for produto in produtos])

@estoque.route('/', methods=['POST'])
def cria_produto():
    data: dict = request.get_json()
    
    nome = data.get('nome')
    valor = data.get('valor')
    quantidade = data.get('quantidade')
    tipo_unidade = data.get('tipo_unidade')
    
    if not nome or quantidade is None or valor is None or not tipo_unidade:
        return jsonify({'error': 'todos os campos são obrigatórios'}), 400
    elif tipo_unidade not in ('unidade', 'peso'):
        return jsonify({'error': 'tipo de unidade pode ser "unidade" ou "peso"'}), 400
    elif not isinstance(quantidade, int) or quantidade < 0:
        return jsonify({'error': f'Quantidade é um inteiro não negativo'}), 400
    elif not isinstance(valor, (int, float)) or valor < 0:
        return jsonify({'error': f'Valor numero não negativo'}), 400
    
    try:
        produto = Produto(nome=nome, valor=valor, quantidade=quantidade, tipo_unidade=tipo_unidade)
        
        db.session.add(produto)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        mensagem_error = str(e)
        
        if 'UNIQUE constraint failed: produto.nome' in mensagem_error:
            return jsonify({'error': f'Nome {nome} já está cadastrado'}), 400
        
        return jsonify({'error': str(e.args)}), 400        
    
    return jsonify({'status': 'ok', 'produto': produto.to_json()}), 201