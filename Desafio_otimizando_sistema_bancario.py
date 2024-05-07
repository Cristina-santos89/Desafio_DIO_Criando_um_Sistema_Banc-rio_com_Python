import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar 
    [s]\tSacar
    [r]\tRecarregar   
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def lista_operadoras():
    operadoras = """\n
    ================ Operadoras ================
    [1]\tClaro
    [2]\tOI
    [3]\tVivo 
    [4]\tTim
=> """
    return input(textwrap.dedent(operadoras))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("Depósito realizado com sucesso")
    else:
        print("\nFalha na operação! O valor informado é inválido.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nFalha na operação! Saldo insuficiente.")

    elif excedeu_limite:
        print("\nFalha na operação! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("\nFalha na operação! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\nSaque realizado com sucesso!")

    else:
        print("\nFalha na operação! O valor informado é inválido")

    return saldo, extrato


def recarregar(*, saldo, valor, extrato, limite_recarga):
    excedeu_saldo_recarga = valor > saldo
    excedeu_limite_recarga = valor > limite_recarga

    if excedeu_saldo_recarga:
        print("\nFalha na operação! Saldo insuficiente.")

    elif excedeu_limite_recarga:
        print("\nFalha na operação! O valor da recarga excede o limite.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Recarga:\tR$ {valor:.2f}\n"
        print("Recarga realizada com sucesso!")

    else:
        print("\nFalha na operação! O valor informado é inválido")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n---------------- EXTRATO ----------------")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("-------------------------------------------")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 50)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    limite_recarga = 100
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []



    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "r":
            lista_operadoras()
            valor = float(input("Informe o valor da recarga: "))


            saldo, extrato = recarregar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite_recarga=limite_recarga,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
            print(f"\n limite saque R$: {limite * LIMITE_SAQUES}")
            print(f"\n limite recarga R$: {limite_recarga}")
            print("-------------------------------------------")
        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Falha na operação! Por favor selecione novamente a operação desejada.")


main()
