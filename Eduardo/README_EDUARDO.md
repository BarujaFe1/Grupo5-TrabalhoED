# Parte 1 - Classes Base e Lista Duplamente Encadeada (Responsável: Eduardo Affonso Boide Santos - RA: 16862544)

Esta seção do sistema é responsável por modelar os dados fundamentais do domínio financeiro (Ordem e Nó) e a estrutura de dados principal do livro de ofertas: a **Lista Duplamente Encadeada Ordenada** (`DoublyLinkedList`), implementada do zero por meio de referências em memória.

## Estrutura das Classes

### 1. Order
Representa as ordens de negociação criadas e inseridas no livro.
```python
class Order:
    def __init__(self, id: int, tipo: str, preco: float, quantidade: int, timestamp: datetime):
        self.id = id           # Identificador numérico único
        self.tipo = tipo       # 'C' para Compra ou 'V' para Venda
        self.preco = preco     # Valor unitário aceito na negociação
        self.quantidade = qty  # Quantidade de ações
        self.timestamp = time  # Registro temporal do cadastro no terminal
```

### 2. Node
Elemento dinâmico de encadeamento da lista que encapsula um objeto `Order`.
```python
class Node:
    def __init__(self, data: Order):
        self.data = data  # Referência ao objeto Order
        self.prev = None  # Ponteiro para o nó anterior
        self.next = None  # Ponteiro para o próximo nó
```

### 3. DoublyLinkedList
Lista encadeada ordenada de duas vias para compras e vendas ativas.
*   **Inserção Ordenada (`insert_ordered`)**: 
    *   **Compras (`'C'`)**: Ordenadas de forma **decrescente** por preço (melhor comprador no início).
    *   **Vendas (`'V'`)**: Ordenadas de forma **crescente** por preço (melhor vendedor no início).
    *   **Prioridade Temporal (FIFO)**: Se o preço de duas ordens for idêntico, a comparação estrita (`>` ou `<`) garante que o novo nó seja inserido atrás das ordens mais antigas, preservando o tempo de chegada.
*   **Remoção por ID (`remove_by_id`)**: Varre a lista em busca do ID da ordem para desfazer e reconecta as referências dos nós adjacentes, liberando o nó da memória sem perder os ponteiros da lista.
*   **Acesso e Remoção de Topo (`obter_topo` / `remover_topo`)**: Permite ao motor de match ler e remover o nó de melhor preço instantaneamente em **$O(1)$**.

## Como se integra com o resto do sistema
O módulo é a base do simulador. O `OrderBook` (desenvolvido pelo Victor) instancia os livros de compra e venda como duas instâncias de `DoublyLinkedList`:
```python
self.buy_orders = DoublyLinkedList()   # Livro de Compras
self.sell_orders = DoublyLinkedList()  # Livro de Vendas
```
No cruzamento de ordens do motor, o Victor lê `obter_topo()` e remove as ordens liquidadas com `remover_topo()`. A remoção cirúrgica por ID (`remove_by_id`) é acionada pela funcionalidade de *undo* do motor de negociação.

## Análise de Complexidade Assintótica

| Operação | Complexidade | Justificativa |
| :--- | :--- | :--- |
| `insert_ordered` | $O(n)$ | Varredura linear na lista para encontrar a posição de preço correspondente. |
| `remove_by_id` | $O(n)$ | Busca linear pelo ID antes do religamento dos ponteiros adjacentes. |
| `busca` | $O(n)$ | Varredura sequencial a partir do ponteiro `head`. |
| `obter_topo` | $O(1)$ | Retorna diretamente o ponteiro de leitura da cabeça (`head`). |
| `remover_topo` | $O(1)$ | Avança o ponteiro `head` para o próximo elemento e remove a referência anterior. |
| `is_empty` | $O(1)$ | Verifica se `self.head` é nulo. |
