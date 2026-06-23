# ==================================================
# SIMULADOR DE LIVRO DE OFERTAS
# Disciplina: Estrutura de Dados em Python
# Integrantes: Eduardo, Felipe, Fernando, Nicolas e Victor
#
# Arquivo único do projeto.
# PARTE 5 pronta: Menu principal e execução do simulador.
# Responsável: Felipe
# ==================================================

from datetime import datetime


# ==================================================
# PARTE 1 - CLASSES BASE E LISTA DUPLAMENTE ENCADEADA
# Responsável: Eduardo
# Commit: feat: implementa classes base e lista duplamente encadeada
# ==================================================

class Order:
    """
    Representa uma ordem de compra ou venda.

    Atributos:
    id, tipo, preco, quantidade e timestamp.
    """
    def __init__(self, id, tipo, preco, quantidade, timestamp):
        self.id = id
        self.tipo = tipo
        self.preco = preco
        self.quantidade = quantidade
        self.timestamp = timestamp

    def __str__(self):
        tipo_texto = "Compra" if self.tipo == "C" else "Venda"
        return (
            f"ID: {self.id} | Tipo: {tipo_texto} | "
            f"Preço: R$ {self.preco:.2f} | Quantidade: {self.quantidade} | "
            f"Timestamp: {self.timestamp}"
        )


