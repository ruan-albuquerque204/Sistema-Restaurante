from sqlalchemy.exc import IntegrityError

from .data_base import db
from .produto import Produto
from .pedido import Pedido
from .cliente import Cliente
from .item_pedido import ItemPedido
from .funcionario import Funcionario