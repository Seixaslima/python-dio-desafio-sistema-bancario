from abc import ABC,abstractmethod

class cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self):
        pass

    def adicionar_conta(self):
        pass

class pessoa_fisica(cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class conta:
    def __init__(self,saldo,numero,agencia,cliente):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico()
    
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

class conta_corrente(conta):
    def __init__(self, saldo, numero, agencia, cliente, limite, limite_saque):
        super().__init__(saldo, numero, agencia, cliente)
        self._limite = limite
        self._limite_saque = limite_saque

    
class transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(cls,conta):
        pass

class deposito(transacao):
    def __init__(self,valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    

    def registrar(self, conta):
        pass
        
    
class saque(transacao):
    def __init__(self,valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        pass


class historico:
    def __init__(self) -> None:
        self._transacoes =  []
    
    def adicionar_transacao(self,transacao):
        self._transacoes.append(transacao)


def menu():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuario
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair

    => """

    return menu

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    sucesso = False
    if valor > 0:
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= limite_saques
        
        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            sucesso = True
            numero_saques += 1
            print("Saque realizado com sucesso")
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato, sucesso

def depositar(saldo, valor, extrato, /):
    sucesso = False

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        sucesso = True
        print("Deposito realizado com sucesso")

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, sucesso

def exibir_extrato(saldo, / , * , extrato ):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = buscar_usuario(cpf, usuarios)
    if usuario:
        print("Usuario ja está cadastrado")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"cpf":cpf, "nome":nome, "data_nascimento":data_nascimento, "endereco":endereco})
    print("Usuario criado com sucesso")

def buscar_usuario(cpf, usuarios):
    for usuario in usuarios: 
        if usuario["cpf"] == cpf:
            return usuario

def criar_conta(contas, usuarios):
    agencia = "0001"
    numero = len(contas) + 1
    cpf = input("Informe o cpf do titular da conta")
    usuario = buscar_usuario(cpf, usuarios)

    if usuario:
        contas.append({"agencia":agencia, "numero":numero, "usuario":usuario})
        print("Conta criada com sucesso")
    else:
        print("Usuario não encontrado")
        print("Não foi possivel criar a conta")

def listar_contas(contas):
    if len(contas) > 0:
        for conta in contas:
            print(f'Agencia: {conta["agencia"]}, Número: {conta["numero"]}, Titular: {conta["usuario"]["nome"]}')
    else:
        print("Nenhuma conta cadastrada")


def main():

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    extrato_modificado = False

    usuarios = []
    contas = []

    while True:

        opcao = input(menu())

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato, sucesso = depositar(saldo, valor, extrato)
            if sucesso:
                extrato_modificado = True

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato, sucesso = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                limite_saques=LIMITE_SAQUES,
                numero_saques=numero_saques
            )
            if sucesso:
                extrato_modificado = True
                
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
            extrato_modificado = False

        elif opcao == "nu":
            criar_usuario(usuarios)
        
        elif opcao == "nc":
            criar_conta(contas, usuarios)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            if extrato_modificado:
                exibir_extrato(saldo, extrato=extrato)
            print("Obrigado, volte sempre!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()