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

class OrderBook:
    def __init__(self):
        # Inicializa a fila de entrada e os livros usando encadeamento manual
        self.fila_entrada = Queue()
        self.compras = ListaDuplamenteEncadeada(tipo_lista="compra") # ordenado decrescente
        self.vendas = ListaDuplamenteEncadeada(tipo_lista="venda")   # ordenado crescente
        self.pilha_undo = Pilha()
        self.transacoes = []

    def adicionar_ordem(self, order):
        #Coloca a ordem diretamente na fila de entrada.
        self.fila_entrada.inserir(order)
        print(f"Ordem {order.id} ({order.tipo.upper()}) recebida e adicionada à fila.")

    def processar_proxima(self):
        #Retira a primeira ordem da fila(que foi adicionada mais antigamente) 
        #e envia para o motor de match
        if self.fila_entrada.vazio():
            print("Fila de entrada vazia. Nenhuma ordem para processar.")
            return False
        
        proxima = self.fila_entrada.remover()
        print(f"\nRetirando ordem {proxima.id} da fila e executando match...")
        self.casar_ordem(proxima)
        return True

    def processar_todas(self):
        #Mesma logica do processar proxima, mas abrange todas as ordens
        enquanto_houver_ordens = True
        while enquanto_houver_ordens:
            #Usamos o processar proxima para o processar todas
            enquanto_houver_ordens = self.processar_proxima()

    def casar_ordem(self, ordem_atual):
 
        # match quando o preço de compra >= preço de venda.
        
        if ordem_atual.tipo == "compra":
            # Tenta casar com as melhores ofertas de venda disponíveis
            while ordem_atual.quantidade > 0 and not self.vendas.vazia():
                melhor_venda = self.vendas.obter_topo()
                
                # Preço de compra deve ser >= ao preço de venda
                if ordem_atual.preco >= melhor_venda.preco:
                    # Pega a menor quantidade entre quem quer vender e quem quer comprar
                    qtd_negociada = min(ordem_atual.quantidade, melhor_venda.quantidade)
                    
                    # Gera a transação usando o preço de quem já estava no livro
                    nova_transacao = Transacao(
                        id_compra=ordem_atual.id,
                        id_venda=melhor_venda.id,
                        preco=melhor_venda.preco,
                        quantidade=qtd_negociada
                    )
                    self.transacoes.append(nova_transacao)
                    print(f"NÉGOCIO FECHADO! {qtd_negociada} un. negociadas a R$ {melhor_venda.preco:.2f}")
                    
                    # Atualiza os saldos das ordens
                    ordem_atual.quantidade -= qtd_negociada
                    melhor_venda.quantidade -= qtd_negociada
                    
                    # Se a ordem do livro zerou, remove ela da lista 
                    if melhor_venda.quantidade == 0:
                        self.vendas.remover_topo()
                else:
                    # Preço da melhor venda está acima do que aceitamos pagar, então nenhuma das ordens serve
                    break
            
            # Se ainda sobrou quantidade na compra, insere o saldo no livro
            if ordem_atual.quantidade > 0:
                self.compras.inserir_ordenado(ordem_atual)
                self.pilha_undo.empilhar(ordem_atual.id) # Guarda o ID no undo caso precise reverter

        elif ordem_atual.tipo == "venda":
            # Tenta casar com as melhores ofertas de compra
            while ordem_atual.quantidade > 0 and not self.compras.vazia():
                melhor_compra = self.compras.obter_topo()
                
                # Preço de compra >= preço de venda
                if melhor_compra.preco >= ordem_atual.preco:
                    qtd_negociada = min(melhor_compra.quantidade, ordem_atual.quantidade)
                    
                    # Preço determinado por quem já estava esperando no livro
                    nova_transacao = Transacao(
                        id_compra=melhor_compra.id,
                        id_venda=ordem_atual.id,
                        preco=melhor_compra.preco,
                        quantidade=qtd_negociada
                    )
                    self.transacoes.append(nova_transacao)
                    print(f"NEGÓCIO FECHADO! {qtd_negociada} un. negociadas a R$ {melhor_compra.preco:.2f}")
                    
                    # Atualiza os saldos
                    ordem_atual.quantidade -= qtd_negociada
                    melhor_compra.quantidade -= qtd_negociada
                    
                    if melhor_compra.quantidade == 0:
                        self.compras.remover_topo()
                else:
                    # Melhor compra do livro paga menos do que aceitamos vender
                    break
            
            # Se sobrou saldo da venda, guarda no livro
            if ordem_atual.quantidade > 0:
                self.vendas.inserir_ordenado(ordem_atual)
                self.pilha_undo.empilhar(ordem_atual.id)

    def exibir_livros(self):
        #Placar da "Bolsa Eletrônica"
        print("\n <<<< LIVRO DE OFERTAS ATUALIZADO >>>> ")
        print(" COMPRAS (Preços Decrescentes) ")
        self.compras.exibir()
        print(" VENDAS (Preços Crescentes) ")
        self.vendas.exibir()

    def exibir_transacoes(self):
        # Mostra todas as ordens que foram negociadas
        print("\n<<<< HISTÓRICO DE NEGOCIAÇÕES >>>>")
        if not self.transacoes:
            print("  Nenhuma transação efetuada até o momento.")
        for t in self.transacoes:
            print(f"  {t}")


