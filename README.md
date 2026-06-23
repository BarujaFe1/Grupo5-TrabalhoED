# Simulador de Livro de Ofertas

Projeto prático da disciplina **Estrutura de Dados em Python**.

Simulador de livro de ofertas (Order Book) usando estruturas de dados lineares implementadas manualmente — fila (FIFO), pilha (LIFO) e lista duplamente encadeada ordenada — para receber ordens de compra/venda, realizar casamento (match) e registrar transações.

## Integrantes

- Eduardo
- Felipe
- Fernando
- Nicolas
- Victor

## Regras do projeto

Todas as estruturas foram construídas manualmente com nós, sem uso de `list` ou `collections.deque`.

## Estrutura do repositório

```
Grupo5-TrabalhoED/
├── README.md
├── AI_CONTEXT.md
├── Relatorio 0.2.pdf
├── Eduardo/
│   └── eduardo_classes_lista.py
├── Felipe/
│   ├── felipe_menu.py
│   └── README_FELIPE.md
├── Nicolas/
│   ├── nicolas_transacoes.py
│   └── README_NICOLAS.MD
├── Victor/
│   ├── victor_livro_match.py
│   └── README_VICTOR.md
├── final/
│   ├── simulador_livro_ofertas.py
│   └── link_github.txt
└── notebook/
    └── performance_tests.ipynb
```

## Divisão das partes

### Eduardo — `Eduardo/eduardo_classes_lista.py`

**Classes base e lista duplamente encadeada.**

Implementou:
- `Order` — ordem de compra ou venda (id, tipo, preco, quantidade, timestamp)
- `Node` — nó com data, next e prev
- `DoublyLinkedList` — inserção ordenada (compras decrescente, vendas crescente), remoção por ID, busca, exibição

Na apresentação explica: o que é uma ordem, nó, lista duplamente encadeada, ordenação por preço, complexidade O(n) da inserção ordenada.

---

### Fernando — (implementado no arquivo final)

**Fila encadeada e pilha de undo.**

Implementado em `final/simulador_livro_ofertas.py`:
- `Queue` — enqueue, dequeue, peek, is_empty (FIFO, O(1))
- `Stack` — push, pop, peek, is_empty (LIFO, O(1))

Na apresentação explica: por que fila na entrada (FIFO), pilha no undo (LIFO), operações O(1) nas pontas.

---

### Nicolas — `Nicolas/nicolas_transacoes.py`

**Transações.**

Implementou:
- `Transaction` — id_compra, id_venda, preco, quantidade, timestamp, `__str__`

Na apresentação explica: o que é uma transação, quando é criada, dados registrados, importância do histórico.

---

### Victor — `Victor/victor_livro_match.py`

**Livro de ofertas e motor de match.**

Implementou:
- `OrderBook` com lógica de match entre compra e venda
- Casamento total e parcial
- Atualização de quantidades e remoção de ordens zeradas

Na apresentação explica: funcionamento do livro de ofertas, critério de match (preço_compra >= preço_venda), match total e parcial, integração com undo.

---

### Felipe — `Felipe/felipe_menu.py`

**Menu principal e execução do simulador.**

Implementou:
- Menu interativo no terminal
- Validação de ID, preço, quantidade e tipo
- Geração de timestamp
- Chamadas para o `OrderBook`
- Arquivo completo e funcional (placeholders substituídos)

Na apresentação explica: fluxo do sistema pelo terminal, como cada opção do menu chama o OrderBook.

## Arquivo final integrado

`final/simulador_livro_ofertas.py` reúne todas as partes em um único arquivo funcional:

1. **Eduardo** — Order, Node, DoublyLinkedList (com métodos extras: vazia, obter_topo, remover_topo)
2. **Fernando** — Queue, Stack (com aliases pt-BR: inserir, remover, empilhar, etc.)
3. **Nicolas** — Transaction + TransactionHistory (histórico encadeado)
4. **Victor** — OrderBook adaptado (métodos em inglês, tipo C/V, Stack, Transaction, undo)
5. **Felipe** — Menu, validações, execução

