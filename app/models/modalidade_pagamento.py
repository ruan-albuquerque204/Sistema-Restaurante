from sqlalchemy import Column, Integer, String

from . import db

class ModalidadePagamento(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(30), nullable=False)