# ==================================================
# SIMULADOR DE LIVRO DE OFERTAS
# Disciplina: Estrutura de Dados em Python
# Integrantes: Eduardo, Felipe, Fernando, Nicolas e Victor
#
# Arquivo único do projeto.
# PARTE 5 pronta: Menu principal e execução do simulador.
# Responsável: Felipe
#
# As demais partes estão como placeholders temporários.
# Cada colega deverá substituir a própria seção pela implementação final.
# ==================================================

from datetime import datetime


# ==================================================
# PARTE 1 - CLASSES BASE E LISTA DUPLAMENTE ENCADEADA
# Responsável: Eduardo
# Commit: feat: implementa classes base e lista duplamente encadeada
# ==================================================

class Order:
    """
    Representa uma ordem de compra ou venda.

    Atributos:
    id, tipo, preco, quantidade e timestamp.
    """
    def __init__(self, id, tipo, preco, quantidade, timestamp):
        self.id = id
        self.tipo = tipo
        self.preco = preco
        self.quantidade = quantidade
        self.timestamp = timestamp

    def __str__(self):
        tipo_texto = "Compra" if self.tipo == "C" else "Venda"
        return (
            f"ID: {self.id} | Tipo: {tipo_texto} | "
            f"Preço: R$ {self.preco:.2f} | Quantidade: {self.quantidade} | "
            f"Timestamp: {self.timestamp}"
        )


class Node:
    """
    Placeholder temporário.
    Eduardo substituirá esta classe pela implementação completa do nó.
    """
    pass


class DoublyLinkedList:
    """
    Placeholder temporário.
    Eduardo substituirá esta classe pela lista duplamente encadeada completa.
    """
    pass


# ==================================================
# PARTE 2 - FILA ENCADEADA E PILHA DE UNDO
# Responsável: Fernando
# Commit: feat: implementa fila encadeada e pilha de undo
# ==================================================

class Queue:
    """
    Placeholder temporário.
    Fernando substituirá esta classe pela fila encadeada completa.
    """
    pass


class Stack:
    """
    Placeholder temporário.
    Fernando substituirá esta classe pela pilha encadeada completa.
    """
    pass


# ==================================================
# PARTE 3 - TRANSAÇÕES
# Responsável: Nicolas
# Commit: docs: adiciona transacoes
# ==================================================

class Transaction:
    """
    Placeholder temporário.
    Nicolas substituirá esta classe pela implementação completa das transações.
    """
    pass


# ==================================================
# PARTE 4 - LIVRO DE OFERTAS E MOTOR DE MATCH
# Responsável: Victor
# Commit: feat: implementa livro de ofertas e motor de match
# ==================================================

class OrderBook:
    """
    Interface mínima temporária para o menu funcionar durante os testes.

    Victor deverá substituir esta classe pelo livro de ofertas completo,
    integrando fila, pilha, listas encadeadas, transações e motor de match.
    """
    def __init__(self):
        self.total_ordens_recebidas = 0

    def add_order(self, order):
        self.total_ordens_recebidas += 1
        print("\nOrdem recebida e enviada para a fila de entrada.")
        print(order)

    def process_next_order(self):
        print("\n[AVISO] process_next_order será implementado por Victor.")

    def process_all_orders(self):
        print("\n[AVISO] process_all_orders será implementado por Victor.")

    def show_buy_orders(self):
        print("\n[AVISO] show_buy_orders será implementado por Victor.")

    def show_sell_orders(self):
        print("\n[AVISO] show_sell_orders será implementado por Victor.")

    def show_transactions(self):
        print("\n[AVISO] show_transactions será implementado por Victor.")

    def undo_last_order(self):
        print("\n[AVISO] undo_last_order será implementado por Victor.")


# ==================================================
# PARTE 5 - MENU PRINCIPAL E EXECUÇÃO DO SIMULADOR
# Responsável: Felipe
# Commit: feat: adiciona menu principal e execucao do simulador
# ==================================================

