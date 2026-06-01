
# PARTE 4 - LIVRO DE OFERTAS E MOTOR DE MATCH - Responsável: Victor

class Order:
    #Classe para a ordem de negociação
    def __init__(self, id, tipo, preco, quantidade):
        self.id = id
        self.tipo = tipo  # "compra" ou "venda"
        self.preco = float(preco)
        self.quantidade = int(quantidade) # qauntidade a ser negociada

    def __str__(self):
        #formatação para representar a ordem
        return f"[ID {self.id}] {self.tipo.upper()} | Qtd: {self.quantidade} | Preço: R$ {self.preco:.2f}"


class Node:
    #Guarda a ordem de compra e venda e aponta para os outros
    def __init__(self, order):
        self.order = order #Conteudo que o nó carrega
        self.next = None
        self.prev = None


class Queue:
    # Classe que representa uma fila - First in, First out
    # Fila de encadeamento manual
    def __init__(self):
        #Inicia a fila vazia
        self.head = None
        self.tail = None

    def vazio(self):
        return self.head is None

    def inserir(self, order):
        #Jnsere uma nova ordem no fim da fila
        novo_no = Node(order)
        if self.vazio():
            self.head = self.tail = novo_no
        else:
            self.tail.next = novo_no
            novo_no.prev = self.tail
            self.tail = novo_no

    def remover(self):
        # FIFO: Remove do início usando a referência head
        if self.vazio():
            return None
        temp = self.head.order
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        return temp


if __name__ == "__main__":
    print("Teste Local para o dia 1")
    
    # Criando a fila de entrada
    fila_de_entrada = Queue()
    
    # Criando ordens de simulação
    o1 = Order(id=101, tipo="compra", preco=50.0, quantidade=10)
    o2 = Order(id=102, tipo="venda", preco=48.5, quantidade=15)
    
    print("\ninserindo Ordem")
    fila_de_entrada.inserir(o1)
    print(f"Adicionada: {o1}")
    fila_de_entrada.inserir(o2)
    print(f"Adicionada: {o2}")
    
    print("\nRemovendo Ordem")
    ordem_removida_1 = fila_de_entrada.remover()
    print(f"Processando: {ordem_removida_1}")
    
    ordem_removida_2 = fila_de_entrada.remover()
    print(f"Processando: {ordem_removida_2}")
    
    # Tentando remover de uma fila vazia
    tentativa = fila_de_entrada.remover()
    if tentativa is None:
        print("\nFila de entrada vazia, sem ordens")
