from sqlalchemy import Column, Integer, String

from . import db

class Funcionario(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    
    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome
        }