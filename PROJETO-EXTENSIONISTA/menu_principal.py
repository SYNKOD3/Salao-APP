import os
import clientes # Módulo para o cadastro de clientes
import agendamento # Módulo para o agendamento de serviços
import servicosLog # Módulo para o registros de serviços prestados
import estoque # Módulo para o gerenciamento de estoque

#Função principal do menu principal para interação com o usuário
def main():
    while True:
        os.system('cls')
        print("============ SALÃO DE BELEZA - NOBRE ============")
        print("|\t\t\t\t\t\t|")
        print("|\t1. Cadastro de Clientes\t\t\t|")
        print("|\t2. Agendamento de Serviços\t\t|")
        print("|\t3. Registro de Serviços Prestados\t|")
        print("|\t4. Gerenciamento de Estoque\t\t|")
        print("|\t5. Sair do aplicativo\t\t\t|")
        print("|\t\t\t\t\t\t|")
        print("========= // ========= // ========= // ==========\n")

        escolha = input("Escolha uma opção (1 à 5): ")

        #Acessa a classe de cadastro de clientes
        if escolha == "1":            
            clientes.cadClientes()

        #Acessa a classe de Agendamentos
        elif escolha == "2":            
            agendamento.main()

        #Acessa a classe de registro de serviços
        elif escolha == "3":
            servicosLog.servicos()

        #Acessa a classe de gerenciamento de estoque
        elif escolha == "4":
            estoque.gerenciar_estoque()

        #Finaliza a execução do loop e do código
        elif escolha == "5":
            os.system('cls')
            print("\nSaindo do aplicativo. Até logo!\n")
            os.system("PAUSE")
            exit()
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
