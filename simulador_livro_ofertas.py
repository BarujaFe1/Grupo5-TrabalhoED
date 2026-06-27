# ==================================================
# SIMULADOR DE LIVRO DE OFERTAS
# Disciplina: Estrutura de Dados em Python
# Integrantes:
#   - Eduardo Affonso Boide Santos – RA: 16862544
#   - Fernando Lacerda Dantas – RA: 17097341
#   - Felipe Alirio Baruja – RA: 15636442
#   - Nicolas Gonçalves Follone – RA: 16827586
#   - Victor Hugo Aparecido Galho Trasancos – RA: 16839040
#
# Arquivo unificado contendo os códigos individuais integrados.
# ==================================================

from datetime import datetime

# ==================================================
# PARTE 1 - CLASSES BASE E LISTA DUPLAMENTE ENCADEADA
# Responsável: Eduardo Affonso Boide Santos – RA: 16862544
# ==================================================

class Order:
    """
    Representa uma ordem de negociação no sistema (Livro de Ofertas).
    
    Esta classe atua apenas como a estrutura de dados 
    que transitará entre a Fila de Entrada e o Livro de Ofertas.
    """
    def __init__(self, id: int, tipo: str, preco: float, quantidade: int, timestamp: datetime):
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

    def insert_ordered(self, ordem:Order):
        """
        Insere uma nova ordem na lista com complexidade O(n).
        
        A lógica de ordenação respeita o tipo da ordem:
        - Compras ('C'): Ordem decrescente (maior preço no topo).
        - Vendas ('V'): Ordem crescente (menor preço no topo).
        
        Args:
            ordem (Order): O objeto da ordem a ser inserido no livro.
        """
        no = Node(ordem)

        # Caso Base: Inserção em lista vazia
        if self.head == None:
            self.head = no
            self.tail = no
            return
        
        # Fluxo para Lista de Compras (Ordem Decrescente de Preço)
        if no.data.tipo == 'C':
            
            # Cenário 1: Inserção no início (novo maior preço)
            if no.data.preco > self.head.data.preco:
                self.head.prev = no
                no.next = self.head
                self.head = no
                return

            # Cenário 2: Custo O(n) para inserção no meio
            ponteiro = self.head
            while ponteiro:
                # O uso de '>' estrito garante a prioridade temporal (FIFO).
                # Em caso de preços iguais, a nova ordem avança, ficando atrás da mais antiga.
                if no.data.preco > ponteiro.data.preco:
                    # Amarra os ponteiros do novo nó
                    no.next = ponteiro
                    no.prev = ponteiro.prev
                    # Atualiza os ponteiros dos vizinhos (religamento)
                    ponteiro.prev.next = no
                    ponteiro.prev = no
                    return
                ponteiro = ponteiro.next

            # Cenário 3: Inserção no final (novo menor preço de compra)
            no.prev = self.tail
            self.tail.next = no
            self.tail = no
        
        # Fluxo para Lista de Vendas (Ordem Crescente de Preço)
        else:
            
            # Cenário 1: Inserção no início (novo menor preço)
            if no.data.preco < self.head.data.preco:
                self.head.prev = no
                no.next = self.head
                self.head = no
                return
            
            # Cenário 2: Custo O(n) para inserção no meio
            ponteiro = self.head
            while ponteiro:
                # O uso de '<' estrito garante a prioridade temporal (FIFO).
                if no.data.preco < ponteiro.data.preco: #Desigualdade estrita mantém a prioridade de quem chegou primeiro
                    no.next = ponteiro
                    no.prev = ponteiro.prev
                    ponteiro.prev.next = no
                    ponteiro.prev = no
                    return
                ponteiro = ponteiro.next

            # Cenário 3: Inserção no final (novo maior preço de venda)
            no.prev = self.tail
            self.tail.next = no
            self.tail = no

    def remove_by_id(self, id_ordem: int):
        """
        Busca e remove uma ordem específica com base no seu ID (usado pelo sistema de Undo.
        
        Args:
            ordem (Order): Objeto contendo o ID alvo para cancelamento.
            
        Returns:
            bool: True se a ordem foi encontrada e removida, False caso contrário.
        """
        if self.head == None:
            return
        
        ponteiro = self.head
        while ponteiro:
            # A busca linear (O(n)) é feita comparando o ID único
            if ponteiro.data.id == id_ordem:

                # Cenário 1: Único elemento da lista
                if ponteiro == self.head and ponteiro == self.tail:
                    self.head = None
                    self.tail = None
                
                # Cenário 2: Remoção do primeiro nó (head)
                elif ponteiro == self.head:
                    self.head = ponteiro.next
                    self.head.prev = None
                
                # Cenário 3: Remoção do último nó (tail)
                elif ponteiro == self.tail:
                    self.tail = ponteiro.prev
                    self.tail.next = None
                
                # Cenário 4: Remoção de um nó no meio da estrutura
                else:
                    ponteiro.prev.next = ponteiro.next
                    ponteiro.next.prev = ponteiro.prev
                
                return True
            ponteiro = ponteiro.next
        return False

    def busca(self, id_ordem:int):
        """
        Realiza uma busca linear (O(n)) na lista por um ID específico.
        
        Args:
            id_ordem (int): O identificador numérico da ordem buscada.
            
        Returns:
            Order/bool: Retorna o objeto Order se encontrado, ou False se não existir.
        """
        if self.head == None:
            return False
        
        ponteiro = self.head
        while ponteiro:
            if ponteiro.data.id == id_ordem:
                return ponteiro.data
            ponteiro = ponteiro.next
        return False

    def display(self):
        """Percorre a lista O(n) exibindo os dados de cada nó formatados no terminal."""
        if self.head == None:
            print('Lista Vazia')
            return
        
        ponteiro = self.head
        while ponteiro:
            # Utiliza a formatação estruturada dos atributos do objeto Order
            print(f'ID:{ponteiro.data.id}, Tipo:{ponteiro.data.tipo}, Preço:{ponteiro.data.preco}, Quantidade:{ponteiro.data.quantidade}, Tempo:{ponteiro.data.timestamp}')
            ponteiro = ponteiro.next 


    #Funções adicionais necessárias para o OrderBook:
    
    def is_empty(self):
        """
        Verifica se a lista encadeada está vazia.
        
        Returns:
            bool: True se a lista estiver vazia, False caso contrário.
        """
        return self.head is None

    def obter_topo(self):
        """
        Retorna a ordem no topo da lista (o melhor preço) sem removê-la.
        
        Este método opera em tempo constante O(1), permitindo que o Motor de Match 
        verifique rapidamente os preços sem alterar a estrutura da lista.
        
        Returns:
            Order/bool: Retorna o objeto Order no topo, ou False se a lista estiver vazia.
        """
        if self.head is None:
            return False
        
        # Retorna apenas a carga útil (Order), blindando o Node interno
        return self.head.data

    def remover_topo(self):
        """
        Remove a ordem no topo da lista (o primeiro elemento).
        
        Utilizado pelo Motor de Match após uma transação ser concluída com sucesso.
        A operação é realizada em tempo constante O(1) através do religamento do head.
        
        Returns:
            bool: True se o topo foi removido com sucesso, False se a lista estava vazia.
        """
        if self.head is None:
            return False
        
        # Cenário 1: Se for o único nó da lista
        if self.head == self.tail:
            self.head = None
            self.tail = None
            return True
            
        # Cenário 2: Se a lista tiver mais de um elemento
        self.head = self.head.next
        self.head.prev = None
        
        return True


