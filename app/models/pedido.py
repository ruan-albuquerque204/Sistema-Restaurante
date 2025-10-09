from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, String, DATE
from sqlalchemy.orm import relationship

from . import db
from .cliente import Cliente
from .funcionario import Funcionario

class Pedido(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(DECIMAL(10,2))
    forma_pagamento = Column(String(30))
    quant_produtos = Column(Integer)
    data = Column(DATE)
    # funcionario_fk = Column(Integer, ForeignKey('funcionario.id'),nullable=False)
    # cliente_fk = Column(Integer, ForeignKey('cliente.id'))
    
    # funcionario = relationship('Funcionario', backref='pedidos')
    # cliente = relationship('Cliente', backref='pedidos')
    itens = relationship('ItemPedido', back_populates='pedido')

    def to_json(self) -> dict:
        return {
            'id': self.id,
            # 'funcionario': self.funcionario_fk,
            # 'cliente': self.cliente_fk,
            'valor': self.valor,
            'forma_pagamento': self.forma_pagamento,
            'quant_produtos': self.quant_produtos,
        }
