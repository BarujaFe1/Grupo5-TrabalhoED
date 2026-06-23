# Contexto para IA — Simulador de Livro de Ofertas

## Propósito

Este documento resume o que foi feito no repositório `Grupo5-TrabalhoED` para que uma IA (ou novo integrante) entenda rapidamente o estado atual do projeto, o que cada arquivo contém e o que ainda precisa ser feito.

---

## Estrutura do Repositório

```
Grupo5-TrabalhoED/
├── AI_CONTEXT.md                          ← Este arquivo
├── README.md                              ← Documentação geral do projeto
├── Relatorio 0.2.pdf                      ← Relatório parcial
├── LICENSE
│
├── Eduardo/
│   └── eduardo_classes_lista.py           ← Order, Node, DoublyLinkedList (Eduardo)
│
├── Felipe/
│   ├── felipe_menu.py                     ← Menu principal + implementações completas (Felipe)
│   └── README_FELIPE.md
│
├── Nicolas/
│   ├── nicolas_transacoes.py              ← Transaction (Nicolas)
│   └── README_NICOLAS.MD
│
├── Victor/
│   ├── victor_livro_match.py              ← OrderBook, match (Victor — nomes em português)
│   └── README_VICTOR.md
│
├── final/
│   ├── simulador_livro_ofertas.py         ← Arquivo final integrado (803 linhas)
│   └── link_github.txt                    ← Link do repositório
│
└── notebook/
    └── performance_tests.ipynb            ← Notebook de análise de performance
```

---

## O que foi feito (commits finais)

| Commit | Descrição |
|---|---|
| `357b841` | Cria `final/simulador_livro_ofertas.py` e `final/link_github.txt` |
| `787d180` | Cria `notebook/performance_tests.ipynb` |
| `1672e95` | Atualiza README com estrutura final |
| `bd84264` | Substitui placeholders no `felipe_menu.py` por implementações reais |

---

## Arquivo Final

`final/simulador_livro_ofertas.py` é o arquivo principal integrado. Contém:

1. **Parte 1 — Eduardo**: `Order`, `Node`, `DoublyLinkedList` com inserção ordenada, remoção, busca, exibição, `vazia()`, `obter_topo()`, `remover_topo()`
2. **Parte 2 — Queue e Stack**: Implementação manual com nós, O(1) nas pontas, aliases pt-BR para compatibilidade
3. **Parte 3 — Nicolas**: `Transaction` + `TransactionHistory` (histórico encadeado, sem `list`)
4. **Parte 4 — Victor (adaptado)**: `OrderBook` com motor de match, nomes em inglês (`add_order`, `process_next_order`, etc.), `undo_last_order`
5. **Parte 5 — Felipe**: Menu, validações, execução

### Compatibilidades resolvidas no arquivo final

| Problema | Solução |
|---|---|
| Victor usa `Pilha` / `Transacao` | Aliases `Pilha = Stack`, `Transacao = Transaction` |
| Victor usa `"compra"/"venda"` | Normalizado com `tipo.strip().upper()` |
| Victor usa `list` para transações | Substituído por `TransactionHistory` |
| DList sem `vazia`, `obter_topo`, `remover_topo` | Adicionados na classe do arquivo final |
| Queue/Stack sem aliases pt-BR | `inserir = enqueue`, `empilhar = push`, etc. |

---

## Pendências por Pessoa (para defesa oral)

### Eduardo — Quase pronto
Faltam 3 métodos na `DoublyLinkedList` do arquivo dele:
- `vazia()` → `return self.head is None`
- `obter_topo()` → `return self.head.data if self.head else None`
- `remover_topo()` → remove head com religação de ponteiros

### Victor — Vários problemas
- Nomes dos métodos em português, mas o menu do Felipe chama em inglês
- Tipo `"compra"/"venda"` em vez de `"C"/"V"` — quebra o match
- Usa `Pilha` (classe inexistente) e `Transacao` (nome errado)
- Usa `list` para transações (viola enunciado)
- Falta `undo_last_order`
- Ver detalhes no `README.md` seção "Métodos que precisam ser preservados"

### Nicolas — Quase pronto
- `Transaction` está correta
- Falta criar `TransactionHistory` (histórico encadeado) no arquivo dele

### Fernando — Precisa criar o arquivo
- `fernando_fila_pilha.py` com `Queue` e `Stack` manuais
- Queue: `enqueue`, `dequeue`, `peek`, `is_empty`, `inserir`, `remover`, `vazio`
- Stack: `push`, `pop`, `peek`, `is_empty`, `empilhar`, `desempilhar`, `vazio`

### Felipe — Completo
- Arquivo `felipe_menu.py` já substituiu placeholders por implementações reais
- Roda standalone com `python felipe_menu.py`

---

## Como Executar

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

### Notebook
```bash
jupyter notebook notebook/performance_tests.ipynb
```

---

## Testes Realizados

Todos os 5 cenários obrigatórios passaram:

1. **Compra sem venda** — ordem aparece no livro ✅
2. **Venda com match total** — transação registrada ✅
3. **Match parcial** — sobra de 15 unidades na compra ✅
4. **Sem match (80 < 100)** — ambas nos livros ✅
5. **Undo** — ordem removida do livro ✅

Testes adicionais: Queue FIFO, Stack LIFO, aliases pt-BR, DoublyLinkedList extra methods, match múltiplo contra várias compras.

---

## Regras para IA ao modificar este repositório

1. NÃO alterar arquivos de integrantes sem permissão explícita
2. NÃO reescrever partes já prontas
3. NÃO usar `list` ou `collections.deque` para estruturas principais
4. Preferir adaptações no arquivo final em vez de mexer nos arquivos individuais
5. Preservar nomes públicos: `Order`, `Node`, `DoublyLinkedList`, `Queue`, `Stack`, `Transaction`, `OrderBook`
6. Preservar métodos: `add_order`, `process_next_order`, `process_all_orders`, `show_buy_orders`, `show_sell_orders`, `show_transactions`, `undo_last_order`
7. Tipos de ordem: `"C"` para Compra, `"V"` para Venda
