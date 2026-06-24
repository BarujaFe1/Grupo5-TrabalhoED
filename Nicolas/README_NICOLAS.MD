# Parte 3 - Transações (Responsável: Nicolas)

Esta seção do sistema é responsável pelo registro dos negócios fechados pelo motor de match. A classe `Transaction` funciona como um recibo imutável de cada operação concluída, e a classe `TransactionHistory` armazena todas as transações em uma lista encadeada manual, sem uso de listas nativas do Python.

## O que é uma transação

Uma transação é criada sempre que o motor de match (implementado pelo Victor) identifica que o preço de uma ordem de compra é maior ou igual ao preço de uma ordem de venda. Ela não toma nenhuma decisão — apenas registra o resultado do negócio.

## Estrutura das classes

### Transaction

```python
class Transaction:
    def __init__(self, id_compra, id_venda, preco, quantidade):
        self.id_compra  # ID da ordem de compra envolvida
        self.id_venda   # ID da ordem de venda envolvida
        self.preco      # Preço pelo qual o negócio foi executado
        self.quantidade # Quantidade de ativos negociados
        self.timestamp  # Momento exato do fechamento do negócio
```

O `timestamp` é gerado automaticamente no momento da criação da transação, sem precisar ser passado como parâmetro.

### NodeTransaction

Nó interno usado pelo `TransactionHistory`. Encapsula um objeto `Transaction` e mantém um ponteiro `next` para o próximo nó da cadeia.

```python
class NodeTransaction:
    def __init__(self, data: Transaction):
        self.data = data  # A transação armazenada
        self.next = None  # Ponteiro para o próximo nó
```

### TransactionHistory

Lista encadeada simples que armazena todas as transações em ordem cronológica, sem uso de `list` ou qualquer estrutura nativa do Python.

```python
class TransactionHistory:
    def __init__(self):
        self.head  # Primeiro nó (transação mais antiga)
        self.tail  # Último nó (transação mais recente)

    def add(transaction)    # Insere no final — O(1)
    def is_empty()          # Verifica se há transações — O(1)
    def show()              # Exibe todo o histórico no terminal — O(n)
```

A inserção é sempre no final da cadeia (`tail`), preservando a ordem de chegada. A exibição percorre a cadeia do `head` ao último nó.

## Como se integra com o resto do sistema

Quem usa as classes desta parte é o Victor, dentro do método `match_order` do `OrderBook`. O histórico é inicializado no construtor:

```python
self.transactions = TransactionHistory()
```

Sempre que um match ocorre, o Victor instancia uma transação e a adiciona ao histórico:

```python
nova_transacao = Transaction(
    id_compra=ordem_atual.id,
    id_venda=melhor_venda.id,
    preco=melhor_venda.preco,
    quantidade=qtd_negociada
)
self.transactions.add(nova_transacao)
```

O preço registrado é sempre o de quem já estava no livro de ofertas, respeitando a prioridade de chegada. Essa decisão é do motor de match — a `Transaction` apenas armazena o valor recebido.

O menu do Felipe chama:

```python
livro.show_transactions()
```

Esse método está no `OrderBook` do Victor, que invoca `self.transactions.show()`. O `__str__` da classe `Transaction` é o que aparece no terminal:

```text
[2024-01-15 10:32:47] NEGÓCIO FECHADO | Compra #3 x Venda #7 | Qtd: 5 | Preço: R$ 48.00
```

## Análise de complexidade

| Operação                        | Complexidade |
|---------------------------------|--------------|
| `Transaction.__init__`          | O(1)         |
| `TransactionHistory.add`        | O(1)         |
| `TransactionHistory.is_empty`   | O(1)         |
| `TransactionHistory.show`       | O(n)         |