# ==================================================
# PARTE 2 - FILA ENCADEADA E PILHA DE UNDO
# Responsável: Fernando Lacerda Dantas – RA: 17097341
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
# Responsável: Nicolas Gonçalves Follone – RA: 16827586
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


# ==================================================
# PARTE 4 - LIVRO DE OFERTAS E MOTOR DE MATCH
# Responsável: Victor Hugo Aparecido Galho Trasancos – RA: 16839040
# ==================================================

class OrderBook:
    def __init__(self):
        # Inicializa a fila de entrada e os livros usando encadeamento manual
        self.fila_entrada = Queue()
        self.buy_orders = DoublyLinkedList() # ordenado decrescente
        self.sell_orders = DoublyLinkedList()   # ordenado crescente
        self.undo_stack = Stack()
        self.transactions = TransactionHistory()

    def add_order(self, order):
        # Coloca a ordem diretamente na fila de entrada.
        self.fila_entrada.enqueue(order)
        print(f"Ordem {order.id} ({order.tipo.upper()}) recebida e adicionada à fila.")

    def process_next_order(self):
        # Retira a primeira ordem da fila(que foi adicionada mais antigamente) 
        # e envia para o motor de match
        if self.fila_entrada.is_empty():
            print("Fila de entrada vazia. Nenhuma ordem para processar.")
            return False
        
        proxima = self.fila_entrada.dequeue()
        print(f"\nRetirando ordem {proxima.id} da fila e executing match...")
        self.match_order(proxima)
        return True

    def process_all_orders(self):
        # Mesma logica do processar proxima, mas abrange todas as ordens
        enquanto_houver_ordens = True
        while enquanto_houver_ordens:
            # Usamos o processar proxima para o processar todas
            enquanto_houver_ordens = self.process_next_order()

    def match_order(self, ordem_atual):
        # match quando o preço de compra >= preço de venda.
        
        if ordem_atual.tipo == "C":
            # Tenta casar com as melhores ofertas de venda disponíveis
            while ordem_atual.quantidade > 0 and not self.sell_orders.is_empty():
                melhor_venda = self.sell_orders.obter_topo()
                
                # Preço de compra deve ser >= ao preço de venda
                if ordem_atual.preco >= melhor_venda.preco:
                    # Pega a menor quantidade entre quem quer vender e quem quer comprar
                    qtd_negociada = min(ordem_atual.quantidade, melhor_venda.quantidade)
                    
                    # Gera a transação usando o preço de quem já estava no livro
                    nova_transacao = Transaction(
                        id_compra=ordem_atual.id,
                        id_venda=melhor_venda.id,
                        preco=melhor_venda.preco,
                        quantidade=qtd_negociada
                    )
                    self.transactions.add(nova_transacao)
                    print(f"NÉGOCIO FECHADO! {qtd_negociada} un. negociadas a R$ {melhor_venda.preco:.2f}")
                    
                    # Atualiza os saldos das ordens
                    ordem_atual.quantidade -= qtd_negociada
                    melhor_venda.quantidade -= qtd_negociada
                    
                    # Se a ordem do livro zerou, remove ela da lista 
                    if melhor_venda.quantidade == 0:
                        self.sell_orders.remover_topo()
                else:
                    # Preço da melhor venda está acima do que aceitamos pagar, então nenhuma das ordens serve
                    break
            
            # Se ainda sobrou quantidade na compra, insere o saldo no livro
            if ordem_atual.quantidade > 0:
                self.buy_orders.insert_ordered(ordem_atual)
                self.undo_stack.push(ordem_atual.id) # Guarda o ID no undo caso precise reverter

        elif ordem_atual.tipo == "V":
            # Tenta casar com as melhores ofertas de compra
            while ordem_atual.quantidade > 0 and not self.buy_orders.is_empty():
                melhor_compra = self.buy_orders.obter_topo()
                
                # Preço de compra >= preço de venda
                if melhor_compra.preco >= ordem_atual.preco:
                    qtd_negociada = min(melhor_compra.quantidade, ordem_atual.quantidade)
                    
                    # Preço determinado por quem já estava esperando no livro
                    nova_transacao = Transaction(
                        id_compra=melhor_compra.id,
                        id_venda=ordem_atual.id,
                        preco=melhor_compra.preco,
                        quantidade=qtd_negociada
                    )
                    self.transactions.add(nova_transacao)
                    print(f"NEGÓCIO FECHADO! {qtd_negociada} un. negociadas a R$ {melhor_compra.preco:.2f}")
                    
                    # Atualiza os saldos
                    ordem_atual.quantidade -= qtd_negociada
                    melhor_compra.quantidade -= qtd_negociada
                    
                    if melhor_compra.quantidade == 0:
                        self.buy_orders.remover_topo()
                else:
                    # Melhor compra do livro paga menos do que aceitamos vender
                    break
            
            # Se sobrou saldo da venda, guarda no livro
            if ordem_atual.quantidade > 0:
                self.sell_orders.insert_ordered(ordem_atual)
                self.undo_stack.push(ordem_atual.id)

    def undo_last_order(self):
        # Desfaz a última ordem inserida no livro de ofertas
        if self.undo_stack.is_empty():
            print("Nenhuma ordem para desfazer no livro.")
            return
        
        last_id = self.undo_stack.pop()
        # Tenta remover tanto do livro de compras quanto do de vendas
        if not self.buy_orders.remove_by_id(last_id):
            self.sell_orders.remove_by_id(last_id)
        print(f"Ordem {last_id} desfeita e removida do livro com sucesso.")

    def show_buy_orders(self):
        # Placar da "Bolsa Eletrônica" para compras
        print(" COMPRAS (Preços Decrescentes) ")
        self.buy_orders.display()

    def show_sell_orders(self):
        # Placar da "Bolsa Eletrônica" para vendas
        print(" VENDAS (Preços Crescentes) ")
        self.sell_orders.display()

    def show_transactions(self):
        # Mostra todas as ordens que foram negociadas
        print("\n<<<< HISTÓRICO DE NEGOCIAÇÕES >>>>")
        if self.transactions.is_empty():
            print("  Nenhuma transação efetuada até o momento.")
        else:
            self.transactions.show()


