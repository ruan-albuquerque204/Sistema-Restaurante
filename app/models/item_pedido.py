from sqlalchemy import Column, Integer, ForeignKey, String, DECIMAL
from sqlalchemy.orm import relationship, validates

from . import db

class ItemPedido(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    # produto_fk = Column(Integer, ForeignKey('produto.id'))
    nome = Column(String(100), nullable=False)
    valor = Column(DECIMAL(10,2), nullable=False)
    quantidade = Column(Integer, nullable=False)
    
    pedido_fk = Column(Integer, ForeignKey('pedido.id', ondelete='CASCADE'))
    pedido = relationship('Pedido', back_populates='itens')
    
    @validates('quantidade')
    def validade_quantidade(self, key, quant: int):
        if quant < 0:
            raise ValueError('Quantidade não pode ser um número negativo')
        return quant
    
    @validates('valor')
    def validar_valor(self, key, preco: int):
        if preco < 0:
            raise ValueError('Valor não pode ser negativo')
        return preco
    
    def to_json(self) -> dict:
        return {
            'id': self.id,
            'pedido_id': self.pedido_fk,
            'nome': self.nome,
            'quantidade': self.quantidade,
            'valor': self.valor,
        }
    
    def __repr__(self):
        return f'ItemPedido: {self.produto_fk} - {self.pedido_fk}'