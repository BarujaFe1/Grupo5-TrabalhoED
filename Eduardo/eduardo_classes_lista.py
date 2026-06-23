from datetime import datetime

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

    def insercao_ordenada(self, ordem:Order):
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

    def remover(self, ordem:Order):
        """
        Busca e remove uma ordem específica com base no seu ID.
        
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
            if ponteiro.data.id == ordem.id:

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

    def exibir(self):
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
    
    def vazia(self) -> bool:
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