# ==================================================
# PARTE 5 - MENU PRINCIPAL E EXECUÇÃO DO SIMULADOR
# Responsável: Felipe Alirio Baruja – RA: 15636442
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


def mostrar_fila_entrada(livro):
    """Exibe as ordens na fila de entrada aguardando processamento."""
    print("\n <<<< FILA DE ENTRADA (Aguardando Processamento) >>>>")
    if livro.fila_entrada.is_empty():
        print("  Fila de entrada vazia.")
        return
    ponteiro = livro.fila_entrada._front
    while ponteiro:
        print(f"  {ponteiro.data}")
        ponteiro = ponteiro.next


def exibir_menu():
    print("\nEscolha uma opção:")
    print("1 - Inserir ordem de compra")
    print("2 - Inserir ordem de venda")
    print("3 - Mostrar fila de entrada")
    print("4 - Processar próxima ordem da fila")
    print("5 - Processar todas as ordens da fila")
    print("6 - Mostrar livro de compras")
    print("7 - Mostrar livro de vendas")
    print("8 - Mostrar transações realizadas")
    print("9 - Desfazer última ordem inserida no livro")
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
            mostrar_fila_entrada(livro)
        elif opcao == "4":
            livro.process_next_order()
        elif opcao == "5":
            livro.process_all_orders()
        elif opcao == "6":
            livro.show_buy_orders()
        elif opcao == "7":
            livro.show_sell_orders()
        elif opcao == "8":
            livro.show_transactions()
        elif opcao == "9":
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
