# PARTE 2 - FILA E PILHA - Responsável: Fernando


class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class Queue:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def enqueue(self, dado):
        novo = No(dado)
        if self.fim is not None:
            self.fim.proximo = novo
        self.fim = novo
        if self.inicio is None:
            self.inicio = novo

    def dequeue(self):
        if self.is_empty():
            return None
        dado = self.inicio.dado
        self.inicio = self.inicio.proximo
        if self.inicio is None:
            self.fim = None
        return dado

    def peek(self):
        if self.is_empty():
            return None
        return self.inicio.dado

    def is_empty(self):
        return self.inicio is None

    # Aliases em português
    def inserir(self, dado):
        return self.enqueue(dado)

    def remover(self):
        return self.dequeue()

    def vazio(self):
        return self.is_empty()


class Stack:
    def __init__(self):
        self.topo = None

    def push(self, dado):
        novo = No(dado)
        novo.proximo = self.topo
        self.topo = novo

    def pop(self):
        if self.is_empty():
            return None
        dado = self.topo.dado
        self.topo = self.topo.proximo
        return dado

    def peek(self):
        if self.is_empty():
            return None
        return self.topo.dado

    def is_empty(self):
        return self.topo is None

    # Aliases em português
    def empilhar(self, dado):
        return self.push(dado)

    def desempilhar(self):
        return self.pop()

    def vazio(self):
        return self.is_empty()
