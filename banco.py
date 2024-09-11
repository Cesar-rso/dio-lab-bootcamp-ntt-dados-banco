from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente():
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []
        
    def adicionar_conta(self, conta):
        self._contas.append(conta)
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    @property
    def contas(self):
        return self._contas


class PessoaFisica(Cliente):
    def __init__(self, **kwargs):
        self._cpf = kwargs["cpf"]
        self._nome = kwargs["nome"]
        self._data_nascimento = kwargs["data_nascimento"]
        super().__init__(kwargs["endereco"])
        
    def __str__(self):
        return self._nome
        
        
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
        
    @abstractclassmethod
    def registrar(self, conta):
        pass
        

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
        
    def registrar(self, conta):
        resultado_transacao = conta.depositar(self._valor)
        
        if resultado_transacao:
            conta.historico.adicionar_transacao(self)
            
            
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
        
    def registrar(self, conta):
        resultado_transacao = conta.sacar(self._valor)
        
        if resultado_transacao:
            conta.historico.adicionar_transacao(self)
            
    
class Historico():
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
        
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
        

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    def __str__(self):
        return str(self._numero)
        
    @property
    def saldo(self):
        return self._saldo
        
    @property
    def numero(self):
        return self._numero
        
    @property
    def agencia(self):
        return self._agencia
        
    @property
    def cliente(self):
        return self._cliente
        
    @property
    def historico(self):
        return self._historico
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
        
    def sacar(self, valor):
        if valor > self._saldo:
            print("\n Transacao nao realizada! \n Valor informado maior que o saldo disponivel!")
            return False
            
        self._saldo -= valor
        return True
        
    def depositar(self, valor):
        if valor < 0:
            print("\n Transacao nao realizada! \n Valor informado invalido!")
            return False
            
        self._saldo += valor
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        
    @property
    def limite(self):
        return self._limite
        
    @property
    def limite_saques(self):
        return self._limite_saques
        
    def sacar(self, valor):
        saques_hoje = sum([1 for transacao in self.historico.transacoes if datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date() == datetime.now().date()])
        if valor > self._limite:
            print("\n Transacao nao realizada! \n Valor requisitado maior que limite da conta!")
            return False
            
        if saques_hoje >= self._limite_saques:
            print("\n Transacao nao realizada! \n Atingido limite de saques diario da conta!")
            return False
            
        super().sacar(valor)
        
        
def main():
    usuarios = {}
    usuario = None
    conta = None
    menu = f"""
    Usuario = {usuario}
    Agencia = 0001 / Conta = {conta} 
    ==========MENU==========
    [d]  Deposito
    [s]  Saque
    [e]  Extrato
    [tu] Trocar Usuario
    [tc] Trocar Conta
    [nu] Novo Usuario
    [nc] Nova Conta
    [q]  Sair
    
    => """
    
    while True:
        opcao = input(menu)
    
        if opcao == "d":
            if usuario and conta:
                valor = float(input("Informe o valor para deposito: R$ "))
                Deposito(valor).registrar(conta)
                print("Valor depositado!\n")
            else:
                print("Erro! Escolha um usuario/conta para realizar essa operacao!")
    
        elif opcao == "s":
            if usuario and conta:
                valor = float(input("Informe o valor para saque: R$ "))
                Saque(valor).registrar(conta)
                print("Saque realizado!")
            else:
                print("Erro! Escolha um usuario/conta para realizar essa operacao!")
    
        elif opcao == "e":
            print("\n++++++++++EXTRATO++++++++++\n")
            for item in conta.historico.transacoes:
                print("\n===============================")
                for tipo, valor in item.items():
                    print(f"{tipo}: {valor}")
            print("\n===============================\n")
            
        elif opcao == "nu":
            nome = input("Informe o nome completo: ")
            cpf = input("Informe o cpf: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereco: ")
            
            novo_usuario = PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco)
            usuarios[cpf] = novo_usuario
            print("\nNovo usuario cadastrado com sucesso!")
            
            if usuario == None:
                usuario = novo_usuario
        
        elif opcao == "nc":
            if usuario == None:
                print("\nErro! Nao e possivel criar conta sem informar usuario! \n")
                continue
        
            numero_conta = len(usuario.contas) + 1
            nova_conta = ContaCorrente.nova_conta(usuario, numero_conta)
            usuario.adicionar_conta(nova_conta)
            print("\nNova conta adicionada com sucesso!")
            
            if conta == None:
                conta = nova_conta
    
        elif opcao == "tu":
            cpf_usuario = input("Informe o cpf: ")
            if cpf_usuario in usuarios.keys():
                usuario = usuario[cpf_usuario]
                print("\nUsuario trocado com sucesso!")
            else:
                print("\nUsuario nao encontrado no sistema!")
                
        elif opcao == "tc":
            if usuario == None:
                print("\nErro! Nao e possivel trocar conta sem informar usuario! \n")
                continue
                
            numero_conta = int(input("Informe o numero da conta: "))
            for contacorrente in usuario.contas:
                if contacorente.numero == numero_conta:
                    conta = contacorrente
                    print("\nConta trocada com sucesso!")
                    break
                    
        elif opcao == "q":
            break
        else:
            print("\nOperacao Invalida! Informe uma das opcoes apresentadas.\n")
        
        
main()
