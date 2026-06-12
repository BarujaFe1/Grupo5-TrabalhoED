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

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insercao_ordenada(self, ordem:Order):
        no = Node(ordem)
        if self.head == None:
            self.head = no
            self.tail = no
            return
        
        if no.data.tipo == 'C':

            if no.data.preco > self.head.data.preco:
                self.head.prev = no
                no.next = self.head
                self.head = no
                return

            ponteiro = self.head
            while ponteiro:
                if no.data.preco > ponteiro.data.preco:
                    no.next = ponteiro
                    no.prev = ponteiro.prev
                    ponteiro.prev.next = no
                    ponteiro.prev = no
                    return
                ponteiro = ponteiro.next
            no.prev = self.tail
            self.tail.next = no
            self.tail = no
        
        else:

            if no.data.preco < self.head.data.preco:
                self.head.prev = no
                no.next = self.head
                self.head = no
                return
            
            ponteiro = self.head
            while ponteiro:
                if no.data.preco < ponteiro.data.preco: #Desigualdade estrita mantém a prioridade de quem chegou primeiro
                    no.next = ponteiro
                    no.prev = ponteiro.prev
                    ponteiro.prev.next = no
                    ponteiro.prev = no
                    return
                ponteiro = ponteiro.next
            no.prev = self.tail
            self.tail.next = no
            self.tail = no

    def remover(self, ordem:Order):

        if self.head == None:
            return
        
        ponteiro = self.head
        while ponteiro:
            if ponteiro.data.id == ordem.id:
                if ponteiro == self.head and ponteiro == self.tail:
                    self.head = None
                    self.tail = None
                
                elif ponteiro == self.head:
                    self.head = ponteiro.next
                    self.head.prev = None
                
                elif ponteiro == self.tail:
                    self.tail = ponteiro.prev
                    self.tail.next = None
                
                else:
                    ponteiro.prev.next = ponteiro.next
                    ponteiro.next.prev = ponteiro.prev
                
                return True
            ponteiro = ponteiro.next
        return False

    def busca(self, id_ordem:int):

        if self.head == None:
            return False
        
        ponteiro = self.head
        while ponteiro:
            if ponteiro.data.id == id_ordem:
                return ponteiro.data
            ponteiro = ponteiro.next
        return False

    def exibir(self):

        if self.head == None:
            print('Lista Vazia')
            return
        
        ponteiro = self.head
        while ponteiro:
            print(f'ID:{ponteiro.data.id}, Tipo:{ponteiro.data.tipo}, Preço:{ponteiro.data.preco}, Quantidade:{ponteiro.data.quantidade}, Tempo:{ponteiro.data.timestamp}')
            ponteiro = ponteiro.next 
