# ==================================================
# SIMULADOR DE LIVRO DE OFERTAS
# Disciplina: Estrutura de Dados em Python
# Integrantes: Eduardo, Felipe, Fernando, Nicolas e Victor
#
# PARTE 3 - TRANSAÇÕES
# Responsável: Nicolas
# Commit: docs: adiciona transacoes
#
# Esta parte registra as transações realizadas pelo motor de match.
# Uma transação é criada sempre que uma ordem de compra e uma ordem
# de venda são casadas, total ou parcialmente.
# ==================================================

from datetime import datetime


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


class NodeTransaction:
    """
    Nó interno da lista encadeada usada pelo TransactionHistory.

    Encapsula um objeto Transaction e mantém o ponteiro para o próximo nó,
    permitindo o encadeamento manual sem uso de estruturas nativas.

    Atributos:
        data (Transaction): A transação armazenada neste nó.
        next (NodeTransaction | None): Ponteiro para o próximo nó da cadeia.
    """

    def __init__(self, data: Transaction):
        """
        Inicializa o nó com a transação fornecida e ponteiro nulo.

        Complexidade: O(1).
        """
        self.data = data
        self.next = None


class TransactionHistory:
    """
    Histórico de transações implementado como lista encadeada simples.

    Armazena de forma ordenada (cronológica) todas as transações geradas
    pelo motor de match, sem utilizar listas nativas do Python.

    A inserção é feita sempre no final da cadeia (append), preservando
    a ordem de chegada. A exibição percorre a cadeia do início ao fim.

    Atributos:
        head (NodeTransaction | None): Primeiro nó da cadeia (transação mais antiga).
        tail (NodeTransaction | None): Último nó da cadeia (transação mais recente).
    """

    def __init__(self):
        """
        Inicializa o histórico vazio.

        Complexidade: O(1).
        """
        self.head = None
        self.tail = None

    def add(self, transaction: Transaction):
        """
        Insere uma nova transação no final do histórico.

        Preserva a ordem cronológica: a transação mais antiga fica no início
        da cadeia e a mais recente sempre no final.

        Args:
            transaction (Transaction): O objeto da transação a ser registrada.

        Complexidade: O(1).
        """
        no = NodeTransaction(transaction)

        # Caso Base: histórico vazio
        if self.head is None:
            self.head = no
            self.tail = no
            return

        # Caso Geral: encadeia ao final
        self.tail.next = no
        self.tail = no

    def is_empty(self):
        """
        Verifica se o histórico está vazio.

        Returns:
            bool: True se não houver nenhuma transação registrada, False caso contrário.

        Complexidade: O(1).
        """
        return self.head is None

    def show(self):
        """
        Percorre o histórico e exibe todas as transações no terminal.

        Utiliza o __str__ de cada Transaction para formatar a saída.
        Se o histórico estiver vazio, exibe uma mensagem informativa.

        Complexidade: O(n), onde n é o número de transações registradas.
        """
        if self.is_empty():
            print("  Nenhuma transação efetuada até o momento.")
            return

        ponteiro = self.head
        while ponteiro:
            print(f"  {ponteiro.data}")
            ponteiro = ponteiro.next