## Como executar

### Simulador final
```bash
cd final
python simulador_livro_ofertas.py
```

### Arquivo do Felipe (standalone)
```bash
cd Felipe
python felipe_menu.py
```

### Notebook de performance
```bash
jupyter notebook notebook/performance_tests.ipynb
```

## Fluxo do sistema

```
1. Usuário abre o terminal → menu principal
2. Escolhe inserir compra ou venda
3. Sistema cria uma Order e coloca na fila de entrada (Queue)
4. Fila é processada → motor de match verifica se há ordens compatíveis
5. Se preço_compra >= preço_venda → Transaction é criada
6. Se sobrar quantidade → ordem vai para o livro (DoublyLinkedList)
7. Se ordem entrar no livro → ID vai para a pilha de undo (Stack)
8. Usuário pode consultar livros, transações ou desfazer última ordem
```

## Testes realizados

| Teste | Resultado |
|---|---|
| Compra sem venda | Compra ID 1 aparece no livro |
| Venda com match total | Transação de 10 un. registrada |
| Match parcial | Transação de 5 un., sobra de 15 na compra |
| Sem match (80 < 100) | Ambas as ordens nos livros |
| Undo | Última ordem removida do livro |
| Queue FIFO | enqueue/dequeue A→B→C ordem correta |
| Stack LIFO | push/pop X→Y→Z ordem inversa |
| Aliases pt-BR | inserir, remover, vazio, empilhar, desempilhar funcionam |
| Match múltiplo | Venda casa com várias compras em ordem de melhor preço |

## Análise de complexidade

| Estrutura | Operação | Complexidade |
|---|---|---|
| Queue | enqueue / dequeue | O(1) |
| Stack | push / pop | O(1) |
| DoublyLinkedList | inserção ordenada | O(n) |
| DoublyLinkedList | remoção por ID | O(n) |
| DoublyLinkedList | busca | O(n) |

A fila e a pilha têm desempenho constante O(1). A lista duplamente encadeada ordenada exige busca linear O(n) para inserir na posição correta, o que torna o processamento mais custoso conforme o volume de ordens cresce — resultado esperado e documentado no notebook de performance.

## Notebook de performance

`notebook/performance_tests.ipynb` contém:
- Geração de ordens simuladas (compra e venda aleatórias)
- Testes com 1.000, 5.000 e 10.000 ordens
- Medição de tempo de inserção, processamento e total
- Tabela comparativa de resultados
- Gráficos: qtde × tempo total, qtde × tempo médio, inserção vs processamento
- Análise textual dos resultados

## Defesa oral

Cada integrante explica sua parte:

| Pessoa | Tema |
|---|---|
| Eduardo | Order, Node, DoublyLinkedList |
| Fernando | Queue, Stack, FIFO, LIFO, undo |
| Nicolas | Transaction, histórico de negociações |
| Victor | OrderBook, motor de match, casamento total/parcial |
| Felipe | Menu principal, execução, fluxo pelo terminal |

Cada um deve explicar: o que construiu, como funciona, como se conecta ao restante, complexidade principal, como testou.

## Links

- Repositório: `final/link_github.txt`
- Relatório: `Relatorio 0.2.pdf`

## Pendências para versão final

- [ ] **Eduardo**: adicionar `vazia()`, `obter_topo()`, `remover_topo()` na DoublyLinkedList
- [ ] **Victor**: renomear métodos para inglês, trocar `"compra"/"venda"` por `"C"/"V"`, usar `Stack`/`Transaction`, adicionar `undo_last_order`, trocar `list` por TransactionHistory
- [ ] **Nicolas**: criar `TransactionHistory` (histórico encadeado)
- [ ] **Fernando**: criar `fernando_fila_pilha.py` com Queue e Stack
- [x] **Felipe**: arquivo completo e funcional
- [x] Arquivo final integrado criado
- [x] Notebook de performance criado
- [x] link_github.txt criado
