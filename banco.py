menu = """
    [d] Deposito
    [s] Saque
    [e] Extrato
    [q] Sair
    
    => """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

def deposito(valor, extrato):
    if valor < 0:
        print("Valor informado menor que zero! Não foi possível completar a operacao!")
    else:
        global saldo
        saldo += valor
        operacao = f"Deposito no valor de R$ {valor:.2f}"
        extrato.append(operacao)
        print("Operacao realizada com sucesso!\n" + operacao)

def saque(valor, limite_saque, extrato):
    global saldo
    global numero_saques
    if valor > saldo:
        print("Valor requerido maior que saldo atual! Não foi possível completar a operacao!")
    elif valor > limite_saque:
        print("Valor requerido maior que limite de saque atual! Não foi possível completar a operacao!")
    else:
        saldo -= valor
        numero_saques += 1
        operacao = f"Saque no valor de R$ {valor:.2f}"
        extrato.append(operacao)
        print("Operacao realizada com sucesso!\n" + operacao)

def exibe_extrato(saldo, extrato):
    if len(extrato) == 0:
        print("Não foram realizadas movimentacoes!")
    else:
        print("\n==========EXTRATO==========\n")
        for operacao in extrato:
            print(operacao)
        
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("\n===========================\n")


while True:
    opcao = input(menu)
    
    if opcao == "d":
        valor = float(input("Informe o valor para deposito: R$ "))
        deposito(valor, extrato)
    
    elif opcao == "s":
        if numero_saques >= LIMITE_SAQUES:
    	    print("Limite de saques diario atingido! Não foi possível completar a operacao!")
        else:
            valor = float(input("Informe o valor para saque: R$ "))
            saque(valor, limite, extrato)
    
    elif opcao == "e":
        exibe_extrato(saldo, extrato)
    
    elif opcao == "q":
        break
    else:
        print("Operacao Invalida! Informe uma das opcoes apresentadas.")
        
