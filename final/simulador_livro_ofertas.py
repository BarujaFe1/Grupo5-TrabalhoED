# ==================================================
# SIMULADOR DE LIVRO DE OFERTAS
# Disciplina: Estrutura de Dados em Python
# Integrantes: Eduardo, Felipe, Fernando, Nicolas e Victor
#
# Arquivo final integrado do projeto.
# Contém todas as partes do simulador unificadas em um único arquivo.
# ==================================================

from datetime import datetime


# ==================================================
# PARTE 1 - CLASSES BASE E LISTA DUPLAMENTE ENCADEADA
# Responsável: Eduardo
# Commit: feat: implementa classes base e lista duplamente encadeada
# ==================================================

class Order:
    """
    Representa uma ordem de negociação no sistema (Livro de Ofertas).

    Esta classe atua apenas como a estrutura de dados
    que transitará entre a Fila de Entrada e o Livro de Ofertas.
    """
    def __init__(self, id: int, tipo: str, preco: float, quantidade: int, timestamp):
        self.id = id
        self.tipo = tipo
        self.preco = preco
        self.quantidade = quantidade
        self.timestamp = timestamp

    def __str__(self):
        """Formata a ordem para exibição no terminal."""
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
    """
    Nó da Lista Duplamente Encadeada.

    Encapsula o objeto Order e mantém os ponteiros de navegação (next e prev)
    necessários para a estruturação da lista.
    """
    def __init__(self, data: Order):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """
    Implementação de uma Lista Duplamente Encadeada.

    Gerencia as inserções ordenadas e remoções de ordens (nós) manipulando
    referências de memória manualmente, sem depender de estruturas nativas.
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def insercao_ordenada(self, ordem: Order):
        """
        Insere uma nova ordem na lista com complexidade O(n).

        A lógica de ordenação respeita o tipo da ordem:
        - Compras ('C'): Ordem decrescente (maior preço no topo).
        - Vendas ('V'): Ordem crescente (menor preço no topo).

        Args:
            ordem (Order): O objeto da ordem a ser inserido no livro.
        """
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

    def remover(self, ordem: Order):
        """
        Busca e remove uma ordem específica com base no seu ID.

        Args:
            ordem (Order): Objeto contendo o ID alvo para cancelamento.

        Returns:
            bool: True se a ordem foi encontrada e removida, False caso contrário.
        """
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

    def busca(self, id_ordem: int):
        """
        Realiza uma busca linear (O(n)) na lista por um ID específico.

        Args:
            id_ordem (int): O identificador numérico da ordem buscada.

        Returns:
            Order/bool: Retorna o objeto Order se encontrado, ou False se não existir.
        """
        if self.head is None:
            return False

        ponteiro = self.head
        while ponteiro:
            if ponteiro.data.id == id_ordem:
                return ponteiro.data
            ponteiro = ponteiro.next
        return False

    def exibir(self):
        """Percorre a lista O(n) exibindo os dados de cada nó no terminal."""
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
        """Verifica se a lista está vazia. Complexidade: O(1)."""
        return self.head is None

    def obter_topo(self):
        """Retorna o dado do primeiro nó sem remover. Complexidade: O(1)."""
        if self.head is None:
            return None
        return self.head.data

    def remover_topo(self):
        """Remove o primeiro nó da lista. Complexidade: O(1)."""
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
    """Nó interno para a fila encadeada."""
    __slots__ = ('data', 'next')

    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    """
    Fila (FIFO) implementada manualmente com nós encadeados.

    Operações de extremidade em O(1):
    - enqueue: insere no final.
    - dequeue: remove do início.
    - peek: consulta o início sem remover.
    - is_empty: verifica se a fila está vazia.
    """

    def __init__(self):
        self._front = None
        self._rear = None

    def enqueue(self, data):
        """Insere um elemento no final da fila. Complexidade: O(1)."""
        node = _QueueNode(data)
        if self._rear is None:
            self._front = node
            self._rear = node
        else:
            self._rear.next = node
            self._rear = node

    def dequeue(self):
        """Remove e retorna o elemento do início da fila. Complexidade: O(1)."""
        if self._front is None:
            return None
        data = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        return data

    def peek(self):
        """Retorna o elemento do início sem remover. Complexidade: O(1)."""
        if self._front is None:
            return None
        return self._front.data

    def is_empty(self):
        """Verifica se a fila está vazia. Complexidade: O(1)."""
        return self._front is None

    inserir = enqueue
    remover = dequeue
    vazio = is_empty


class _StackNode:
    """Nó interno para a pilha encadeada."""
    __slots__ = ('data', 'next')

    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    """
    Pilha (LIFO) implementada manualmente com nós encadeados.

    Operações de extremidade em O(1):
    - push: insere no topo.
    - pop: remove do topo.
    - peek: consulta o topo sem remover.
    - is_empty: verifica se a pilha está vazia.
    """

    def __init__(self):
        self._top = None

    def push(self, data):
        """Insere um elemento no topo da pilha. Complexidade: O(1)."""
        node = _StackNode(data)
        node.next = self._top
        self._top = node

    def pop(self):
        """Remove e retorna o elemento do topo da pilha. Complexidade: O(1)."""
        if self._top is None:
            return None
        data = self._top.data
        self._top = self._top.next
        return data

    def peek(self):
        """Retorna o elemento do topo sem remover. Complexidade: O(1)."""
        if self._top is None:
            return None
        return self._top.data

    def is_empty(self):
        """Verifica se a pilha está vazia. Complexidade: O(1)."""
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
    Representa uma transação realizada entre uma ordem de compra e uma ordem de venda.

    Uma transação é gerada pelo motor de match (OrderBook) no momento em que
    o preço de compra é maior ou igual ao preço de venda, permitindo o negócio.

    A transação registra:
    - Qual ordem de compra participou do negócio (id_compra)
    - Qual ordem de venda participou do negócio (id_venda)
    - O preço pelo qual o negócio foi executado (preco)
    - A quantidade de ativos negociados (quantidade)
    - O momento exato em que o negócio ocorreu (timestamp)

    O preço de execução é sempre o preço de quem já estava no livro de ofertas,
    respeitando a prioridade de quem chegou primeiro ao mercado.

    Atributos:
        id_compra (int): ID da ordem de compra envolvida na transação.
        id_venda (int): ID da ordem de venda envolvida na transação.
        preco (float): Preço unitário pelo qual o negócio foi executado.
        quantidade (int): Quantidade de ativos negociados nesta transação.
        timestamp (str): Data e hora em que a transação foi registrada.
    """

    def __init__(self, id_compra: int, id_venda: int, preco: float, quantidade: int):
        """
        Inicializa uma nova transação com os dados do negócio realizado.

        O timestamp é gerado automaticamente no momento da criação,
        registrando o instante exato do fechamento do negócio.

        Complexidade: O(1).
        """
        self.id_compra = id_compra
        self.id_venda = id_venda
        self.preco = float(preco)
        self.quantidade = int(quantidade)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        """
        Retorna uma representação legível da transação para exibição no terminal.

        Exemplo de saída:
        [2024-01-15 10:32:47] NEGÓCIO FECHADO | Compra #3 x Venda #7 | Qtd: 5 | Preço: R$ 48.00

        Complexidade: O(1).
        """
        return (
            f"[{self.timestamp}] NEGÓCIO FECHADO | "
            f"Compra #{self.id_compra} x Venda #{self.id_venda} | "
            f"Qtd: {self.quantidade} | "
            f"Preço: R$ {self.preco:.2f}"
        )


