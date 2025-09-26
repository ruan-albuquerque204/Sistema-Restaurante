from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import db

class Pedido(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    funcionario_fk = Column(Integer, ForeignKey('funcionario.id'),nullable=False)
    cliente_fk = Column(Integer, ForeignKey('cliente.id'), default=0)
    
    funcionario = relationship('Fucionario', backref='pedidos')
    cliente = relationship('Cliente', backref='pedidos')

