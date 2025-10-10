from datetime import date
from decimal import Decimal

from flask import Blueprint, jsonify, request, redirect, url_for

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
    valor_pago = data.get('valorPago')
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
    
    pedido = Pedido(
        data=data,
        cliente=cliente,
        valor_pago=valor_pago,
        forma_pagamento=forma_pagamento) # funcionario_fk=funcionario, cliente_fk=cliente
    
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
        
        item = ItemPedido(
            nome=produto.nome,
            valor=float(produto.valor),
            pedido=pedido,
            quantidade=float(quant_item) if float(quant_item) % 1 > 0 else int(quant_item))
        
        pedido.itens.append(item)
        # produto.quantidade -= value
    
    pedido.valor = float(mont_pedido)
    pedido.quant_produtos = quant_pedido
    
    db.session.add(pedido)
    db.session.add_all(pedido.itens)
    db.session.commit()
        
    return jsonify({'status': 'ok', 'mensagem': f'Pedido {pedido.id} cadastrado com sucesso.','pedido': pedido.to_json(), 'itens': [ip.to_json() for ip in pedido.itens]}), 201


# Views
@bp_pedido.route('/excluir/<int:id>')
def excluir(id: int):
    pedido = db.session.query(Pedido).filter_by(id=id).first()
    
    if not pedido:
        return redirect(url_for('views.pedidos'))
    
    db.session.delete(pedido)
    db.session.commit()
    
    
    return redirect(url_for('views.pedidos'))
    