class _TransactionNode:
    """Nó interno para o histórico encadeado de transações."""
    __slots__ = ('data', 'next')

    def __init__(self, data):
        self.data = data
        self.next = None


class TransactionHistory:
    """
    Histórico de transações implementado como lista encadeada simples.

    Evita o uso de list() para a estrutura principal de armazenamento
    de transações, atendendo ao requisito do enunciado.
    """

    def __init__(self):
        self._head = None

    def add(self, transaction):
        """Adiciona uma transação ao histórico. Complexidade: O(1)."""
        node = _TransactionNode(transaction)
        node.next = self._head
        self._head = node

    def show(self):
        """Exibe todas as transações do histórico. Complexidade: O(n)."""
        if self._head is None:
            print("  Nenhuma transação efetuada até o momento.")
            return
        current = self._head
        while current:
            print(f"  {current.data}")
            current = current.next

    def is_empty(self):
        """Verifica se o histórico está vazio. Complexidade: O(1)."""
        return self._head is None

    def __iter__(self):
        """Permite iterar sobre as transações do histórico."""
        current = self._head
        while current:
            yield current.data
            current = current.next


Transacao = Transaction
Pilha = Stack


# ==================================================
# PARTE 4 - LIVRO DE OFERTAS E MOTOR DE MATCH
# Responsável: Victor
# Commit: feat: implementa livro de ofertas e motor de match
# ==================================================

