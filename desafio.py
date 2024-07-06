from abc import ABC,abstractmethod

class cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class pessoa_fisica(cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
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
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
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

class conta_corrente(conta):
    def __init__(self, saldo, numero, agencia, cliente, limite, limite_saque):
        super().__init__(saldo, numero, agencia, cliente)
        self._limite = limite
        self._limite_saque = limite_saque

    def sacar(self, valor):
        if valor > 0:
            excedeu_saldo = valor > self._saldo
            excedeu_limite = valor > self._limite
            excedeu_saques = False
            
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

    
class transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self,conta):
        pass

class deposito(transacao):
    def __init__(self,valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        
    
class saque(transacao):
    def __init__(self,valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class historico:
    def __init__(self) -> None:
        self._transacoes =  []
    
    def adicionar_transacao(self,transacao):
        self._transacoes.append(transacao)

    @property
    def transacoes(self):
        return self._transacoes




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