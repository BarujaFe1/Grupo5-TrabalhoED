# Como a parte do Felipe funciona

Este README serve para os outros integrantes entenderem como adaptar as partes deles ao menu principal feito pelo Felipe.

A minha parte é a interface de execução do sistema. Ela não implementa a lógica do livro de ofertas. Ela apenas recebe os comandos do usuário pelo terminal e chama os métodos que serão implementados nas outras partes.

Arquivo principal:

```text
simulador_livro_ofertas.py
```

Minha seção no arquivo:

```python
# ==================================================
# PARTE 5 - MENU PRINCIPAL E EXECUÇÃO DO SIMULADOR
# Responsável: Felipe
# Commit: feat: adiciona menu principal e execucao do simulador
# ==================================================
```

## O que minha parte faz

Minha parte cria o menu do terminal com estas opções:

```text
1 - Inserir ordem de compra
2 - Inserir ordem de venda
3 - Processar próxima ordem da fila
4 - Processar todas as ordens da fila
5 - Mostrar livro de compras
6 - Mostrar livro de vendas
7 - Mostrar transações realizadas
8 - Desfazer última ordem inserida no livro
0 - Sair
```

Também criei funções auxiliares para:

```text
gerar timestamp da ordem
ler ID
ler preço
ler quantidade
validar entrada inválida
criar uma ordem de compra
criar uma ordem de venda
chamar os métodos do OrderBook
```

## Como o menu se conecta com as outras partes

O menu cria um objeto principal:

```python
livro = OrderBook()
```

Depois disso, cada opção do menu chama um método do `OrderBook`.

Por isso, a parte do Victor precisa manter exatamente estes métodos na classe `OrderBook`:

```python
add_order(order)
process_next_order()
process_all_orders()
show_buy_orders()
show_sell_orders()
show_transactions()
undo_last_order()
```

Se esses nomes forem alterados, o menu vai parar de funcionar. Então, a adaptação principal é: Victor pode implementar a lógica interna como quiser, mas deve preservar esses nomes de métodos.

## Como a parte de Eduardo deve se adaptar

Eduardo ficará com:

```python
Order
Node
DoublyLinkedList
```

A função `ler_ordem()` do menu já cria uma ordem assim:

```python
return Order(
    id=id_ordem,
    tipo=tipo,
    preco=preco,
    quantidade=quantidade,
    timestamp=timestamp
)
```

Então a classe `Order` precisa aceitar esses parâmetros:

```python
id
tipo
preco
quantidade
timestamp
```

Também é importante manter o método `__str__`, porque o menu imprime a ordem quando ela é cadastrada.

Modelo esperado:

```python
class Order:
    def __init__(self, id, tipo, preco, quantidade, timestamp):
        self.id = id
        self.tipo = tipo
        self.preco = preco
        self.quantidade = quantidade
        self.timestamp = timestamp
```

## Como a parte de Fernando deve se adaptar

Fernando ficará com:

```python
Queue
Stack
```

A fila e a pilha serão usadas dentro do `OrderBook`, principalmente na parte do Victor.

O menu não chama `Queue` e `Stack` diretamente. Ele chama o `OrderBook`.

Então Fernando precisa garantir que Victor consiga usar métodos como:

```python
enqueue(order)
dequeue()
is_empty()
peek()
push(order_id)
pop()
```

Esses métodos devem funcionar sem usar `list` ou `collections.deque`.

## Como a parte de Nicolas deve se adaptar

Nicolas ficará com:

```python
Transaction
```

A classe `Transaction` será usada pelo `OrderBook` quando acontecer um match.

A parte do menu chama:

```python
livro.show_transactions()
```

Então Victor precisa guardar as transações e exibi-las nesse método.

Nicolas deve deixar a transação com dados fáceis de imprimir, por exemplo:

```python
id_compra
id_venda
preco_execucao
quantidade
timestamp
```

Também é recomendado criar um `__str__` para que `show_transactions()` consiga mostrar as transações de forma legível.

## Como a parte de Victor deve se adaptar

Victor ficará com:

```python
OrderBook
```

Essa é a parte que conecta tudo.

O menu já espera que o `OrderBook` tenha estes métodos:

```python
def add_order(self, order):
    pass

def process_next_order(self):
    pass

def process_all_orders(self):
    pass

def show_buy_orders(self):
    pass

def show_sell_orders(self):
    pass

def show_transactions(self):
    pass

def undo_last_order(self):
    pass
```

A lógica interna deve usar as estruturas feitas pelos colegas:

```text
Queue, feita por Fernando
Stack, feita por Fernando
DoublyLinkedList, feita por Eduardo
Transaction, feita por Nicolas
Order, feita por Eduardo
```

O fluxo esperado é:

```text
menu recebe dados
menu cria Order
menu chama livro.add_order(order)
OrderBook coloca a ordem na fila
OrderBook processa a fila
OrderBook tenta fazer match
OrderBook registra transações
OrderBook insere sobras no livro
OrderBook permite undo
```

## O que não pode mudar

Para o menu continuar funcionando, não mudem estes nomes:

```python
Order
OrderBook
add_order
process_next_order
process_all_orders
show_buy_orders
show_sell_orders
show_transactions
undo_last_order
```

Também não mudem estes valores de tipo:

```text
C = Compra
V = Venda
```

## Como testar minha parte

Execute:

```bash
python simulador_livro_ofertas.py
```

Teste básico:

```text
1 - Inserir ordem de compra
ID: 1
Preço: 50
Quantidade: 100
```

Depois teste:

```text
2 - Inserir ordem de venda
ID: 2
Preço: 48
Quantidade: 60
```

Enquanto as outras partes não forem implementadas, algumas opções mostrarão avisos dizendo que serão completadas por Victor. Isso é normal.

## Resumo para o grupo

Minha parte está pronta para receber as outras implementações. O menu já cria ordens, valida os dados e chama os métodos principais do `OrderBook`.

Cada colega deve adaptar sua parte sem quebrar os nomes usados pelo menu.
