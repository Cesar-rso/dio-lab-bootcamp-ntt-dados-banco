

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente numeros): ")
    if cpf in usuarios:
        print("\nCPF informado já é cadastrado no sistema!\n")
        return
    else:
        usuarios[cpf] = {}
        usuarios[cpf]["nome"] = input("Informe o nome completo: ")
        usuarios[cpf]["data_nascimento"] = input("Informe a data de nascimento: ")
        usuarios[cpf]["telefone"] = input("Informe o telefone (somente numeros, incluindo ddd): ")
        usuarios[cpf]["endereco"] = input("Informe o endereco: ")
        usuarios[cpf]["contas"] = []
        
        print("Cliente cadastrado com sucesso!")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuario: ")
    if cpf in usuarios:
        conta = {"agencia": agencia, "numero": numero_conta, "usuario": {cpf: usuarios[cpf]}}
        print("Conta criada com sucesso!")
        return conta
    else:
        print("\nCPF não cadastrado no sistema!\n")

def deposito(valor, extrato, saldo, /):
    if valor < 0:
        print("\nValor informado menor que zero! Não foi possível completar a operacao!\n")
    else:
        saldo += valor
        operacao = f"Deposito: \n   R$ {valor:.2f}"
        extrato.append(operacao)
        print("Operacao realizada com sucesso!\n" + operacao)

def saque(*, valor, saque, numero_saques, limite_saque, extrato):
    
    if valor > saldo:
        print("\nValor requerido maior que saldo atual! Não foi possível completar a operacao!\n")
    elif valor > limite_saque:
        print("\nValor requerido maior que limite de saque atual! Não foi possível completar a operacao!\n")
    else:
        saldo -= valor
        numero_saques += 1
        operacao = f"Saque: \n      R$ {valor:.2f}"
        extrato.append(operacao)
        print("Operacao realizada com sucesso!\n" + operacao)

def exibe_extrato(saldo, /, *, extrato):
    print("\n==========EXTRATO==========\n")
    if len(extrato) == 0:
        print("Não foram realizadas movimentacoes!")
    else:
        for operacao in extrato:
            print(operacao)
        
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("\n===========================\n")


def main():
    menu = """
    ==========MENU==========
    [d]  Deposito
    [s]  Saque
    [e]  Extrato
    [nu] Novo Usuario
    [nc] Nova Conta
    [q]  Sair
    
    => """

    usuarios = {}
    contas = []
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    while True:
        opcao = input(menu)
    
        if opcao == "d":
            valor = float(input("Informe o valor para deposito: R$ "))
            deposito(valor, extrato, saldo)
    
        elif opcao == "s":
            if numero_saques >= LIMITE_SAQUES:
    	        print("Limite de saques diario atingido! Não foi possível completar a operacao!")
            else:
                valor = float(input("Informe o valor para saque: R$ "))
                saque(valor=valor, saque=saque, numero_saques=numero_saques, limite_saque=limite, extrato=extrato)
    
        elif opcao == "e":
            exibe_extrato(saldo, extrato=extrato)
            
        elif opcao == "nu":
            criar_usuario(usuarios)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            
            if conta:
                contas.append(conta)
    
        elif opcao == "q":
            break
        else:
            print("\nOperacao Invalida! Informe uma das opcoes apresentadas.\n")
        
        
main()
