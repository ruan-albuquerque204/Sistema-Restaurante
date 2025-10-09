from flask import Blueprint, jsonify, request, redirect, url_for

from ..models import db, IntegrityError
from ..models.produto import Produto

bp_produto = Blueprint('produto', __name__, url_prefix='/api/produto')

@bp_produto.route('/', methods=['GET'])
def lista_produto():
    pedidos = list(p.to_json() for p in Produto.query.all())
    return jsonify(pedidos)

@bp_produto.route('/<int:id>', methods=['GET'])
def busca_produto(id):
    produto: Produto = Produto.query.filter_by(id=id).first()
    
    if not produto:
        return jsonify({'error': 'produto não existe'}), 400
    
    return jsonify({'mensagem': 'produto localizado', 'produto': produto.to_json()}), 200

@bp_produto.route('/cadastrar', methods=['POST'])
def cria_produto():
    form: dict = request.form
    
    nome = form.get('nome')
    valor = float(form.get('valor'))
    # quantidade = data.get('quantidade')
    # tipo_unidade = data.get('tipo_unidade')
    
    if not nome or not valor: #  or quantidade is None or not tipo_unidade
        return redirect(url_for('views.cadastro_produto'))
        return jsonify({'error': 'todos os campos são obrigatórios'}), 400
    # elif tipo_unidade not in ('unidade', 'peso'):
    #     return jsonify({'error': 'tipo de unidade pode ser "unidade" ou "peso"'}), 400
    # elif not isinstance(quantidade, int) or quantidade < 0:
    #     return jsonify({'error': f'Quantidade é um inteiro não negativo'}), 400
    elif not isinstance(valor, (int, float)) or valor < 0:
        return redirect(url_for('views.cadastro_produto'))
        return jsonify({'error': f'Valor numero não negativo'}), 400
    
    nome = nome.lower()
    
    produto = db.session.query(Produto).filter_by(nome=nome).first()
    
    try:
        if produto:
            produto.valor = valor
        else:
            produto = Produto(nome=nome, valor=valor) #, quantidade=quantidade, tipo_unidade=tipo_unidade
        
        db.session.add(produto)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        mensagem_error = str(e)
        
        if 'UNIQUE constraint failed: produto.nome' in mensagem_error:
            return redirect(url_for('views.cadastro_produto'))
            return jsonify({'error': f'Nome {nome} já está cadastrado'}), 400
        
        return redirect(url_for('views.cadastro_produto'))
        return jsonify({'error': str(e.args)}), 400        
    
    return redirect(url_for('views.cadastro_produto'))
    return jsonify({'status': 'ok', 'produto': produto.to_json()}), 201

@bp_produto.route('/excluir/<int:id>')
def excluir_item(id: int):
    produto = db.session.query(Produto).filter_by(id=id).first()
    if not produto:
        return redirect(url_for('views.cadastro_produto'))
        return jsonify({'error': 'produto não existe'}), 400
    
    db.session.delete(produto)
    db.session.commit()

    return redirect(url_for('views.cadastro_produto'))
    return jsonify({'status': 'ok', 'produto': produto.to_json()}), 201

@bp_produto.route('/diminuir/<int:id>')
def diminuir_item(id: int):
    quant = request.args.get('quant')
    
    produto = db.session.query(Produto).filter_by(id=id).first()
    if not produto:
        return redirect(url_for('views.cadastro_produto'))
        return jsonify({'error': 'produto não existe'}), 400
    elif quant is None:
        quant = 1
    elif quant.isdecimal():
        quant = int(quant)
    
    if quant <= 0: quant = 1
    
    if produto.quantidade - quant < 0:
        return redirect(url_for('views.cadastro_produto'))
        return jsonify({'error': 'produto não pode ficar negativo'}), 400
    
    produto.quantidade -= quant
    db.session.commit()

    return redirect(url_for('views.cadastro_produto'))
    return jsonify({'status': 'ok', 'produto': produto.to_json()}), 201

@bp_produto.route('/adicionar/<int:id>', methods=['POST'])
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
