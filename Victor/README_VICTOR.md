# Livro de Ofertas e Motor de Match 

O sistema é capaz de receber ordens de compra e venda através de uma fila de processamento, organizar essas ordens em livros de ofertas e realizar o casamento de preços (match) automaticamente quando as condições de mercado são atendidas.

Toda a lógica foi desenvolvida utilizando **estruturas de dados puras e de encadeamento manual**, sem o uso de listas nativas ou métodos prontos do Python para a ordenação e armazenamento interno.

##  Funcionalidades

- **Fila de Entrada (FIFO):** Centraliza o recebimento de ordens e garante que elas sejam processadas na ordem exata de chegada.
- **Livro de Ofertas Ordenado:** - As ordens de **Compra** são organizadas em ordem **decrescente** de preço.
  - As ordens de **Venda** são organizadas em ordem **crescente** de preço.
- **Motor de Match:** Executa o cruzamento de ordens sempre que o preço de uma ordem de compra é maior ou igual ao preço de uma ordem de venda.
- **Histórico de Negociações:** Registra formalmente cada transação realizada, documentando as partes envolvidas, quantidade e preço final, como se fosse uma nota fiscal.

##  Estruturas de Dados Utilizadas

Para atender aos requisitos de manipulação manual de memória e ponteiros, foram implementadas as seguintes estruturas:

1. `Node`: Classe base que carrega a ordem (`Order`) e mantém referências para os nós vizinhos (`next` e `prev`).
2. `Queue` (Fila): Controla o fluxo de entrada das ordens sob a regra *First-In, First-Out*.
3. `ListaDuplamenteEncadeada`: Responsável pelo armazenamento dinâmico das ordens no livro. Realiza buscas sequenciais na memória para realizar a inserção ordenada dos nós.
4. `Pilha`: Armazena os identificadores das ordens de forma encadeada sob a regra *Last-In, First-Out* para controle de operações de desfazer.

##  Agrupamentos Principais

- `Order`: Modela a ordem de negociação contendo ID, tipo (`compra` ou `venda`), preço e quantidade de ativos.
- `Transacao`: Funciona como o recibo/comprovante gerado logo após um casamento de ordens bem-sucedido.
- `OrderBook`: O coração do sistema, responsável por coordenar a fila de entrada, invocar o motor de casamento (`casar_ordem`) e gerenciar os livros.
