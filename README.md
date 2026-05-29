Segue um `README.md` geral pronto para copiar e colocar na raiz do projeto:

````markdown
# Simulador de Livro de Ofertas

Projeto prático da disciplina **Estrutura de Dados em Python**.

O objetivo do trabalho é desenvolver um simulador de livro de ofertas, utilizando estruturas de dados lineares implementadas manualmente, como fila, pilha e lista duplamente encadeada.

O sistema simula o funcionamento básico de um livro de ofertas, recebendo ordens de compra e venda, organizando essas ordens por preço, realizando o casamento entre comprador e vendedor e registrando as transações realizadas.

## Integrantes

- Eduardo
- Felipe
- Fernando
- Nicolas
- Victor

## Regra principal do projeto

As estruturas de dados devem ser construídas manualmente.

Não devemos usar estruturas prontas do Python para implementar fila, pilha ou lista encadeada, como:

```python
list
collections.deque
````

A ideia é demonstrar o funcionamento das estruturas por meio de nós, referências e ponteiros lógicos.

## Organização inicial do projeto

Antes de juntarmos tudo em um único arquivo final, cada integrante vai criar uma pasta com seu nome e colocar dentro dela o arquivo `.py` correspondente à sua parte.

A estrutura inicial será assim:

```text
simulador-livro-ofertas/
│
├── README.md
│
├── felipe/
│   └── felipe_menu.py
│
├── eduardo/
│   └── eduardo_classes_lista.py
│
├── fernando/
│   └── fernando_fila_pilha.py
│
├── nicolas/
│   └── nicolas_transacoes.py
│
├── victor/
│   └── victor_livro_match.py
│
└── final/
    └── simulador_livro_ofertas.py
```

Depois que cada parte estiver pronta, vamos unir tudo no arquivo final:

```text
final/simulador_livro_ofertas.py
```

Esse será o arquivo principal entregue como código do projeto.

## Divisão das partes

### Eduardo

Responsável por:

```text
Classes base e lista duplamente encadeada
```

Arquivo inicial:

```text
eduardo/eduardo_classes_lista.py
```

Eduardo deve implementar:

* Classe `Order`
* Classe `Node`
* Classe `DoublyLinkedList`
* Inserção ordenada
* Remoção de nós
* Busca por ID
* Exibição da lista
* Lista de compras em ordem decrescente de preço
* Lista de vendas em ordem crescente de preço

Commit sugerido:

```bash
git commit -m "feat: implementa classes base e lista duplamente encadeada"
```

Na apresentação, Eduardo explica:

* O que é uma ordem
* O que é um nó
* Como funciona a lista duplamente encadeada
* Como a ordenação das ofertas é feita
* Por que a inserção ordenada tem custo O(n)

---

### Fernando

Responsável por:

```text
Fila encadeada e pilha de undo
```

Arquivo inicial:

```text
fernando/fernando_fila_pilha.py
```

Fernando deve implementar:

* Classe `Queue`
* Método `enqueue`
* Método `dequeue`
* Método `peek`
* Método `is_empty`
* Classe `Stack`
* Método `push`
* Método `pop`
* Método `peek`
* Método `is_empty`
* Funcionamento FIFO da fila
* Funcionamento LIFO da pilha

Commit sugerido:

```bash
git commit -m "feat: implementa fila encadeada e pilha de undo"
```

Na apresentação, Fernando explica:

* Por que usamos fila na entrada das ordens
* Como funciona o FIFO
* Por que usamos pilha no undo
* Como funciona o LIFO
* Por que as operações de extremidade são O(1)

---

### Nicolas

Responsável por:

```text
Transações
```

Arquivo inicial:

```text
nicolas/nicolas_transacoes.py
```

Nicolas deve implementar:

* Classe `Transaction`
* Registro do ID da ordem de compra
* Registro do ID da ordem de venda
* Preço de execução
* Quantidade negociada
* Timestamp da transação
* Método `__str__` para exibir a transação
* Comentários explicando o papel da transação no sistema

Commit sugerido:

```bash
git commit -m "docs: adiciona transacoes"
```

Na apresentação, Nicolas explica:

* O que é uma transação
* Quando uma transação é criada
* Quais dados ficam registrados
* Por que o histórico de transações é importante

---

### Victor

Responsável por:

```text
Livro de ofertas e motor de match
```

Arquivo inicial:

```text
victor/victor_livro_match.py
```

Victor deve implementar:

* Classe `OrderBook`
* Integração com fila de entrada
* Integração com lista de compras
* Integração com lista de vendas
* Integração com pilha de undo
* Integração com transações
* Método `add_order`
* Método `process_next_order`
* Método `process_all_orders`
* Método `match_order`
* Método `undo_last_order`
* Método `show_buy_orders`
* Método `show_sell_orders`
* Método `show_transactions`
* Match total
* Match parcial
* Atualização de quantidade restante
* Remoção de ordens zeradas
* Registro de transações

Commit sugerido:

```bash
git commit -m "feat: implementa livro de ofertas e motor de match"
```

Na apresentação, Victor explica:

* Como o livro de ofertas funciona
* Como ocorre o casamento entre compra e venda
* Quando uma ordem entra no livro
* Quando uma ordem vira transação
* Como funciona o casamento parcial
* Como o undo se integra ao livro

---

### Felipe

Responsável por:

```text
Menu principal e execução do simulador
```

Arquivo inicial:

```text
felipe/felipe_menu.py
```

A parte do Felipe já está pronta.

Ela contém:

* Menu principal no terminal
* Função `main`
* Função `menu`
* Leitura de ordem de compra
* Leitura de ordem de venda
* Validação de ID
* Validação de preço
* Validação de quantidade
* Geração de timestamp
* Entrada com vírgula ou ponto para preço
* Chamada dos métodos principais do `OrderBook`
* Tratamento de opção inválida
* Execução com:

```python
if __name__ == "__main__":
    main()
