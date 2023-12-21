import pandas as pd
import menu_principal # Módulo do menu principal
import os
from datetime import datetime, timedelta

class AgendamentoServicos:
    def __init__(self, clientes_file='clientes.xlsx', agendamentos_file='agendamentos.xlsx'):
        # Inicialização da classe, carrega dados de clientes e agendamentos
        self.clientes_file = clientes_file
        self.agendamentos_file = agendamentos_file
        self.clientes_df = self._carregar_clientes()
        self.agendamentos_df = self._carregar_agendamentos()

    def _carregar_clientes(self):
        try:
            # Tenta carregar dados dos clientes do arquivo Excel
            return pd.read_excel(self.clientes_file)
        except FileNotFoundError:
            # Se o arquivo não existir, exibe uma mensagem de erro e retorna ao menu principal
            os.system('cls')
            print(">>> ERRO: NENHUM CLIENTE CADASTRADO! <<<\n")
            os.system("PAUSE")            
            menu_principal.main()

    def _carregar_agendamentos(self):
        try:
            # Tenta carregar dados de agendamentos do arquivo Excel
            return pd.read_excel(self.agendamentos_file)
        except FileNotFoundError:
            # Se o arquivo não existir, cria um DataFrame vazio com as colunas necessárias
            return pd.DataFrame(columns=['Nome', 'Data', 'Horario', 'Servico'])

    def agendar_servico(self):
        # Função para agendar um novo serviço
        nome = input("Digite o nome do cliente: ")
        if nome not in self.clientes_df['Nome'].values:
            # Verifica se o cliente já existe no DataFrame de clientes
            print(f"\nCliente {nome} não encontrado.\n")
            os.system("PAUSE")
            os.system('cls')
            return

        data_str = input("Digite a data do agendamento (formato: dd/mm/aaaa): ")
        try:
            data = datetime.strptime(data_str, '%d/%m/%Y').date()
        except ValueError:
            # Verifica se o formato da data é válido
            print("Formato de data inválido. Use dd/mm/aaaa.")
            return

        horarios_disponiveis = self._horarios_disponiveis(data)
        if not horarios_disponiveis:
            # Verifica se há horários disponíveis para o dia escolhido
            print("Todos os horários para este dia estão ocupados.")
            return

        print("\nHorários Disponíveis:")
        for i, horario in enumerate(horarios_disponiveis, start=1):
            print(f"{i}. {horario}")

        escolha_horario = input("Escolha um número de horário: ")

        if escolha_horario not in map(str, range(1, len(horarios_disponiveis) + 1)):
            # Verifica se a escolha do horário é válida
            print("Escolha de horário inválida.")
            return

        horario_escolhido = horarios_disponiveis[int(escolha_horario) - 1]

        servico = input("Digite o serviço a ser agendado: ")

        novo_agendamento = pd.Series({'Nome': nome, 'Data': data, 'Horario': horario_escolhido, 'Servico': servico})
        self.agendamentos_df = self.agendamentos_df.append(novo_agendamento, ignore_index=True)
        self._atualizar_historico(nome, f"{data} - {servico}")
        self._salvar_agendamentos_no_excel()

    def _horarios_disponiveis(self, data):
        # Retorna os horários disponíveis para o dia especificado
        horarios_ocupados = self.agendamentos_df.loc[self.agendamentos_df['Data'] == data, 'Horario'].tolist()

        horarios_disponiveis = []
        horario_atual = datetime.strptime("09:00", "%H:%M")

        while horario_atual < datetime.strptime("17:00", "%H:%M"):
            horario_str = horario_atual.strftime("%H:%M")

            if horario_str not in horarios_ocupados:
                horarios_disponiveis.append(horario_str)

            horario_atual += timedelta(minutes=30)

        return horarios_disponiveis

    def _atualizar_historico(self, nome, novo_servico):
        # Atualiza o histórico de serviços do cliente
        filtro = self.clientes_df['Nome'] == nome
        if filtro.any():
            historico_atual = self.clientes_df.loc[filtro, 'Histórico de Serviços'].values[0]
            if pd.isna(historico_atual):
                historico_atual = []
            historico_atual.append(novo_servico)
            self.clientes_df.loc[filtro, 'Histórico de Serviços'] = historico_atual
            self._salvar_clientes_no_excel()
        else:
            print(f"Cliente {nome} não encontrado.")

    def _salvar_agendamentos_no_excel(self):
        # Salva os dados de agendamentos no arquivo Excel
        self.agendamentos_df.to_excel(self.agendamentos_file, index=False)

    def _salvar_clientes_no_excel(self):
        # Salva os dados de clientes no arquivo Excel
        self.clientes_df.to_excel(self.clientes_file, index=False)

    def visualizar_servicos_agendados(self):
        # Exibe os serviços agendados no console
        if self.agendamentos_df.empty:
            print(">>> NÃO HÁ SERVIÇOS AGENDADOS <<<\n")
        else:
            print("========== SERVIÇOS AGENDADOS ==========\n")
            print(self.agendamentos_df[['Nome', 'Data', 'Horario', 'Servico']])
            print("\n========================================\n")

def main():
    # Função principal para interação com o usuário e execução do sistema
    agendamento = AgendamentoServicos()

    while True:
        os.system('cls')
        print("============ AGENDAMENTO DE SERVIÇOS ============")
        print("|\t\t\t\t\t\t|")
        print("|\t1. Agendar Serviço\t\t\t|")
        print("|\t2. Visualizar serviços agendados\t|")
        print("|\t3. Voltar ao Menu Principal\t\t|")
        print("|\t\t\t\t\t\t|")
        print("========= // ========= // ========= // ==========\n")

        escolha = input("Escolha uma opção (1 à 3): ")

        # Acessa a área de agendamento de serviços
        if escolha == "1":
            os.system('cls')
            agendamento.agendar_servico()

        # Visualiza todos os serviços agendados, caso haja
        elif escolha == "2":
            os.system('cls')
            agendamento.visualizar_servicos_agendados()
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
    main()
