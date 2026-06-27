# Parte 2 - Fila e Pilha (Responsável: Fernando Lacerda Dantas - RA: 17097341)

Esta seção do sistema fornece os mecanismos de enfileiramento de entrada (FIFO) e o sistema de undo (LIFO) do motor de negociação por meio das classes `Queue` (Fila) e `Stack` (Pilha), implementadas manualmente sem o auxílio de estruturas prontas do Python.

## Estrutura das Classes

### 1. No (Nó)
Classe simples de encadeamento dinâmico que guarda o dado da ordem e a referência para o próximo elemento da cadeia.
```python
class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None
```

### 2. Queue (Fila)
Estrutura FIFO (First-In, First-Out). Todas as ordens recém-cadastradas no terminal entram nesta fila para aguardar o processamento pelo motor de negociação.
*   `enqueue(dado)`: Insere um novo elemento no final da fila.
*   `dequeue()`: Remove e retorna o elemento mais antigo do início da fila.
*   `peek()`: Retorna o dado do início da fila sem removê-lo.
*   `is_empty()`: Retorna `True` se a fila estiver vazia.
*   **Aliases em português**: `inserir()`, `remover()`, `vazio()`.

### 3. Stack (Pilha)
Estrutura LIFO (Last-In, First-Out). Armazena exclusivamente o ID das ordens que foram inseridas com sucesso nos livros de ofertas, permitindo o cancelamento rápido.
*   `push(dado)`: Empilha um novo elemento no topo da pilha.
*   `pop()`: Desempilha e retorna o elemento do topo da pilha.
*   `peek()`: Consulta o topo sem removê-lo.
*   `is_empty()`: Retorna `True` se a pilha estiver vazia.
*   **Aliases em português**: `empilhar()`, `desempilhar()`, `vazio()`.

## Como se integra com o resto do sistema
O modulo é instanciado no construtor do `OrderBook` (desenvolvido pelo Victor):
*   `self.fila_entrada`: Uma instância de `Queue` para armazenar as novas ordens vindas do menu do Felipe.
*   `self.undo_stack`: Uma instância de `Stack` para armazenar os IDs das ordens inseridas com sucesso no livro de ofertas.

Quando o menu do Felipe aciona a opção de inserir ordem, o sistema chama `add_order(ordem)`, que coloca a ordem na fila através de `enqueue(ordem)`.
Ao selecionar para processar a fila, o motor retira as ordens da fila usando `dequeue()` e, caso a ordem não sofra match total imediato e seja guardada nos livros, o ID correspondente é empilhado na `undo_stack` usando `push(id_ordem)`. Ao acionar o desfazer, a pilha realiza um `pop()` para remover a ordem correspondente.

## Análise de Complexidade Assintótica

Como as operações de inserção e remoção em filas e pilhas baseadas em ponteiros ocorrem apenas nas extremidades (início/fim da fila e topo da pilha), todas as operações primárias possuem **complexidade constante $O(1)$**:

| Operação | Método | Complexidade | Justificativa |
| :--- | :--- | :--- | :--- |
| Enfileirar | `Queue.enqueue` | $O(1)$ | Adiciona o nó no ponteiro `fim` e atualiza a referência. |
| Desenfileirar | `Queue.dequeue` | $O(1)$ | Retira o nó apontado por `inicio` e avança para o próximo. |
| Empilhar | `Stack.push` | $O(1)$ | Insere o nó no topo da pilha (`topo`) e atualiza as referências. |
| Desempilhar | `Stack.pop` | $O(1)$ | Remove o nó apontado por `topo` e avança o topo para o próximo nó. |
| Consulta | `peek` / `is_empty` | $O(1)$ | Apenas lê o valor do ponteiro da extremidade. |