class Node:
    """
    Nó da Lista Duplamente Encadeada.
    Encapsula o objeto Order e mantém os ponteiros next e prev.
    """
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """
    Lista Duplamente Encadeada com inserção ordenada.

    Compras ('C'): ordem decrescente de preço.
    Vendas ('V'): ordem crescente de preço.
    Preços iguais respeitam ordem de chegada (FIFO).
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def insercao_ordenada(self, ordem):
        no = Node(ordem)

        if self.head is None:
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
                if no.data.preco < ponteiro.data.preco:
                    no.next = ponteiro
                    no.prev = ponteiro.prev
                    ponteiro.prev.next = no
                    ponteiro.prev = no
                    return
                ponteiro = ponteiro.next

            no.prev = self.tail
            self.tail.next = no
            self.tail = no

    def remover(self, ordem):
        if self.head is None:
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

    def busca(self, id_ordem):
        if self.head is None:
            return False
        ponteiro = self.head
        while ponteiro:
            if ponteiro.data.id == id_ordem:
                return ponteiro.data
            ponteiro = ponteiro.next
        return False

    def exibir(self):
        if self.head is None:
            print('  Lista Vazia')
            return
        ponteiro = self.head
        while ponteiro:
            print(f'  ID:{ponteiro.data.id}, Tipo:{ponteiro.data.tipo}, '
                  f'Preço:{ponteiro.data.preco}, Quantidade:{ponteiro.data.quantidade}, '
                  f'Tempo:{ponteiro.data.timestamp}')
            ponteiro = ponteiro.next

    def vazia(self):
        return self.head is None

    def obter_topo(self):
        if self.head is None:
            return None
        return self.head.data

    def remover_topo(self):
        if self.head is None:
            return
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None


# ==================================================
# PARTE 2 - FILA ENCADEADA E PILHA DE UNDO
# Responsável: Fernando
# Commit: feat: implementa fila encadeada e pilha de undo
# ==================================================

class _QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    """
    Fila (FIFO) implementada manualmente com nós encadeados.
    Operações de extremidade em O(1).
    """
    def __init__(self):
        self._front = None
        self._rear = None

    def enqueue(self, data):
        node = _QueueNode(data)
        if self._rear is None:
            self._front = node
            self._rear = node
        else:
            self._rear.next = node
            self._rear = node

    def dequeue(self):
        if self._front is None:
            return None
        data = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        return data

    def peek(self):
        if self._front is None:
            return None
        return self._front.data

    def is_empty(self):
        return self._front is None

    inserir = enqueue
    remover = dequeue
    vazio = is_empty


class _StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    """
    Pilha (LIFO) implementada manualmente com nós encadeados.
    Operações de extremidade em O(1).
    """
    def __init__(self):
        self._top = None

    def push(self, data):
        node = _StackNode(data)
        node.next = self._top
        self._top = node

    def pop(self):
        if self._top is None:
            return None
        data = self._top.data
        self._top = self._top.next
        return data

    def peek(self):
        if self._top is None:
            return None
        return self._top.data

    def is_empty(self):
        return self._top is None

    empilhar = push
    desempilhar = pop
    vazio = is_empty


# ==================================================
# PARTE 3 - TRANSAÇÕES
# Responsável: Nicolas
# Commit: docs: adiciona transacoes
# ==================================================

class Transaction:
    """
    Representa uma transação entre uma ordem de compra e uma de venda.

    Atributos:
        id_compra (int): ID da ordem de compra.
        id_venda (int): ID da ordem de venda.
        preco (float): Preço de execução (preço de quem já estava no livro).
        quantidade (int): Quantidade negociada.
        timestamp (str): Momento da transação.
    """
    def __init__(self, id_compra, id_venda, preco, quantidade):
        self.id_compra = id_compra
        self.id_venda = id_venda
        self.preco = float(preco)
        self.quantidade = int(quantidade)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return (
            f"[{self.timestamp}] NEGÓCIO FECHADO | "
            f"Compra #{self.id_compra} x Venda #{self.id_venda} | "
            f"Qtd: {self.quantidade} | "
            f"Preço: R$ {self.preco:.2f}"
        )


class _TransactionNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class TransactionHistory:
    """
    Histórico de transações como lista encadeada simples.
    Evita uso de list nativa para o armazenamento principal.
    """
    def __init__(self):
        self._head = None

    def add(self, transaction):
        node = _TransactionNode(transaction)
        node.next = self._head
        self._head = node

    def show(self):
        if self._head is None:
            print("  Nenhuma transação efetuada até o momento.")
            return
        current = self._head
        while current:
            print(f"  {current.data}")
            current = current.next

    def is_empty(self):
        return self._head is None

    def __iter__(self):
        current = self._head
        while current:
            yield current.data
            current = current.next


# ==================================================
# PARTE 4 - LIVRO DE OFERTAS E MOTOR DE MATCH
# Responsável: Victor
# Commit: feat: implementa livro de ofertas e motor de match
# ==================================================

class OrderBook:
    """
    Livro de Ofertas com motor de casamento (match).

    Integra fila de entrada (Queue), listas de compra/venda (DoublyLinkedList),
    pilha de undo (Stack) e histórico de transações (TransactionHistory).
    """
    def __init__(self):
        self.fila_entrada = Queue()
        self.compras = DoublyLinkedList()
        self.vendas = DoublyLinkedList()
        self.pilha_undo = Stack()
        self.transacoes = TransactionHistory()

    def add_order(self, order):
        self.fila_entrada.enqueue(order)
        print(f"\nOrdem {order.id} ({order.tipo.upper()}) recebida e adicionada à fila.")

    def process_next_order(self):
        if self.fila_entrada.is_empty():
            print("\nFila de entrada vazia. Nenhuma ordem para processar.")
            return False
        ordem = self.fila_entrada.dequeue()
        print(f"\nProcessando ordem {ordem.id}...")
        self.match_order(ordem)
        return True

    def process_all_orders(self):
        while self.process_next_order():
            pass

    def match_order(self, ordem_atual):
        tipo = ordem_atual.tipo.strip().upper()

        if tipo == 'C':
            while ordem_atual.quantidade > 0 and not self.vendas.vazia():
                melhor_venda = self.vendas.obter_topo()
                if ordem_atual.preco >= melhor_venda.preco:
                    qtd = min(ordem_atual.quantidade, melhor_venda.quantidade)
                    transacao = Transaction(
                        id_compra=ordem_atual.id,
                        id_venda=melhor_venda.id,
                        preco=melhor_venda.preco,
                        quantidade=qtd
                    )
                    self.transacoes.add(transacao)
                    print(f"NEGÓCIO FECHADO! {qtd} un. negociadas a R$ {melhor_venda.preco:.2f}")
                    ordem_atual.quantidade -= qtd
                    melhor_venda.quantidade -= qtd
                    if melhor_venda.quantidade == 0:
                        self.vendas.remover_topo()
                else:
                    break
            if ordem_atual.quantidade > 0:
                self.compras.insercao_ordenada(ordem_atual)
                self.pilha_undo.push(ordem_atual.id)

        elif tipo == 'V':
            while ordem_atual.quantidade > 0 and not self.compras.vazia():
                melhor_compra = self.compras.obter_topo()
                if melhor_compra.preco >= ordem_atual.preco:
                    qtd = min(melhor_compra.quantidade, ordem_atual.quantidade)
                    transacao = Transaction(
                        id_compra=melhor_compra.id,
                        id_venda=ordem_atual.id,
                        preco=melhor_compra.preco,
                        quantidade=qtd
                    )
                    self.transacoes.add(transacao)
                    print(f"NEGÓCIO FECHADO! {qtd} un. negociadas a R$ {melhor_compra.preco:.2f}")
                    ordem_atual.quantidade -= qtd
                    melhor_compra.quantidade -= qtd
                    if melhor_compra.quantidade == 0:
                        self.compras.remover_topo()
                else:
                    break
            if ordem_atual.quantidade > 0:
                self.vendas.insercao_ordenada(ordem_atual)
                self.pilha_undo.push(ordem_atual.id)

    def show_buy_orders(self):
        print("\n <<<< LIVRO DE COMPRAS (Preços Decrescentes) >>>>")
        self.compras.exibir()

    def show_sell_orders(self):
        print("\n <<<< LIVRO DE VENDAS (Preços Crescentes) >>>>")
        self.vendas.exibir()

    def show_transactions(self):
        print("\n<<<< HISTÓRICO DE NEGOCIAÇÕES >>>>")
        self.transacoes.show()

    def undo_last_order(self):
        if self.pilha_undo.is_empty():
            print("\nNenhuma ordem para desfazer.")
            return
        id_ordem = self.pilha_undo.pop()
        removido = self.compras.remover(Order(id_ordem, '', 0, 0, ''))
        if not removido:
            removido = self.vendas.remover(Order(id_ordem, '', 0, 0, ''))
        if removido:
            print(f"\nOrdem ID {id_ordem} desfeita e removida do livro.")
        else:
            print(f"\nOrdem ID {id_ordem} não encontrada no livro para desfazer.")


# ==================================================
# PARTE 5 - MENU PRINCIPAL E EXECUÇÃO DO SIMULADOR
# Responsável: Felipe
# Commit: feat: adiciona menu principal e execucao do simulador
# ==================================================

def gerar_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ler_inteiro(mensagem, valor_minimo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if valor_minimo is not None and valor < valor_minimo:
                print(f"Valor inválido. Informe um número maior ou igual a {valor_minimo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_float(mensagem, valor_minimo=None):
    while True:
        try:
            entrada = input(mensagem).strip().replace(",", ".")
            valor = float(entrada)
            if valor_minimo is not None and valor < valor_minimo:
                print(f"Valor inválido. Informe um número maior ou igual a {valor_minimo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número válido. Exemplo: 25.50")


def ler_tipo_ordem():
    while True:
        tipo = input("Tipo da ordem [C = Compra | V = Venda]: ").strip().upper()
        if tipo in ("C", "V"):
            return tipo
        print("Tipo inválido. Digite apenas C para compra ou V para venda.")


def ler_ordem(tipo=None):
    print("\n--- Cadastro de nova ordem ---")
    id_ordem = ler_inteiro("ID da ordem: ", valor_minimo=1)
    if tipo is None:
        tipo = ler_tipo_ordem()
    preco = ler_float("Preço unitário: R$ ", valor_minimo=0.01)
    quantidade = ler_inteiro("Quantidade: ", valor_minimo=1)
    timestamp = gerar_timestamp()
    return Order(id=id_ordem, tipo=tipo, preco=preco, quantidade=quantidade, timestamp=timestamp)


def exibir_cabecalho():
    print("\n" + "=" * 54)
    print("SIMULADOR DE LIVRO DE OFERTAS")
    print("Estrutura de Dados em Python")
    print("=" * 54)


def exibir_menu():
    print("\nEscolha uma opção:")
    print("1 - Inserir ordem de compra")
    print("2 - Inserir ordem de venda")
    print("3 - Processar próxima ordem da fila")
    print("4 - Processar todas as ordens da fila")
    print("5 - Mostrar livro de compras")
    print("6 - Mostrar livro de vendas")
    print("7 - Mostrar transações realizadas")
    print("8 - Desfazer última ordem inserida no livro")
    print("0 - Sair")


def menu():
    livro = OrderBook()

    while True:
        exibir_cabecalho()
        exibir_menu()
        opcao = input("\nOpção: ").strip()

        if opcao == "1":
            ordem = ler_ordem(tipo="C")
            livro.add_order(ordem)
        elif opcao == "2":
            ordem = ler_ordem(tipo="V")
            livro.add_order(ordem)
        elif opcao == "3":
            livro.process_next_order()
        elif opcao == "4":
            livro.process_all_orders()
        elif opcao == "5":
            livro.show_buy_orders()
        elif opcao == "6":
            livro.show_sell_orders()
        elif opcao == "7":
            livro.show_transactions()
        elif opcao == "8":
            livro.undo_last_order()
        elif opcao == "0":
            print("\nSistema encerrado.")
            break
        else:
            print("\nOpção inválida. Escolha uma opção do menu.")

        input("\nPressione ENTER para continuar...")


def main():
    menu()


if __name__ == "__main__":
    main()
