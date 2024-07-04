def menu():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
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



def main():

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    extrato_modificado = False

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

        elif opcao == "q":
            if extrato_modificado:
                exibir_extrato(saldo, extrato=extrato)
            print("Obrigado, volte sempre!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()