from sqlalchemy import Column, Integer, String

from . import db

class Cliente(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)