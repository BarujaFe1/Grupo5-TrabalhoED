# Parte 3 - Transações (Responsável: Nicolas)

Esta seção do sistema é responsável pelo registro dos negócios fechados pelo motor de match. A classe `Transaction` funciona como um recibo imutável de cada operação concluída, armazenando todos os dados relevantes do momento em que uma compra e uma venda foram casadas.

## O que é uma transação

Uma transação é criada sempre que o motor de match (implementado pelo Victor) identifica que o preço de uma ordem de compra é maior ou igual ao preço de uma ordem de venda. Ela não toma nenhuma decisão — apenas registra o resultado do negócio.

## Estrutura da classe

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

## Como se integra com o resto do sistema

Quem usa a classe `Transaction` é o Victor, dentro do método `casar_ordem` do `OrderBook`. Sempre que um match ocorre, ele instancia uma transação assim:

```python
nova_transacao = Transaction(
    id_compra=ordem_atual.id,
    id_venda=melhor_venda.id,
    preco=melhor_venda.preco,
    quantidade=qtd_negociada
)
self.transacoes.append(nova_transacao)
```

O preço registrado é sempre o de quem já estava no livro de ofertas, respeitando a prioridade de chegada. Essa decisão é do motor de match — a `Transaction` apenas armazena o valor recebido.

O menu do Felipe chama:

```python
livro.show_transactions()
```

Esse método está no `OrderBook` do Victor, que percorre a lista de transações e imprime cada uma. O `__str__` da minha classe é o que aparece no terminal:

```text
[2024-01-15 10:32:47] NEGÓCIO FECHADO | Compra #3 x Venda #7 | Qtd: 5 | Preço: R$ 48.00
```

