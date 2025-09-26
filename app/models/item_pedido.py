from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import db

class ItemPedido(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_fk = Column(Integer, ForeignKey('pedido.id'))
    produto_fk = Column(Integer, ForeignKey('produto.id'))