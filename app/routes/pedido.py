from datetime import date
from decimal import Decimal

from flask import Blueprint, jsonify, request

from ..models import db, IntegrityError, Pedido, Cliente, Produto, ItemPedido, Funcionario

bp_pedido = Blueprint('pedido', __name__, url_prefix='/api/pedido')

@bp_pedido.route('/', methods=['GET'])
def lista_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([pedido.to_json() for pedido in pedidos])

@bp_pedido.route('/registrar', methods=['POST'])
def criar_pedido():
    data: dict = request.get_json()
    
    formas = ('dinheiro', 'debito', 'credito', 'pix')
    
    funcionario = data.get('funcionario')
    cliente = data.get('cliente')
    itens = data.get('itens')
    forma_pagamento = data.get('forma_pagamento')
    data = data.get('data')
    
    if not itens:
        return jsonify({'error': 'não foram passados nenhum item'}), 400
    # elif any(not isinstance(i, int) for i in itens):
    #     return jsonify({'error': 'os itens podem ser somente id'}), 400
    elif forma_pagamento not in formas:
        return jsonify({'error': 'forma de pagamento não aceita'}), 400
    # elif not isinstance(funcionario, int) or not db.session.query(Funcionario).filter_by(id=funcionario).first():
    #     return jsonify({'error': 'funcionario nao é valido'}), 400
    # elif not isinstance(cliente, int) and not cliente is None:
    #     return jsonify({'error': 'cliente não é válido'}), 400
    elif not data:
        data = date.today()
    
    itens_contadores = {}
    for i in itens:
        if itens_contadores.get(i['id']):
            itens_contadores[i] += Decimal(str(i['quantidade']))
            continue
        itens_contadores[i['id']] = Decimal(str(i['quantidade']))
    
    # itens_contadores = map(lambda i: float(i) if i // 1 > 0 else)
    
    pedido = Pedido(data=data) # funcionario_fk=funcionario, cliente_fk=cliente
    itens_pedidos: list[ItemPedido] = []
    
    mont_pedido = Decimal()
    quant_pedido = 0
    for id_item, quant_item in itens_contadores.items():
        produto = db.session.query(Produto).filter_by(id=id_item).first()
        if not produto:
            return jsonify({'error': f'produto {id_item} não está cadastrado'}), 400
        # elif produto.quantidade - value < 0:
        #     return jsonify({'error': f'produto {produto.nome} não possui estoque suficiente'}), 400
        mont_pedido += produto.valor * quant_item
        quant_pedido += 1
        itens_pedidos.append(ItemPedido(nome=produto.nome, valor=float(produto.valor), quantidade=float(quant_item) if float(quant_item) % 1 > 0 else int(quant_item)))
        # produto.quantidade -= value
    
    pedido.valor = float(mont_pedido)
    pedido.quant_produtos = quant_pedido
    pedido.forma_pagamento = forma_pagamento
    
    db.session.add(pedido)
    db.session.commit()
    
    for ip in itens_pedidos:
        ip.pedido_fk = pedido.id
    
    db.session.add_all(itens_pedidos)
    db.session.commit()
    
    return jsonify({'status': 'ok', 'mensagem': f'Pedido {pedido.id} cadastrado com sucesso.','pedido': pedido.to_json(), 'itens': [ip.to_json() for ip in itens_pedidos]}), 201