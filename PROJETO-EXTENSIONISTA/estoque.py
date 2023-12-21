import pandas as pd
import os
import menu_principal # Módulo do menu principal

class GerenciadorEstoque:
    def __init__(self):
        # Carrega a tabela do Excel (se existir) ou cria uma nova
        try:
            self.estoque = pd.read_excel('estoque.xlsx')
        except FileNotFoundError:
            self.estoque = pd.DataFrame(columns=['Produto', 'Quantidade'])

    def adicionar_produto(self, produto, quantidade):
        # Adiciona um produto à tabela ou atualiza a quantidade se o produto já existir
        if produto in self.estoque['Produto'].tolist():
            self.estoque.loc[self.estoque['Produto'] == produto, 'Quantidade'] += quantidade
        else:
            novo_produto = pd.DataFrame({'Produto': [produto], 'Quantidade': [quantidade]})
            self.estoque = pd.concat([self.estoque, novo_produto], ignore_index=True)

        # Atualiza a tabela no Excel
        self.estoque.to_excel('estoque.xlsx', index=False)

        # Exibe uma mensagem de sucesso
        print(f"\nProduto '{produto}' adicionado com sucesso!\n")
        os.system("PAUSE")

    def remover_produto(self, produto, quantidade):
        # Remove a quantidade especificada do produto
        if produto in self.estoque['Produto'].tolist():
            self.estoque.loc[self.estoque['Produto'] == produto, 'Quantidade'] -= quantidade
            # Remove a linha se a quantidade se tornar zero ou negativa
            self.estoque = self.estoque[self.estoque['Quantidade'] > 0]
            # Atualiza a tabela no Excel
            self.estoque.to_excel('estoque.xlsx', index=False)
            
            # Exibe mensagem de sucesso
            print(f"\nProduto '{produto}' removido com sucesso!\n")
            os.system("PAUSE")
        else:
            print(f"\nProduto {produto} não encontrado no estoque.\n")

    def exibir_estoque(self):
        # Exibe o estoque atual ou uma mensagem de erro se estiver vazio
        if self.estoque.empty:
            print("\nERRO: Estoque não cadastrado ou vazio.\n")
            os.system("PAUSE")
        else:
            print("============== ESTOQUE ==============\n")
            print(self.estoque)
            print("\n=====================================\n")
            os.system("PAUSE")

# Função principal para interação com o usuário e execução do sistema
def gerenciar_estoque():
    gerEstoque = GerenciadorEstoque()

    while True:
        os.system('cls')
        print("=========== GERENCIAR ESTOQUE ===========")
        print("|\t\t\t\t\t|")
        print("|\t1. Adicionar Produto\t\t|")
        print("|\t2. Remover Produto\t\t|")
        print("|\t3. Visualizar Estoque\t\t|")
        print("|\t4. Voltar ao Menu Anterior\t|")
        print("|\t\t\t\t\t|")
        print("======= // ======= // ======= // ========\n")

        escolha = input("Escolha uma opção (1 à 4): ")

        # Acessa a área de adição de produtos
        if escolha == "1":
            os.system('cls')
            produto = input("Digite o nome do produto: ")
            quantidade = int(input("Digite a quantidade a ser adicionada: "))
            gerEstoque.adicionar_produto(produto, quantidade)

        # Acessa a área de remocção de produtos
        elif escolha == "2":
            os.system('cls')
            produto = input("Digite o nome do produto: ")
            quantidade = int(input("Digite a quantidade a ser removida: "))
            gerEstoque.remover_produto(produto, quantidade)

        # Visualiza o estoque, se houver
        elif escolha == "3":
            os.system('cls')
            gerEstoque.exibir_estoque()

        # Volta ao menu principal
        elif escolha == "4":
            menu_principal.main()
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    gerenciar_estoque()