```

Commit sugerido:

```bash
git commit -m "feat: adiciona menu principal e execucao do simulador"
```

Na apresentação, Felipe explica:

* Como o sistema é executado
* Como o usuário interage pelo terminal
* Como inserir compra e venda
* Como o menu chama o `OrderBook`
* Como as outras partes serão conectadas ao menu

## Como a parte do Felipe está funcionando

A parte do Felipe funciona como a interface principal do projeto.

O menu cria um objeto:

```python
livro = OrderBook()
```

Depois, cada opção chama um método do `OrderBook`.

Por isso, a parte do Victor deve manter estes métodos exatamente com estes nomes:

```python
add_order(order)
process_next_order()
process_all_orders()
show_buy_orders()
show_sell_orders()
show_transactions()
undo_last_order()
```

Se esses nomes forem alterados, o menu não conseguirá chamar corretamente o livro de ofertas.

## Fluxo geral do sistema

O funcionamento esperado será:

```text
1. Usuário abre o sistema pelo terminal.
2. Menu principal aparece.
3. Usuário escolhe inserir compra ou venda.
4. O menu cria uma Order.
5. O menu envia a Order para o OrderBook.
6. O OrderBook coloca a ordem na fila.
7. O sistema processa a fila.
8. O motor verifica se existe match.
9. Se houver match, uma Transaction é criada.
10. Se sobrar quantidade, a ordem restante entra no livro.
11. Se a ordem entrar no livro, seu ID vai para a pilha de undo.
12. O usuário pode consultar compras, vendas, transações ou desfazer a última ordem.
```

## Métodos que precisam ser preservados

Para a integração final funcionar, não devemos mudar estes nomes:

```python
Order
Node
DoublyLinkedList
Queue
Stack
Transaction
OrderBook
add_order
process_next_order
process_all_orders
show_buy_orders
show_sell_orders
show_transactions
undo_last_order
menu
main
```

Também devemos manter os tipos de ordem:

```text
C = Compra
V = Venda
```

## Arquivo final

Depois que todos entregarem suas partes, vamos unir tudo em:

```text
final/simulador_livro_ofertas.py
```

A ordem dentro do arquivo final será:

```text
1. Classes base e lista duplamente encadeada - Eduardo
2. Fila encadeada e pilha de undo - Fernando
3. Transações - Nicolas
4. Livro de ofertas e motor de match - Victor
5. Menu principal e execução do simulador - Felipe
```

## Como testar a parte do Felipe

Entrar na pasta do Felipe:

```bash
cd felipe
```

Executar:

```bash
python felipe_menu.py
```

O menu deve aparecer no terminal.

Algumas opções ainda podem mostrar avisos temporários, porque dependem das partes de Victor, Eduardo, Fernando e Nicolas.

Isso é normal nesta etapa.

## Como vamos juntar as partes

Cada integrante deve entregar seu `.py` dentro da própria pasta.

Depois, vamos copiar as classes e funções de cada arquivo para o arquivo final:

```text
final/simulador_livro_ofertas.py
```

A parte do Felipe ficará no final do arquivo, porque ela executa o sistema.

A parte do Victor ficará antes do menu, porque o menu depende da classe `OrderBook`.

A parte do Eduardo, Fernando e Nicolas ficará antes do `OrderBook`, porque o `OrderBook` depende dessas classes.

## Checklist individual

Antes de enviar sua parte, cada pessoa deve conferir:

* O arquivo `.py` está dentro da pasta com seu nome.
* A parte está comentada.
* O nome das classes e métodos foi mantido.
* Não usou `list` para implementar estrutura principal.
* Não usou `collections.deque`.
* O código não quebra a integração com o menu.
* O commit foi feito com a mensagem combinada.
* A pessoa sabe explicar sua parte na apresentação.

## Commits oficiais

```bash
feat: implementa classes base e lista duplamente encadeada
feat: implementa fila encadeada e pilha de undo
docs: adiciona transacoes
feat: implementa livro de ofertas e motor de match
feat: adiciona menu principal e execucao do simulador
```

## Objetivo da integração final

A integração final deve gerar um único simulador funcional no terminal, capaz de:

* Inserir ordens de compra
* Inserir ordens de venda
* Processar fila de entrada
* Organizar livro de compras
* Organizar livro de vendas
* Realizar match de ordens
* Registrar transações
* Executar undo da última ordem inserida
* Exibir os dados pelo terminal

## Observação final

A parte do Felipe já está pronta e serve como base de integração.

Os demais integrantes devem adaptar suas partes aos nomes e métodos esperados pelo menu, para que a união final seja simples e sem retrabalho.

```
```