class ListaDuplamenteEncadeada:
    # é o orderbook real
    def __init__(self, tipo_lista):
        self.head = None
        self.tail = None
        self.tipo_lista = tipo_lista

    def vazia(self):
        return self.head is None

    def obter_topo(self):
        return self.head.order if self.head else None

    def remover_topo(self):
        if self.vazia():
            return
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None

    def inserir_ordenado(self, order):
        #Insere a ordem na posição exata quando ela não encontra um par imediato
        novo_no = Node(order)
        if self.vazia():
            self.head = self.tail = novo_no
            return

        atual = self.head
        if self.tipo_lista == "compra":
            while atual and atual.order.preco >= order.preco:
                atual = atual.next
        else:
            while atual and atual.order.preco <= order.preco:
                atual = atual.next

        if atual == self.head:
            novo_no.next = self.head
            self.head.prev = novo_no
            self.head = novo_no
        elif atual is None:
            self.tail.next = novo_no
            novo_no.prev = self.tail
            self.tail = novo_no
        else:
            novo_no.next = atual
            novo_no.prev = atual.prev
            atual.prev.next = novo_no
            atual.prev = novo_no

    def exibir(self):
        if self.vazia():
            print("Vazio")
            return
        atual = self.head
        while atual:
            print(f"  {atual.order}")
            atual = atual.next


class Pilha:
    # Guarda os IDs na posição que foram inseridos,
    # permitindo desfazer a última operação
    def __init__(self):
        self.topo = None

    def empilhar(self, id_ordem):
        novo_no = Node(id_ordem)
        if self.topo:
            novo_no.next = self.topo
        self.topo = novo_no


class Transacao:
    #Funciona como um recbo da transação
    def __init__(self, id_compra, id_venda, preco, quantidade):
        self.id_compra = id_compra
        self.id_venda = id_venda
        self.preco = preco
        self.quantidade = quantidade

    def __str__(self):
        return f"TRATO FEITO! Compra #{self.id_compra} casou com Venda #{self.id_venda} | Qtd: {self.quantidade} | Preço: R$ {self.preco:.2f}"


if __name__ == "__main__":
    livro = OrderBook()
    livro.adicionar_ordem(Order(id=1, tipo="compra", preco=45.50, quantidade=10))
    livro.adicionar_ordem(Order(id=2, tipo="compra", preco=47.00, quantidade=5))
    livro.adicionar_ordem(Order(id=3, tipo="venda", preco=52.00, quantidade=10))
    livro.processar_todas()
    livro.exibir_livros()
    livro.adicionar_ordem(Order(id=4, tipo="venda", preco=46.00, quantidade=12))
    livro.processar_todas()
    livro.exibir_livros()
    livro.exibir_transacoes()

