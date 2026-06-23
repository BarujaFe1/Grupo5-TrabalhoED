# PARTE 4 - LIVRO DE OFERTAS E MOTOR DE MATCH - Responsável: Victor

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
