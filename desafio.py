from abc import ABC,abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class pessoa_fisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = f"{numero}"
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
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
        return cls(numero, cliente)
    
    def __str__(self) -> str:
        return f"Tipo: {self.__class__.__name__} Agencia: {self.agencia} Numero: {self.numero}"
    
    def sacar(self, valor):
        if valor > 0:
            excedeu_saldo = valor > self._saldo

            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")
            else:
                self._saldo -= valor
                print("Saque realizado com sucesso")
                return True
        else:
            print("Operação falhou! O valor informado é inválido.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Valor depositado com sucesso")
            return True
        print("Valor invalido para deposito")
        return False

class conta_corrente(Conta):
    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self._limite = 500
        self._limite_saque = 2

    def sacar(self, valor):
        if valor > 0:
            excedeu_saldo = valor > self._saldo
            excedeu_limite = valor > self._limite
            excedeu_saques = self._historico.numero_saques_dia() >= self._limite_saque
            
            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")

            elif excedeu_limite:
                print("Operação falhou! O valor do saque excede o limite.")

            elif excedeu_saques:
                print("Operação falhou! Número máximo de saques excedido.")

            else:
                return super().sacar(valor)
        else:
            print("Operação falhou! O valor informado é inválido.")

        return False

    
class Transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self,conta):
        pass

class deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        
    
class saque(Transacao):
    def __init__(self,valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self) -> None:
        self._transacoes =  []
    
    def adicionar_transacao(self,transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%Y %m %d %H:%M:%S"), 
        })

    def numero_saques_dia(self):
        num_saques = 0
        for transacao in self._transacoes:
            if transacao["tipo"] == saque.__name__:
                num_saques += 1
        
        return num_saques

    @property
    def transacoes(self):
        return self._transacoes

def encontrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
        
    return None

def encontrar_conta(numero,contas:list[Conta]):
    for conta in contas:
        if conta.numero == numero:
            return conta
        
    return None

def mostrar_contas(contas):
    resultado = ""
    for conta in contas:
        resultado += f"{conta} \n"
    return resultado


def menu():
    menu = """

    [d]     Depositar
    [s]     Sacar
    [e]     Extrato
    [ncl]   Novo Cliente
    [nc]    Nova Conta
    [lc]    Listar Contas
    [q]     Sair

    => """

    return menu

def sacar(clientes:list[pessoa_fisica]):
    cpf = input("digite o cpf do cliente: ")
    cliente = encontrar_cliente(cpf, clientes) 

    if cliente:
        contas = cliente.contas
        if not(contas):
            print("O cliente não possui nenhuma conta cadastrada, cadastre uma conta primeiro antes de realizar o deposito")
            return
        
        print(mostrar_contas(contas))
        numero = input("Informe o numero da conta para Sacar: ")
        conta = encontrar_conta(numero, contas)
        if conta:
            valor = float(input("Digite o valor para sacar: "))
            saque(valor).registrar(conta)
        else:
            print("Conta não encontrada")
            return
    else:
        print("Cliente não encontrado")
        return

def depositar(clientes:list[pessoa_fisica]):
    cpf = input("digite o cpf do cliente: ")
    cliente = encontrar_cliente(cpf, clientes) 

    if cliente:
        contas = cliente.contas
        if not(contas):
            print("O cliente não possui nenhuma conta cadastrada, cadastre uma conta primeiro antes de realizar o deposito")
            return
        
        print(mostrar_contas(contas))
        numero = input("Informe o numero da conta para depositar: ")
        conta = encontrar_conta(numero, contas)
        if conta:
            valor = float(input("Digite o valor para depositar: "))
            deposito(valor).registrar(conta)
        else:
            print("Conta não encontrada")
            return
    else:
        print("Cliente não encontrado")
        return

def registrar_cliente(clientes:list[pessoa_fisica]):
    cpf = input("Digite o CPF do novo cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if cliente:
        print("Esse cliente já existe")
    else:
        endereco = input("Digite o endereço do cliente: ")
        nome = input("Digite o nome do cliente: ")
        data_nascimento = input("Digite a data de nascimento no formado DD/MM/AAAA: ")
        clientes.append(pessoa_fisica(endereco,cpf,nome,data_nascimento))
    
    return clientes

def criar_conta(clientes:list[pessoa_fisica], contas:list[Conta]):
    cpf = input("Digite o CPF do novo cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if cliente:
        numero_conta = len(contas) + 1
        conta = conta_corrente(numero_conta,cliente)
        cliente.adicionar_conta(conta)
        contas.append(conta)
        print("Conta criada com sucesso")
    else:
        print("Cliente não encontrado")
    
def mostrar_extrato(clientes:list[pessoa_fisica]):
    cpf = input("Digite o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if cliente:
        contas = cliente.contas
        if not(contas):
            print("O cliente não possui nenhuma conta cadastrada, cadastre uma conta primeiro")
            return
        
        print(mostrar_contas(contas))
        numero = input("Informe o numero da conta para extrato: ")
        conta = encontrar_conta(numero, contas)
        if conta:
            historico = conta.historico.transacoes
            if historico:
                print("Tipo:        Valor:              Data:")
                for transacao in historico:
                    print(f"{transacao['tipo']}       {transacao['valor']}              {transacao['data']}")
            else:
                print("nenhuma transação realizada")

        else:
            print("Conta não encontrada")
            return
    else:
        print("cliente não encontrado")
        return


def main():

    clientes = list[pessoa_fisica]()
    contas = list[Conta]()

    while True:
        opcao = input(menu())

        if opcao == "d": # [d] Depositar
            depositar(clientes)

        elif opcao == "s": # [s] Sacar
            sacar(clientes)

        elif opcao == "e": # [e] Extrato
            mostrar_extrato(clientes)

        elif opcao == "ncl": # [ncl] Novo Cliente
            registrar_cliente(clientes)

        elif opcao == "nc": # [nc] Nova Conta
            criar_conta(clientes,contas)

        elif opcao == "lc": # [lc] Listar Contas
            if len (contas) > 0:
                print(mostrar_contas(contas))
            else:
                print("nenhuma conta registrada")

        elif opcao == "q": # [q] Sair
            return

    


main()