class OrderBook:
    """
    Livro de Ofertas com motor de casamento (match).

    Integra:
    - Fila de entrada (Queue)
    - Lista de compras (DoublyLinkedList, ordem decrescente)
    - Lista de vendas (DoublyLinkedList, ordem crescente)
    - Pilha de undo (Stack)
    - Histórico de transações (TransactionHistory)
    """

    def __init__(self):
        self.fila_entrada = Queue()
        self.compras = DoublyLinkedList()
        self.vendas = DoublyLinkedList()
        self.pilha_undo = Stack()
        self.transacoes = TransactionHistory()

    def add_order(self, order):
        """Coloca a ordem na fila de entrada. Complexidade: O(1)."""
        self.fila_entrada.enqueue(order)
        print(f"Ordem {order.id} ({order.tipo.upper()}) recebida e adicionada à fila.")

    def process_next_order(self):
        """
        Remove a ordem mais antiga da fila e executa o motor de match.

        Returns:
            bool: True se processou uma ordem, False se fila vazia.
        """
        if self.fila_entrada.is_empty():
            print("Fila de entrada vazia. Nenhuma ordem para processar.")
            return False

        ordem = self.fila_entrada.dequeue()
        print(f"\nRetirando ordem {ordem.id} da fila e executando match...")
        self.match_order(ordem)
        return True

    def process_all_orders(self):
        """Processa todas as ordens da fila de entrada."""
        while self.process_next_order():
            pass

    def match_order(self, ordem_atual):
        """
        Motor de casamento de ordens.

        Match ocorre quando preço de compra >= preço de venda.

        - Se for compra, casa com a melhor venda.
        - Se for venda, casa com a melhor compra.
        - Em match total, a ordem zerada é removida do livro.
        - Em match parcial, a quantidade restante fica no livro.
        - Se sobrar saldo da ordem atual, insere no livro correspondente.
        - Toda transação é registrada no histórico.

        Args:
            ordem_atual (Order): Ordem retirada da fila para processamento.
        """
        tipo = ordem_atual.tipo.strip().upper()

        if tipo == 'C':
            while ordem_atual.quantidade > 0 and not self.vendas.vazia():
                melhor_venda = self.vendas.obter_topo()

                if ordem_atual.preco >= melhor_venda.preco:
                    qtd_negociada = min(ordem_atual.quantidade, melhor_venda.quantidade)

                    transacao = Transaction(
                        id_compra=ordem_atual.id,
                        id_venda=melhor_venda.id,
                        preco=melhor_venda.preco,
                        quantidade=qtd_negociada
                    )
                    self.transacoes.add(transacao)
                    print(f"NEGÓCIO FECHADO! {qtd_negociada} un. negociadas a R$ {melhor_venda.preco:.2f}")

                    ordem_atual.quantidade -= qtd_negociada
                    melhor_venda.quantidade -= qtd_negociada

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
                    qtd_negociada = min(melhor_compra.quantidade, ordem_atual.quantidade)

                    transacao = Transaction(
                        id_compra=melhor_compra.id,
                        id_venda=ordem_atual.id,
                        preco=melhor_compra.preco,
                        quantidade=qtd_negociada
                    )
                    self.transacoes.add(transacao)
                    print(f"NEGÓCIO FECHADO! {qtd_negociada} un. negociadas a R$ {melhor_compra.preco:.2f}")

                    ordem_atual.quantidade -= qtd_negociada
                    melhor_compra.quantidade -= qtd_negociada

                    if melhor_compra.quantidade == 0:
                        self.compras.remover_topo()
                else:
                    break

            if ordem_atual.quantidade > 0:
                self.vendas.insercao_ordenada(ordem_atual)
                self.pilha_undo.push(ordem_atual.id)

    def show_buy_orders(self):
        """Exibe o livro de compras (preços decrescentes)."""
        print("\n <<<< LIVRO DE COMPRAS (Preços Decrescentes) >>>>")
        self.compras.exibir()

    def show_sell_orders(self):
        """Exibe o livro de vendas (preços crescentes)."""
        print("\n <<<< LIVRO DE VENDAS (Preços Crescentes) >>>>")
        self.vendas.exibir()

    def show_transactions(self):
        """Exibe o histórico de transações realizadas."""
        print("\n<<<< HISTÓRICO DE NEGOCIAÇÕES >>>>")
        self.transacoes.show()

    def undo_last_order(self):
        """
        Desfaz a última ordem inserida no livro (compras ou vendas).

        Remove a ordem correspondente ao ID no topo da pilha de undo.
        """
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
    """
    Gera o timestamp da ordem no momento do cadastro.

    Complexidade: O(1).
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ler_inteiro(mensagem, valor_minimo=None):
    """
    Lê um número inteiro com validação.

    Usado para ID e quantidade da ordem.
    """
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
    """
    Lê um número decimal com validação.

    Aceita vírgula ou ponto como separador decimal.
    """
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
    """
    Lê e valida o tipo da ordem.

    C = Compra
    V = Venda
    """
    while True:
        tipo = input("Tipo da ordem [C = Compra | V = Venda]: ").strip().upper()

        if tipo in ("C", "V"):
            return tipo

        print("Tipo inválido. Digite apenas C para compra ou V para venda.")


def ler_ordem(tipo=None):
    """
    Lê os dados de uma nova ordem pelo terminal.

    Se o tipo já vier informado pelo menu, não pergunta novamente.
    """
    print("\n--- Cadastro de nova ordem ---")

    id_ordem = ler_inteiro("ID da ordem: ", valor_minimo=1)

    if tipo is None:
        tipo = ler_tipo_ordem()

    preco = ler_float("Preço unitário: R$ ", valor_minimo=0.01)
    quantidade = ler_inteiro("Quantidade: ", valor_minimo=1)
    timestamp = gerar_timestamp()

    return Order(
        id=id_ordem,
        tipo=tipo,
        preco=preco,
        quantidade=quantidade,
        timestamp=timestamp
    )


def exibir_cabecalho():
    """
    Exibe o cabeçalho do sistema.
    """
    print("\n" + "=" * 54)
    print("SIMULADOR DE LIVRO DE OFERTAS")
    print("Estrutura de Dados em Python")
    print("=" * 54)


def exibir_menu():
    """
    Exibe as opções principais do simulador.

    O menu é a interface de teste pelo terminal.
    Cada opção chama um método específico do livro de ofertas.
    """
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
    """
    Controla o fluxo principal do sistema.

    Responsabilidades:
    - Receber comandos do usuário.
    - Ler os dados de novas ordens.
    - Chamar os métodos correspondentes do OrderBook.
    - Manter o programa em execução até a opção sair.
    """
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
    """
    Função principal do simulador.
    """
    menu()


if __name__ == "__main__":
    main()
