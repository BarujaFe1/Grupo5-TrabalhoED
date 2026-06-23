# Parte 4 - Livro de Ofertas e Motor de Match (Responsável: Victor)

Esta seção do sistema funciona como o núcleo lógico do simulador, sendo estruturada através da classe `OrderBook`. Ela atua como o gerenciador do ciclo de vida das ordens de negociação, controlando os livros de ofertas e executando o cruzamento de preços (Motor de Match).

## Arquitetura e Estruturas Gerenciadas

A classe `OrderBook` integra e manipula as seguintes estruturas lineares desenvolvidas manualmente pelo grupo, respeitando a restrição de não utilizar estruturas nativas ou bibliotecas prontas do Python:

* **Fila de Entrada (`self.fila_entrada`):** Instância de `Queue` usada para recepção das ordens criadas pelo sistema.
* **Livro de Compras (`self.buy_orders`):** Instância de `DoublyLinkedList` que mantém as ofertas de compra ativas, ordenadas de forma **decrescente** por preço.
* **Livro de Vendas (`self.sell_orders`):** Instância de `DoublyLinkedList` que mantém as ofertas de venda ativas, ordenadas de forma **crescente** por preço.
* **Pilha de Desfazer (`self.undo_stack`):** Instância de `Stack` que registra exclusivamente os identificadores (`id`) das ordens que alteraram o estado dos livros, servindo de base para o mecanismo de *undo*.
* **Histórico (`self.transactions`):** Instância de `TransactionHistory` encarregada de armazenar de forma encadeada as transações executadas (`Transaction`) resultantes dos casamentos efetuados.

---

## Funcionalidades e Fluxo de Métodos

### 1. Recepção de Ordens
* **`add_order(order)`**: Consolida a entrada da ordem de negociação no sistema, inserindo-a diretamente no fim da fila de processamento (`self.fila_entrada`).

### 2. Controle de Fluxo
* **`process_next_order()`**: Remove o elemento mais antigo da fila de entrada (garantindo o comportamento FIFO) e o submete ao Motor de Match. Retorna `False` se a fila estiver vazia.
* **`process_all_orders()`**: Executa um laço de repetição condicional invocando `process_next_order()` de forma contínua até que o fluxo pendente seja totalmente esgotado.

### 3. O Motor de Match (`match_order`)
O método `match_order(ordem_atual)` implementa o algoritmo de precificação e cruzamento com base na regra de mercado: **Preço de Compra $\ge$ Preço de Venda**.

* **Identificação de Alvos:** Uma ordem do tipo `"C"` (Compra) busca o topo de `"sell_orders"`; uma ordem do tipo `"V"` (Venda) busca o topo de `"buy_orders"`.
* **Casamento Parcial ou Total:** O motor consome a quantidade disponível respeitando o volume limite entre a ordem atual e a que está no livro. Se a ordem mapeada no livro for zerada, ela é removida.
* **Precificação por Fila:** O preço de execução da `Transaction` gerada é determinado estritamente pela ordem que **já estava esperando no livro**.
* **Inserção de Remanescente:** Caso a ordem ingressante não seja totalmente preenchida, o saldo é inserido ordenadamente no respectivo livro e seu ID é registrado na `undo_stack`.

### 4. Mecanismo de Reversão (*Undo*)
* **`undo_last_order()`**: Remove a última ordem que entrou no livro de ofertas. Ele consome o ID presente no topo da `undo_stack` e realiza a remoção por ID utilizando o método correspondente nos livros de ofertas.

### 5. Exibição e Interface
* **`show_buy_orders()`**: Aciona a exibição formatada do livro de compras em ordem decrescente.
* **`show_sell_orders()`**: Aciona a exibição formatada do livro de vendas em ordem crescente.
* **`show_transactions()`**: Varre a estrutura `TransactionHistory` exibindo o histórico cronológico de todas as negociações consolidadas no terminal.
