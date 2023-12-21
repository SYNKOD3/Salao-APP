import pandas as pd
import os
import menu_principal # Módulo do menu principal

class CadastroClientes:
    def __init__(self, arquivo_excel):
        # Inicialização da classe, recebe o nome do arquivo Excel para armazenar dados
        self.arquivo_excel = arquivo_excel
        self.carregar_dados()

    def carregar_dados(self):
        try:
            # Tenta carregar dados do arquivo Excel, se não existir, cria um DataFrame vazio
            self.clientes = pd.read_excel(self.arquivo_excel)
        except FileNotFoundError:
            # Se o arquivo não existir, cria um DataFrame vazio com as colunas desejadas
            self.clientes = pd.DataFrame(columns=['Nome', 'Telefone', 'Preferências', 'Histórico de Serviços'])

    def salvar_dados(self):
        # Salva os dados no arquivo Excel.
        self.clientes.to_excel(self.arquivo_excel, index=False)

    def adicionar_cliente(self, nome, telefone, preferencias):
        # Adiciona um novo cliente ao DataFrame e salva os dados
        novo_cliente = pd.DataFrame([[nome, telefone, preferencias]],
                                    columns=['Nome', 'Telefone', 'Preferências'])
        self.clientes = pd.concat([self.clientes, novo_cliente], ignore_index=True)
        self.salvar_dados()
        print(f"Cliente {nome} cadastrado com sucesso!\n")

    def visualizar_clientes(self):
        # Exibe a lista de clientes no console
        if self.clientes.empty:
            print(">>> NENHUM CLIENTE CADASTRADO <<<.")
        else:
            print("==================== LISTA DE CLIENTES ===================\n")
            print(self.clientes)
            print("\n==========================================================\n")

    def atualizar_cliente(self, nome, novo_telefone, novas_preferencias):
        # Atualiza as informações de um cliente e salva os dados
        filtro = self.clientes['Nome'] == nome
        if filtro.any():
            self.clientes.loc[filtro, 'Telefone'] = novo_telefone
            self.clientes.loc[filtro, 'Preferências'] = novas_preferencias
            self.salvar_dados()
            print(f"\nInformações do cliente {nome} atualizadas com sucesso!\n")
            os.system("PAUSE")
        else:
            print(f"Cliente {nome} não encontrado.")

    def atualizar_historico_servicos(self, nome, tipo_servico):
        # Atualiza o histórico de serviços de um cliente e salva os dados
        filtro = self.clientes['Nome'] == nome
        if filtro.any():
            historico_atual = self.clientes.loc[filtro, 'Histórico de Serviços'].values[0]
            if pd.isna(historico_atual):
                historico_atual = []
            historico_atual.append(tipo_servico)
            self.clientes.loc[filtro, 'Histórico de Serviços'] = historico_atual
            self.salvar_dados()
        else:
            print(f"Cliente {nome} não encontrado.")

def cadClientes():
    # Função principal para interação com o usuário e execução do sistema
    arquivo_excel = 'clientes.xlsx'
    cadastro = CadastroClientes(arquivo_excel)

    while True:
        os.system('cls')  # Limpa a tela do console (específico para Windows)
        print("========== CADASTRO DE CLIENTES =========")
        print("|\t\t\t\t\t|")
        print("|\t1. Adicionar Cliente\t\t|")
        print("|\t2. Visualizar Clientes\t\t|")
        print("|\t3. Atualizar Cliente\t\t|")
        print("|\t4. Voltar ao menu anterior\t|")
        print("|\t\t\t\t\t|")
        print("======== // ======= // ======= // =======\n")

        escolha = input("Escolha uma opção (1 à 4): ")

        # Acessa a área de cadastro do cliente
        if escolha == "1":
            os.system('cls')
            nome = input("Digite o nome do cliente: ")
            telefone = input("Digite o telefone do cliente: ")
            preferencias = input("Digite as preferências do cliente: ")
            print("\n")
            cadastro.adicionar_cliente(nome, telefone, preferencias)
            os.system("PAUSE")
            os.system('cls')

        # Visualiza todos os clientes cadastrados
        elif escolha == "2":
            os.system('cls')
            cadastro.visualizar_clientes()            
            os.system("PAUSE")
            os.system('cls')

        # Atualiza os dados de um cliente já existente
        elif escolha == "3":
            os.system('cls')
            nome = input("Digite o nome do cliente a ser atualizado: ")
            novo_telefone = input("Digite o novo telefone: ")
            novas_preferencias = input("Digite as novas preferências: ")
            cadastro.atualizar_cliente(nome, novo_telefone, novas_preferencias)
            os.system('cls')
            
        # Volta ao menu principal
        elif escolha == "4":
            os.system('cls')
            menu_principal.main()
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    cadClientes()
