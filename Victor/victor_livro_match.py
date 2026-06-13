# PARTE 4 - LIVRO DE OFERTAS E MOTOR DE MATCH - Responsável: Victor

class OrderBook:
    def __init__(self):
        # Inicializa a fila de entrada e os livros usando encadeamento manual
        self.fila_entrada = Queue()
        self.compras = ListaDuplamenteEncadeada(tipo_lista="compra") # ordenado decrescente
        self.vendas = ListaDuplamenteEncadeada(tipo_lista="venda")   # ordenado crescente
        self.pilha_undo = Pilha()
        self.transacoes = []

    def adicionar_ordem(self, order):
        # Coloca a ordem diretamente na fila de entrada.
        self.fila_entrada.inserir(order)
        print(f"Ordem {order.id} ({order.tipo.upper()}) recebida e adicionada à fila.")

    def processar_proxima(self):
        # Retira a primeira ordem da fila(que foi adicionada mais antigamente) 
        # e envia para o motor de match
        if self.fila_entrada.vazio():
            print("Fila de entrada vazia. Nenhuma ordem para processar.")
            return False
        
        proxima = self.fila_entrada.remover()
        print(f"\nRetirando ordem {proxima.id} da fila e executing match...")
        self.casar_ordem(proxima)
        return True

    def processar_todas(self):
        # Mesma logica do processar proxima, mas abrange todas as ordens
        enquanto_houver_ordens = True
        while enquanto_houver_ordens:
            # Usamos o processar proxima para o processar todas
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
        # Placar da "Bolsa Eletrônica"
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
