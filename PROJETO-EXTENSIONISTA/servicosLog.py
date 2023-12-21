import pandas as pd
import os
from datetime import datetime
import clientes  # Módulo para o cadastro de clientes
import menu_principal  # Módulo do menu principal

class RegistroServicos:
    def __init__(self, arquivo_excel_clientes, arquivo_excel_servicos):
        # Inicialização da classe, recebe os arquivos Excel para clientes e serviços
        self.arquivo_excel_clientes = arquivo_excel_clientes
        self.arquivo_excel_servicos = arquivo_excel_servicos
        self.clientes = clientes.CadastroClientes(self.arquivo_excel_clientes)
        self.carregar_dados()

    def carregar_dados(self):
        try:
            # Tenta carregar dados dos serviços do arquivo Excel
            self.servicos = pd.read_excel(self.arquivo_excel_servicos)
        except FileNotFoundError:
            # Se o arquivo não existir, cria um DataFrame vazio com as colunas desejadas
            self.servicos = pd.DataFrame(columns=['Nome', 'Dia', 'Hora', 'Tipo de Serviço', 'Produtos Usados', 'Custo do Serviço'])

    def salvar_dados(self):
        # Salva os dados dos serviços no arquivo Excel
        self.servicos.to_excel(self.arquivo_excel_servicos, index=False)

    def registrar_servico(self, nome, tipo_servico, produtos_usados, custo_servico):
        # Registra um novo serviço
        data_hora_atual = datetime.now()
        novo_servico = pd.DataFrame([[nome, data_hora_atual.strftime('%Y-%m-%d'), data_hora_atual.strftime('%H:%M:%S'),
                                      tipo_servico, produtos_usados, custo_servico]],
                                    columns=['Nome', 'Dia', 'Hora', 'Tipo de Serviço', 'Produtos Usados', 'Custo do Serviço'])
        self.servicos = pd.concat([self.servicos, novo_servico], ignore_index=True)
        self.salvar_dados()
        # Atualiza o histórico de serviços no módulo de clientes
        self.clientes.atualizar_historico_servicos(nome, tipo_servico)           
        print(f"\nServiço registrado com sucesso para o cliente {nome}!\n")

    def visualizar_historico_servicos(self):
        # Exibe o histórico de serviços
        if self.servicos.empty:
            print(">>> NENHUM SERVIÇO REGISTRADO <<<.")
        else:
            print("============================= HISTÓRICO DE SERVIÇOS ==============================\n")
            print(self.servicos)
            print("\n==================================================================================\n")

# Função principal para interação com o usuário e execução do sistema
def servicos():
    arquivo_excel_clientes = 'clientes.xlsx'
    arquivo_excel_servicos = 'historico_servicos.xlsx'
    registro_servicos = RegistroServicos(arquivo_excel_clientes, arquivo_excel_servicos)

    while True:
        os.system('cls')
        print("======== REGISTRO DE SERVIÇOS PRESTADOS =========")
        print("|\t\t\t\t\t\t|")
        print("|\t1. Registrar Serviço\t\t\t|")
        print("|\t2. Visualizar Histórico de Serviços\t|")
        print("|\t3. Voltar ao Menu Anterior\t\t|")
        print("|\t\t\t\t\t\t|")
        print("========= // ========= // ========= // ==========\n")

        escolha = input("Escolha uma opção (1 à 3): ")

        # Inicia o processo de registro do serviço
        if escolha == "1":
            os.system('cls')
            nome = input("Digite o nome do cliente: ")
            tipo_servico = input("Digite o tipo de serviço prestado: ")
            produtos_usados = input("Digite os produtos usados no serviço: ")
            custo_servico = float(input("Digite o custo do serviço: "))

            registro_servicos.registrar_servico(nome, tipo_servico, produtos_usados, custo_servico)

            os.system("PAUSE")
            os.system('cls')

        # Visualiza o histórico de serviços registrados, se houver
        elif escolha == "2":
            os.system('cls')
            registro_servicos.visualizar_historico_servicos()            
            os.system("PAUSE")
            os.system('cls')

        # Volta ao menu principal
        elif escolha == "3":
            os.system('cls')
            menu_principal.main()
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    servicos()
