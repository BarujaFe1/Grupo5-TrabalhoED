from datetime import datetime

class Order:
    def __init__(self, id: int, tipo: str, preco: float, quantidade: int, timestamp: datetime):
        self.id = id
        self.tipo = tipo
        self.preco = preco
        self.quantidade = quantidade
        self.timestamp = timestamp

    def __str__(self):
        if self.tipo == 'C':
            return(
            f"ID: {self.id} | Tipo: Compra | "
            f"Preço: R$ {self.preco:.2f} | Quantidade: {self.quantidade} | "
            f"Timestamp: {self.timestamp}"
            )
        else:
            return(
            f"ID: {self.id} | Tipo: Venda | "
            f"Preço: R$ {self.preco:.2f} | Quantidade: {self.quantidade} | "
            f"Timestamp: {self.timestamp}"
            )
        
class Node:
    def __init__(self, data: Order):
        self.data = data
        self.prev = None
        self.next = None
