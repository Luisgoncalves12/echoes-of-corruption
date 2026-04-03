from .db import carregar_personagem, inicializar_banco, listar_personagens
from .engine import criar_personagem, menu_jogador


def escolher_personagem_salvo():
    personagens = listar_personagens()

    if not personagens:
        print("Nenhum personagem salvo encontrado.")
        return None

    print("\n===== PERSONAGENS SALVOS =====")
    for indice, personagem in enumerate(personagens, start=1):
        nome, classe, nivel, xp, ouro = personagem
        print(f"{indice} - {nome} | Classe: {classe} | Nivel: {nivel} | XP: {xp} | Ouro: {ouro}")

    print(f"{len(personagens) + 1} - Voltar")

    while True:
        escolha = input("Escolha: ")

        if not escolha.isdigit():
            print("Opcao invalida!")
            continue

        escolha_numero = int(escolha)

        if 1 <= escolha_numero <= len(personagens):
            nome = personagens[escolha_numero - 1][0]
            return carregar_personagem(nome)

        if escolha_numero == len(personagens) + 1:
            return None

        print("Opcao invalida!")


def menu_principal():
    inicializar_banco()
    personagem = None

    while True:
        print("""
1 - Criar novo personagem
2 - Carregar jogo
3 - Continuar
4 - Sair
""")
        escolha = input("Escolha: ")

        if escolha == "1":
            personagem = criar_personagem()
            if personagem is not None:
                menu_jogador(personagem)
        elif escolha == "2":
            personagem = escolher_personagem_salvo()
            if personagem is not None:
                print(f'\nPersonagem "{personagem["nome"]}" carregado com sucesso!')
                menu_jogador(personagem)
        elif escolha == "3":
            if personagem is None:
                print("Nenhum personagem carregado no momento.")
            else:
                menu_jogador(personagem)
        elif escolha == "4":
            print("Saindo do jogo...")
            break
        else:
            print("Opcao invalida!")


def main():
    menu_principal()
