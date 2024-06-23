menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
extrato_modificado = False

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            extrato_modificado = True

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        if valor > 0:
          excedeu_saldo = valor > saldo
          excedeu_limite = valor > limite
          excedeu_saques = numero_saques >= LIMITE_SAQUES
          
          if excedeu_saldo:
              print("Operação falhou! Você não tem saldo suficiente.")

          elif excedeu_limite:
              print("Operação falhou! O valor do saque excede o limite.")

          elif excedeu_saques:
              print("Operação falhou! Número máximo de saques excedido.")

          else:
              saldo -= valor
              extrato += f"Saque: R$ {valor:.2f}\n"
              extrato_modificado = True
              numero_saques += 1
        else:
            print("Operação falhou! O valor informado é inválido.")
            
    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"Saldo: R$ {saldo:.2f}")
        print("==========================================")
        extrato_modificado = False

    elif opcao == "q":
        if extrato_modificado:
          print("\n================ EXTRATO ================")
          print("Não foram realizadas movimentações." if not extrato else extrato)
          print(f"Saldo: R$ {saldo:.2f}")
          print("==========================================")
        print("Obrigado, volte sempre!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

