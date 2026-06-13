# Parte 4 - Livro de Ofertas e Motor de Match (Responsável: Victor)

Esta seção do sistema funciona como o núcleo lógico do simulador, sendo estruturada através da classe `OrderBook`. Ela atua como o gerenciador ciclo de vida das ordens de negociação, controlando os livros de ofertas e executando o cruzamento de preços (Motor de Match).

## Arquitetura e Estruturas Gerenciadas

A classe `OrderBook` integra e manipula as seguintes estruturas lineares desenvolvidas pelo grupo:

* **Fila de Entrada (`self.fila_entrada`):** Instância de `Queue` usada para recepção das ordens criadas pelo sistema.
* **Livro de Compras (`self.compras`):** Instância de `ListaDuplamenteEncadeada` que mantém as ofertas de compra ativas, ordenadas de forma **decrescente** por preço.
* **Livro de Vendas (`self.vendas`):** Instância de `ListaDuplamenteEncadeada` que mantém as ofertas de venda ativas, ordenadas de forma **crescente** por preço.
* **Pilha de Desfazer (`self.pilha_undo`):** Instância de `Pilha` que registra exclusivamente os (`id`) das ordens que alteraram o estado dos livros, servindo de base para o mecanismo de (*undo*).
* **Histórico (`self.transacoes`):** Coleção encarregada de armazenar as transações executadas (`Transacao`) resultantes dos casamentos efetuados.

---

##  Funcionalidades e Fluxo de Métodos

### 1. Recepção de Ordens
* **`adicionar_ordem(order)`**: Consolida a entrada da ordem de negociação no sistema, inserindo diretamente no fim da fila de processamento (`self.fila_entrada`).

### 2. Controle de Fluxo
* **`processar_proxima()`**: Remove o elemento mais antigo da fila de entrada (garantindo o comportamento FIFO) e o submete ao Motor de Match. 
* **`processar_todas()`**: Executa um laço de repetição condicional invocando `processar_proxima()` de forma contínua até que o fluxo pendente seja totalmente esgotado.

### 3. O Motor de Match (`casar_ordem`)
O método `casar_ordem(ordem_atual)` implementa o algoritmo de precificação e cruzamento com base na regra de mercado: **Preço de Compra $\ge$ Preço de Venda**.
