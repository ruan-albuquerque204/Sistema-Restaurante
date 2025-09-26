from sqlalchemy import Column, Integer, String, Enum, DECIMAL
from sqlalchemy.orm import validates

from . import db

class Produto(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    quantidade = Column(Integer, default=0)
    valor = Column(DECIMAL(10,2), nullable=False)
    tipo_unidade = Column(Enum('unidade', 'peso'), nullable=False)
    
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
            'nome': self.nome,
            'quantidade': self.quantidade,
            'valor': self.valor,
            'tipo_unidade': 'unidade' if self.tipo_unidade == 1 else 'quilo',
        }
        