def gerar_timestamp():
    """
    Gera o timestamp da ordem no momento do cadastro.

    Complexidade: O(1).
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ler_inteiro(mensagem, valor_minimo=None):
    """
    Lê um número inteiro com validação.

    Usado para ID e quantidade da ordem.
    """
    while True:
        try:
            valor = int(input(mensagem))

            if valor_minimo is not None and valor < valor_minimo:
                print(f"Valor inválido. Informe um número maior ou igual a {valor_minimo}.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_float(mensagem, valor_minimo=None):
    """
    Lê um número decimal com validação.

    Aceita vírgula ou ponto como separador decimal.
    """
    while True:
        try:
            entrada = input(mensagem).strip().replace(",", ".")
            valor = float(entrada)

            if valor_minimo is not None and valor < valor_minimo:
                print(f"Valor inválido. Informe um número maior ou igual a {valor_minimo}.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida. Digite um número válido. Exemplo: 25.50")


def ler_tipo_ordem():
    """
    Lê e valida o tipo da ordem.

    C = Compra
    V = Venda
    """
    while True:
        tipo = input("Tipo da ordem [C = Compra | V = Venda]: ").strip().upper()

        if tipo in ("C", "V"):
            return tipo

        print("Tipo inválido. Digite apenas C para compra ou V para venda.")


def ler_ordem(tipo=None):
    """
    Lê os dados de uma nova ordem pelo terminal.

    Se o tipo já vier informado pelo menu, não pergunta novamente.
    """
    print("\n--- Cadastro de nova ordem ---")

    id_ordem = ler_inteiro("ID da ordem: ", valor_minimo=1)

    if tipo is None:
        tipo = ler_tipo_ordem()

    preco = ler_float("Preço unitário: R$ ", valor_minimo=0.01)
    quantidade = ler_inteiro("Quantidade: ", valor_minimo=1)
    timestamp = gerar_timestamp()

    return Order(
        id=id_ordem,
        tipo=tipo,
        preco=preco,
        quantidade=quantidade,
        timestamp=timestamp
    )


def exibir_cabecalho():
    """
    Exibe o cabeçalho do sistema.
    """
    print("\n" + "=" * 54)
    print("SIMULADOR DE LIVRO DE OFERTAS")
    print("Estrutura de Dados em Python")
    print("=" * 54)


def exibir_menu():
    """
    Exibe as opções principais do simulador.

    O menu é a interface de teste pelo terminal.
    Cada opção chama um método específico do livro de ofertas.
    """
    print("\nEscolha uma opção:")
    print("1 - Inserir ordem de compra")
    print("2 - Inserir ordem de venda")
    print("3 - Processar próxima ordem da fila")
    print("4 - Processar todas as ordens da fila")
    print("5 - Mostrar livro de compras")
    print("6 - Mostrar livro de vendas")
    print("7 - Mostrar transações realizadas")
    print("8 - Desfazer última ordem inserida no livro")
    print("0 - Sair")


def menu():
    """
    Controla o fluxo principal do sistema.

    Responsabilidades:
    - Receber comandos do usuário.
    - Ler os dados de novas ordens.
    - Chamar os métodos correspondentes do OrderBook.
    - Manter o programa em execução até a opção sair.
    """
    livro = OrderBook()

    while True:
        exibir_cabecalho()
        exibir_menu()

        opcao = input("\nOpção: ").strip()

        if opcao == "1":
            ordem = ler_ordem(tipo="C")
            livro.add_order(ordem)

        elif opcao == "2":
            ordem = ler_ordem(tipo="V")
            livro.add_order(ordem)

        elif opcao == "3":
            livro.process_next_order()

        elif opcao == "4":
            livro.process_all_orders()

        elif opcao == "5":
            livro.show_buy_orders()

        elif opcao == "6":
            livro.show_sell_orders()

        elif opcao == "7":
            livro.show_transactions()

        elif opcao == "8":
            livro.undo_last_order()

        elif opcao == "0":
            print("\nSistema encerrado.")
            break

        else:
            print("\nOpção inválida. Escolha uma opção do menu.")

        input("\nPressione ENTER para continuar...")


def main():
    """
    Função principal do simulador.
    """
    menu()


if __name__ == "__main__":
    main()
