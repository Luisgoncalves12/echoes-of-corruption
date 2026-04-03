import random

from .db import salvar_personagem
from .world import ITENS_LOJA, MELHORIAS_FERREIRO, ORDEM_PROGRESSAO, PACTO_SOMBRIO, buscar_area


def criar_estado_inicial(vida_base, mana_base):
    return {
        "hp_atual": vida_base,
        "mana_atual": mana_base,
        "local_atual": "Vila Inicial",
        "areas_liberadas": ["Vila Inicial", "Floresta Sombria"],
        "bosses_derrotados": [],
        "efeitos": {},
        "arma_bonus": 0,
        "armadura_bonus": 0,
        "arma_nivel": 0,
        "armadura_nivel": 0,
        "atributos": {"forca": 8, "agilidade": 8, "inteligencia": 8},
        "equipamentos": {"arma": None, "armadura": None, "acessorio": None},
        "maestria": {},
        "materiais": {"Ferro": 0, "Aco": 0, "Cristal": 0, "Essencia Sombria": 0},
        "pacto_sombrio": {
            "encontros": 0,
            "bencoes": [],
            "bloqueio_cura_turnos": 0,
            "efeito_escondido": False,
        },
        "combate": {"pocoes_usadas": 0, "cooldown_pocao": 0, "cooldowns": {}},
        "missoes": {"eliminacoes": 0, "meta": 3, "recompensa_ouro": 40, "recompensa_item": "Pocao media"},
        "moral": 0,
        "corrupcao": 0,
        "campanha_concluida": False,
        "tipo_final": None,
        "historia": {
            "prologo_visto": False,
            "ato_vila": False,
            "crianca_vila": False,
            "guarda_vila": False,
            "sabio_saida": False,
            "mercenario_floresta": False,
            "missao_mercenario": False,
            "altar_floresta": False,
            "boss_floresta_dialogo": False,
            "altar_escolha": None,
            "aldeao_floresta": None,
            "poder_sombrio_lobo": False,
            "campos_intro": False,
            "mercenario_campos": False,
            "caverna_intro": False,
            "npc_preso_caverna": False,
            "boss_caverna_dialogo": False,
        },
    }


def vida_maxima(campeao):
    return campeao["vida"] + bonus_equipamento(campeao, "vida")


def ataque_total(campeao):
    return campeao["atk"] + campeao["estado"]["arma_bonus"] + bonus_equipamento(campeao, "atk")


def defesa_total(campeao):
    return campeao["def"] + campeao["estado"]["armadura_bonus"] + bonus_equipamento(campeao, "def")


def mana_maxima(campeao):
    return campeao["mana"] + bonus_equipamento(campeao, "mana")


def bonus_equipamento(campeao, chave):
    total = 0
    for slot in campeao["estado"]["equipamentos"].values():
        if isinstance(slot, dict):
            total += slot.get(chave, 0)
    return total


def atributo_total(campeao, nome):
    return campeao["estado"]["atributos"].get(nome, 0)


def nome_equipado(campeao, slot):
    item = campeao["estado"]["equipamentos"].get(slot)
    if isinstance(item, dict):
        return item.get("nome")
    return None


def atende_requisito(campeao, item):
    for atributo, valor in item.get("requisito", {}).items():
        if atributo_total(campeao, atributo) < valor:
            return False
    return True


def habilidades_da_classe(campeao):
    habilidades = {
        "Tank": [
            {"id": "golpe_pesado", "nome": "Golpe Pesado", "mana": 0, "cooldown": 2, "descricao": "Ataque forte inspirado em guerreiros de RPG."},
            {"id": "muralha", "nome": "Muralha", "mana": 14, "cooldown": 3, "descricao": "Eleva sua defesa por 2 turnos."},
        ],
        "Mago": [
            {"id": "bola_fogo_jogador", "nome": "Bola de Fogo", "mana": 16, "cooldown": 1, "descricao": "Magia ofensiva classica."},
            {"id": "congelar", "nome": "Congelar", "mana": 20, "cooldown": 3, "descricao": "Causa dano e pode travar o inimigo."},
        ],
        "Guerreiro": [
            {"id": "corte_heroico", "nome": "Corte Heroico", "mana": 10, "cooldown": 1, "descricao": "Golpe consistente de espadachim."},
            {"id": "grito_guerra", "nome": "Grito de Guerra", "mana": 12, "cooldown": 3, "descricao": "Aumenta seu ataque por 3 turnos."},
        ],
        "Arqueiro": [
            {"id": "tiro_duplo", "nome": "Tiro Duplo", "mana": 12, "cooldown": 2, "descricao": "Dispara duas vezes no mesmo turno."},
            {"id": "tiro_preciso", "nome": "Tiro Preciso", "mana": 10, "cooldown": 2, "descricao": "Ataque com alta chance critica."},
        ],
        "Assassino": [
            {"id": "ataque_sombrio", "nome": "Ataque Sombrio", "mana": 12, "cooldown": 2, "descricao": "Explosao de dano com chance de sangramento."},
            {"id": "bomba_fumaca", "nome": "Bomba de Fumaca", "mana": 10, "cooldown": 3, "descricao": "Aumenta sua esquiva por 2 turnos."},
        ],
        "Paladino": [
            {"id": "golpe_sagrado", "nome": "Golpe Sagrado", "mana": 15, "cooldown": 2, "descricao": "Dano e pequena cura."},
            {"id": "aura_protetora", "nome": "Aura Protetora", "mana": 16, "cooldown": 3, "descricao": "Aumenta defesa por 3 turnos."},
        ],
        "Bruxo": [
            {"id": "maldicao", "nome": "Maldicao", "mana": 14, "cooldown": 2, "descricao": "Reduz a defesa do inimigo."},
            {"id": "dreno_vital", "nome": "Dreno Vital", "mana": 16, "cooldown": 2, "descricao": "Rouba vida do alvo."},
        ],
        "Invocador": [
            {"id": "familiar_arcano", "nome": "Familiar Arcano", "mana": 18, "cooldown": 3, "descricao": "Reforca seu ataque por 3 turnos."},
            {"id": "ruptura_astral", "nome": "Ruptura Astral", "mana": 22, "cooldown": 3, "descricao": "Explosao magica pesada."},
        ],
    }
    return habilidades.get(campeao["classe"], [])


def cooldown_atual(campeao, habilidade_id):
    return campeao["estado"]["combate"]["cooldowns"].get(habilidade_id, 0)


def reduzir_cooldowns(campeao):
    cooldowns = campeao["estado"]["combate"]["cooldowns"]
    atualizados = {}
    for habilidade_id, turnos in cooldowns.items():
        if turnos > 1:
            atualizados[habilidade_id] = turnos - 1
    campeao["estado"]["combate"]["cooldowns"] = atualizados


def mostrar_status(campeao):
    print(f"""
===== STATUS DE {campeao["nome"].upper()} =====
Classe: {campeao["classe"]}
Nivel: {campeao["nivel"]}
XP: {campeao["xp"]}
Ouro: {campeao["ouro"]}
Local: {campeao["estado"]["local_atual"]}
Pontos para distribuir: {campeao["pontos_atributo"]}

Vida: {campeao["estado"]["hp_atual"]}/{vida_maxima(campeao)}
Mana: {campeao["estado"]["mana_atual"]}/{mana_maxima(campeao)}
Atk: {campeao["atk"]} (+{campeao["estado"]["arma_bonus"]} forja / +{bonus_equipamento(campeao, "atk")} equip)
Def: {campeao["def"]} (+{campeao["estado"]["armadura_bonus"]} forja / +{bonus_equipamento(campeao, "def")} equip)
Crit: {campeao["crit"]}
Esq: {campeao["esq"]}
Forca: {atributo_total(campeao, "forca")}
Agilidade: {atributo_total(campeao, "agilidade")}
Inteligencia: {atributo_total(campeao, "inteligencia")}
Arma: {nome_equipado(campeao, "arma") or "Nenhuma"}
Armadura: {nome_equipado(campeao, "armadura") or "Nenhuma"}
Acessorio: {nome_equipado(campeao, "acessorio") or "Nenhum"}
Materiais: Ferro {campeao["estado"]["materiais"]["Ferro"]} | Aco {campeao["estado"]["materiais"]["Aco"]} | Cristal {campeao["estado"]["materiais"]["Cristal"]} | Essencia Sombria {campeao["estado"]["materiais"]["Essencia Sombria"]}
Bosses derrotados: {len(campeao["estado"]["bosses_derrotados"])}
Moral: {campeao["estado"]["moral"]}
Corrupcao: {campeao["estado"]["corrupcao"]}
""")


def mostrar_inventario(campeao):
    print(f'\n===== INVENTARIO DE {campeao["nome"].upper()} =====')

    if not campeao["inventario"]:
        print("Inventario vazio.")
        return

    grupos = {"Consumiveis": {}, "Armas": {}, "Armaduras": {}, "Acessorios": {}, "Outros": {}}
    for item in campeao["inventario"]:
        dados = ITENS_LOJA.get(item, {})
        tipo = dados.get("tipo")
        if tipo in ("cura", "mana"):
            grupo = "Consumiveis"
        elif tipo == "arma":
            grupo = "Armas"
        elif tipo == "armadura":
            grupo = "Armaduras"
        elif tipo == "acessorio":
            grupo = "Acessorios"
        else:
            grupo = "Outros"
        grupos[grupo][item] = grupos[grupo].get(item, 0) + 1

    for grupo, itens in grupos.items():
        if not itens:
            continue
        print(f"\n{grupo}:")
        for item, quantidade in itens.items():
            print(f"- {item} x{quantidade}")


def gerenciar_equipamentos(campeao):
    while True:
        print(f"""
===== EQUIPAMENTOS =====
Arma: {nome_equipado(campeao, "arma") or "Nenhuma"}
Armadura: {nome_equipado(campeao, "armadura") or "Nenhuma"}
Acessorio: {nome_equipado(campeao, "acessorio") or "Nenhum"}
1 - Equipar item do inventario
2 - Voltar
""")
        escolha = input("Escolha: ")
        if escolha == "2":
            break
        if escolha != "1":
            print("Opcao invalida!")
            continue

        mostrar_inventario(campeao)
        nome_item = input("Digite o nome do item para equipar: ").strip()
        if nome_item not in campeao["inventario"]:
            print("Item nao encontrado.")
            continue

        dados = ITENS_LOJA.get(nome_item)
        if dados is None or dados.get("tipo") not in ("arma", "armadura", "acessorio"):
            print("Esse item nao pode ser equipado.")
            continue

        slot = dados["tipo"]
        item_equipado = campeao["estado"]["equipamentos"].get(slot)
        if item_equipado is not None:
            campeao["inventario"].append(item_equipado["nome"])

        campeao["inventario"].remove(nome_item)
        dados_equipados = dict(dados)
        dados_equipados["nome"] = nome_item
        dados_equipados["upgrade"] = campeao["estado"]["maestria"].get(nome_item, {}).get("upgrade", 0)
        campeao["estado"]["equipamentos"][slot] = dados_equipados
        print(f"{nome_item} equipado em {slot}.")

        if not atende_requisito(campeao, dados_equipados):
            print("Voce nao atende ao requisito total do item. Ainda pode usar, mas sofrera penalidades.")

        salvar_personagem(campeao)


def ajustar_alinhamento(campeao, moral=0, corrupcao=0):
    campeao["estado"]["moral"] += moral
    campeao["estado"]["corrupcao"] += corrupcao
    salvar_personagem(campeao)


def tendencia_moral(campeao):
    historia = campeao["estado"]["historia"]
    if campeao["estado"]["corrupcao"] >= 3 or historia["aldeao_floresta"] == "matar":
        return "mal"
    if campeao["estado"]["moral"] >= 3 or historia["aldeao_floresta"] == "salvar":
        return "bom"
    return "neutro"


def _ler_escolha_valida(opcoes_validas):
    while True:
        escolha = input("Escolha: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("Opcao invalida!")


def tocar_prologo(campeao):
    historia = campeao["estado"]["historia"]
    if historia["prologo_visto"]:
        return

    print('\n[ Voz Sombria ]')
    print('"Voce esta acordando..."')
    print('"Mas ainda nao entende o que carrega."')
    print('"Quando chegar a hora... voce vai precisar de mim."')
    historia["prologo_visto"] = True
    salvar_personagem(campeao)


def evento_vila_inicial(campeao):
    historia = campeao["estado"]["historia"]
    if historia["ato_vila"]:
        return

    print('\n[ Sabio ]')
    print('"Ah... entao voce finalmente despertou."')
    print('"Ha algo errado neste mundo. Eu sinto... e agora voce tambem sente."')
    print('"Uma forca antiga esta voltando."')
    print("1 - Eu vou ajudar.")
    print("2 - Nao e problema meu.")
    print("3 - Quero poder.")
    escolha = _ler_escolha_valida({"1", "2", "3"})

    if escolha == "1":
        print('"Entao ainda existe esperanca."')
        ajustar_alinhamento(campeao, moral=2)
    elif escolha == "2":
        print('"Todos dizem isso... ate ser tarde demais."')
    else:
        print('"...cuidado com o que deseja."')
        ajustar_alinhamento(campeao, corrupcao=2)

    print('\n[ Crianca ]')
    print('"Voce e um aventureiro?"')
    print('"Voce vai lutar contra os monstros?"')
    print("1 - Sim, vou proteger todos.")
    print("2 - Vou tentar...")
    print("3 - Nao conte comigo.")
    escolha = _ler_escolha_valida({"1", "2", "3"})

    if escolha == "1":
        print('"Sabia! Voce e um heroi!"')
        ajustar_alinhamento(campeao, moral=2)
    elif escolha == "2":
        print('"So... nao desista, ta?"')
        ajustar_alinhamento(campeao, moral=1)
    else:
        print('"...entao quem vai salvar a gente?"')
        ajustar_alinhamento(campeao, corrupcao=1)

    print('\n[ Guarda ]')
    print('"Relatorios estranhos vem da floresta."')
    print('"Animais estao mais agressivos... e pessoas estao sumindo."')
    print('"Se vai ajudar, comece por la."')

    print('\n[ Sabio ]')
    print('"A floresta era pacifica... antes."')
    print('"Volte vivo."')

    historia["ato_vila"] = True
    historia["crianca_vila"] = True
    historia["guarda_vila"] = True
    historia["sabio_saida"] = True
    salvar_personagem(campeao)


def evento_floresta_mercenario(campeao):
    historia = campeao["estado"]["historia"]
    if historia["mercenario_floresta"]:
        return

    print('\n[ Mercenario ]')
    print('"Olha so... mais um tentando bancar o heroi."')
    print('"Deixa eu te dar um conselho: herois morrem cedo."')
    print("1 - Prefiro fazer o certo.")
    print("2 - So quero sobreviver.")
    print("3 - Voce tem razao.")
    escolha = _ler_escolha_valida({"1", "2", "3"})

    if escolha == "1":
        print('"Entao vai morrer pobre tambem."')
        ajustar_alinhamento(campeao, moral=1)
    elif escolha == "2":
        print('"Heh... voce aprende rapido."')
    else:
        print('"Entao talvez voce sobreviva."')
        ajustar_alinhamento(campeao, corrupcao=1)

    print('\n[ Mercenario ]')
    print('"Tem um aldeao mais a frente."')
    print('"Carregando coisas valiosas."')
    print('"Voce resolve isso... e eu divido o ouro."')
    print("1 - Vou salvar o aldeao.")
    print("2 - Vou ignorar isso.")
    print("3 - Eu aceito matar.")
    escolha = _ler_escolha_valida({"1", "2", "3"})

    if escolha == "1":
        print('"Entao continua sendo fraco."')
        historia["aldeao_floresta"] = "salvar"
        ajustar_alinhamento(campeao, moral=2)
    elif escolha == "2":
        print('"Tanto faz. Menos ouro pra voce."')
        historia["aldeao_floresta"] = "ignorar"
    else:
        print('"Agora voce ta comecando a entender."')
        historia["aldeao_floresta"] = "matar"
        campeao["ouro"] += 35
        ajustar_alinhamento(campeao, corrupcao=3)
        print("Voce recebeu 35 ouro do acordo sujo.")

    historia["mercenario_floresta"] = True
    historia["missao_mercenario"] = True
    salvar_personagem(campeao)


def evento_altar_floresta(campeao):
    historia = campeao["estado"]["historia"]
    if historia["altar_floresta"]:
        return

    print('\n[ Altar Corrompido ]')
    print('"A energia vibra no ar..."')
    print('"Algo chama por voce..."')
    print("1 - Destruir.")
    print("2 - Ignorar.")
    print("3 - Tocar.")
    escolha = _ler_escolha_valida({"1", "2", "3"})

    if escolha == "1":
        print('"A energia se dissipa... com dificuldade."')
        historia["altar_escolha"] = "destruir"
        ajustar_alinhamento(campeao, corrupcao=-2)
        campeao["xp"] += 20
    elif escolha == "2":
        print('"Mas a sensacao continua..."')
        historia["altar_escolha"] = "ignorar"
    else:
        print('"O poder percorre seu corpo."')
        historia["altar_escolha"] = "absorver"
        ajustar_alinhamento(campeao, corrupcao=2)
        campeao["estado"]["mana_atual"] = min(campeao["mana"], campeao["estado"]["mana_atual"] + 20)
        campeao["pontos_atributo"] += 2

    historia["altar_floresta"] = True
    verificar_subida_nivel(campeao)
    salvar_personagem(campeao)


def evento_pos_boss_floresta(campeao):
    historia = campeao["estado"]["historia"]
    if historia["boss_floresta_dialogo"]:
        return

    print('\n"Esse animal... estava diferente."')
    print('"Algo esta corrompendo tudo."')

    print('\nUma presenca sombria sussurra ao seu redor.')
    print("1 - Recuar e resistir.")
    print("2 - Usar o poder sombrio por um instante.")
    escolha = _ler_escolha_valida({"1", "2"})

    if escolha == "2":
        historia["poder_sombrio_lobo"] = True
        ajustar_alinhamento(campeao, corrupcao=1)
        campeao["estado"]["mana_atual"] = min(campeao["mana"], campeao["estado"]["mana_atual"] + 10)
        print("O poder sombrio respondeu ao seu chamado.")
    else:
        print("Voce resistiu ao chamado sombrio.")

    historia["boss_floresta_dialogo"] = True
    salvar_personagem(campeao)


def evento_campos_abertos(campeao):
    historia = campeao["estado"]["historia"]
    if historia["campos_intro"]:
        return

    tendencia = tendencia_moral(campeao)
    print("\n===== CAMPOS ABERTOS =====")

    if tendencia == "bom":
        print('"Voce voltou! Por favor, nos ajude!"')
        print("Os aldeoes confiam em voce.")
        campeao["ouro"] += 20
        campeao["inventario"].append("Pocao media")
        print("Os aldeoes lhe deram 20 ouro e uma Pocao media.")
    elif tendencia == "neutro":
        print('"Voce... vai ajudar dessa vez?"')
        print("O povo esta desconfiado, mas ainda espera algo de voce.")
        campeao["ouro"] += 10
    else:
        print('"Fique longe da gente!"')
        print("Os aldeoes fogem ao notar sua presenca.")
        print("1 - Ignorar")
        print("2 - Saquear")
        print("3 - Intimidar")
        escolha = _ler_escolha_valida({"1", "2", "3"})
        if escolha == "2":
            campeao["ouro"] += 30
            ajustar_alinhamento(campeao, corrupcao=1)
            print("Voce saqueou o pouco que restava da aldeia.")
        elif escolha == "3":
            campeao["ouro"] += 15
            ajustar_alinhamento(campeao, corrupcao=1)
            print("Voce intimidou os aldeoes e arrancou recursos.")
        else:
            print("Voce seguiu adiante sem olhar para tras.")

    historia["campos_intro"] = True
    salvar_personagem(campeao)


def evento_mercenario_campos(campeao):
    historia = campeao["estado"]["historia"]
    if historia["mercenario_campos"]:
        return

    escolha_floresta = historia["aldeao_floresta"]
    print('\n[ Mercenario ]')

    if escolha_floresta == "salvar":
        print('"Ainda preso nessa moral fraca?"')
    elif escolha_floresta == "matar":
        print('"Heh... voce ja cruzou a linha."')
        print("Ele oferece uma rota mais sombria adiante.")
        ajustar_alinhamento(campeao, corrupcao=1)
    else:
        print('"Sabia que voce tinha potencial."')
        print("Ele o observa como se ainda estivesse decidindo seu valor.")

    historia["mercenario_campos"] = True
    salvar_personagem(campeao)


def evento_caverna_escura(campeao):
    historia = campeao["estado"]["historia"]
    if historia["caverna_intro"]:
        return

    corrupcao = campeao["estado"]["corrupcao"]
    print('\n[ Espirito Sombrio ]')
    if corrupcao <= 1:
        print('"Voce ainda resiste... interessante."')
    elif corrupcao <= 3:
        print('"Voce ja comecou a mudar..."')
    else:
        print('"Voce ja e meu."')

    print('"Eu posso mudar isso."')
    print("1 - Nunca.")
    print("2 - Que poder?")
    print("3 - Eu aceito.")
    escolha = _ler_escolha_valida({"1", "2", "3"})

    if escolha == "1":
        print('"Todos dizem isso... no comeco."')
        ajustar_alinhamento(campeao, moral=1)
    elif escolha == "2":
        print('"O suficiente."')
    else:
        print('"Eu sabia."')
        ajustar_alinhamento(campeao, corrupcao=2)
        campeao["pontos_atributo"] += 2

    encontro_pacto_sombrio(campeao)

    historia["caverna_intro"] = True
    salvar_personagem(campeao)


def evento_npc_preso_caverna(campeao):
    historia = campeao["estado"]["historia"]
    if historia["npc_preso_caverna"]:
        return

    print('\n[ NPC Preso ]')
    if tendencia_moral(campeao) == "bom":
        print('"Eu ouvi falar de voce... por favor..."')
    elif tendencia_moral(campeao) == "mal":
        print('"Fique longe de mim!"')
    else:
        print('"Por favor... me tire daqui..."')

    print('"Eu nao quero morrer aqui..."')
    print("1 - Vou te salvar.")
    print("2 - Nao posso ajudar.")
    print("3 - Seu sacrificio sera util.")
    escolha = _ler_escolha_valida({"1", "2", "3"})

    if escolha == "1":
        print('"Obrigado... eu nunca vou esquecer isso."')
        ajustar_alinhamento(campeao, moral=2)
        campeao["ouro"] += 20
    elif escolha == "2":
        print('"...eu entendo..."')
    else:
        print('"NAO-"')
        ajustar_alinhamento(campeao, corrupcao=2)
        campeao["estado"]["mana_atual"] = min(campeao["mana"], campeao["estado"]["mana_atual"] + 15)

    historia["npc_preso_caverna"] = True
    salvar_personagem(campeao)


def aplicar_modificadores_narrativos(campeao, area, jogador, inimigo, foi_boss):
    if area["nome"] == "Caverna Escura":
        if campeao["estado"]["corrupcao"] >= 3:
            jogador["atk"] += 2
            inimigo["atk"] += 2
            print("A corrupcao dentro da caverna alimenta a violencia do combate.")
        if campeao["estado"]["moral"] >= 3:
            jogador["def"] += 2
            jogador["hp"] += 10
            print("Sua conviccao lhe concede resistencia diante da escuridao.")
        if foi_boss and campeao["estado"]["corrupcao"] >= 4:
            inimigo["atk"] += 3
            inimigo["def"] += 2
            print("O boss respondeu a sua corrupcao e ficou mais forte.")


def verificar_subida_nivel(campeao):
    while campeao["xp"] >= campeao["nivel"] * 100:
        campeao["xp"] -= campeao["nivel"] * 100
        campeao["nivel"] += 1
        campeao["pontos_atributo"] += 5
        campeao["vida"] += 10
        campeao["mana"] += 5
        campeao["atk"] += 2
        campeao["def"] += 1
        campeao["estado"]["hp_atual"] = min(campeao["estado"]["hp_atual"] + 20, vida_maxima(campeao))
        campeao["estado"]["mana_atual"] = min(campeao["estado"]["mana_atual"] + 10, campeao["mana"])
        print(f'\n{campeao["nome"]} subiu para o nivel {campeao["nivel"]}!')
        print("Voce ganhou +10 vida, +5 mana, +2 atk, +1 def e +5 pontos de atributo.")


def distribuir_pontos(campeao):
    while campeao["pontos_atributo"] > 0:
        print(f"""
===== DISTRIBUIR PONTOS =====
Pontos disponiveis: {campeao["pontos_atributo"]}
1 - Forca (+1 forca, +1 atk)
2 - Agilidade (+1 agilidade, +1 crit, +1 esq)
3 - Inteligencia (+1 inteligencia, +5 mana)
4 - Vida (+5)
5 - Defesa (+1)
6 - Voltar
""")
        escolha = input("Escolha: ")

        if escolha == "1":
            campeao["estado"]["atributos"]["forca"] += 1
            campeao["atk"] += 1
        elif escolha == "2":
            campeao["estado"]["atributos"]["agilidade"] += 1
            campeao["crit"] += 1
            campeao["esq"] += 1
        elif escolha == "3":
            campeao["estado"]["atributos"]["inteligencia"] += 1
            campeao["mana"] += 5
            campeao["estado"]["mana_atual"] += 5
        elif escolha == "4":
            campeao["vida"] += 5
            campeao["estado"]["hp_atual"] += 5
        elif escolha == "5":
            campeao["def"] += 1
        elif escolha == "6":
            break
        else:
            print("Opcao invalida!")
            continue

        campeao["pontos_atributo"] -= 1
        salvar_personagem(campeao)


def aplicar_efeitos_no_inicio(personagem, nome_lado):
    efeitos = personagem["efeitos"]

    if efeitos.get("veneno", 0) > 0:
        personagem["hp"] -= 6
        efeitos["veneno"] -= 1
        print(f"{nome_lado} sofre 6 de dano por veneno.")

    if efeitos.get("sangramento", 0) > 0:
        personagem["hp"] -= 5
        efeitos["sangramento"] -= 1
        print(f"{nome_lado} sofre 5 de dano por sangramento.")

    if efeitos.get("stun", 0) > 0:
        efeitos["stun"] -= 1
        print(f"{nome_lado} esta atordoado neste turno.")
        return True

    if efeitos.get("buff_atk", 0) > 0:
        efeitos["buff_atk"] -= 1

    if efeitos.get("debuff_defesa", 0) > 0:
        efeitos["debuff_defesa"] -= 1
    if efeitos.get("buff_defesa", 0) > 0:
        efeitos["buff_defesa"] -= 1
    if efeitos.get("buff_esquiva", 0) > 0:
        efeitos["buff_esquiva"] -= 1

    return False


def aplicar_mecanica_area(area, personagem, nome_lado):
    if area["nome"] == "Deserto Esquecido":
        personagem["hp"] -= 3
        print(f"O calor do deserto causa 3 de dano em {nome_lado}.")


def chance_esquiva(valor_esq, area):
    bonus = 0
    if area["nome"] == "Floresta Sombria":
        bonus += 4
    return min(valor_esq + bonus, 60)


def dano_ataque(atacante_atk, defensor_def, critico):
    dano = max(1, int(atacante_atk - (defensor_def / 2)))
    if critico:
        dano *= 2
    return dano


def tentar_usar_item(campeao):
    combate_estado = campeao["estado"]["combate"]
    pacto = campeao["estado"]["pacto_sombrio"]

    if pacto.get("bloqueio_cura_turnos", 0) > 0:
        print("O Pacto Sombrio bloqueia sua cura por enquanto.")
        return False

    if combate_estado["pocoes_usadas"] >= 3:
        print("Voce atingiu o limite de 3 pocoes neste combate.")
        return False

    if combate_estado["cooldown_pocao"] > 0:
        print(f"Voce precisa esperar {combate_estado['cooldown_pocao']} turno(s) para beber outra pocao.")
        return False

    if not campeao["inventario"]:
        print("Voce nao possui itens.")
        return False

    mostrar_inventario(campeao)
    item = input("Digite o nome do item para usar: ").strip()

    if item not in campeao["inventario"]:
        print("Item nao encontrado no inventario.")
        return False

    dados_item = ITENS_LOJA.get(item)
    if dados_item is None:
        print("Esse item ainda nao pode ser usado.")
        return False

    if dados_item["tipo"] == "cura":
        campeao["inventario"].remove(item)
        cura = dados_item["cura"]
        campeao["estado"]["hp_atual"] = min(campeao["estado"]["hp_atual"] + cura, vida_maxima(campeao))
        combate_estado["pocoes_usadas"] += 1
        combate_estado["cooldown_pocao"] = 2
        print(f"Voce usou {item} e recuperou {cura} de vida.")
        salvar_personagem(campeao)
        return True

    if dados_item["tipo"] == "mana":
        campeao["inventario"].remove(item)
        cura = dados_item["cura"]
        campeao["estado"]["mana_atual"] = min(campeao["estado"]["mana_atual"] + cura, mana_maxima(campeao))
        combate_estado["pocoes_usadas"] += 1
        combate_estado["cooldown_pocao"] = 2
        print(f"Voce usou {item} e recuperou {cura} de mana.")
        salvar_personagem(campeao)
        return True

    return False


def criar_inimigo(dados_base):
    inimigo = dict(dados_base)
    inimigo["hp"] = inimigo["vida"]
    inimigo["efeitos"] = {}
    inimigo["defendendo"] = False
    inimigo["reviveu"] = False
    return inimigo


def criar_combatente_jogador(campeao):
    arma = campeao["estado"]["equipamentos"].get("arma")
    armadura = campeao["estado"]["equipamentos"].get("armadura")
    acessorio = campeao["estado"]["equipamentos"].get("acessorio")

    atk = ataque_total(campeao)
    defesa = defesa_total(campeao)
    crit = campeao["crit"] + bonus_equipamento(campeao, "crit")
    esq = campeao["esq"] + bonus_equipamento(campeao, "esq")
    mana_total = mana_maxima(campeao)
    penalidades = {"erro_extra": 0, "custo_mana_extra": 0}
    dano_percentual = 0

    if arma:
        atk += arma.get("upgrade", 0)
        categoria = arma.get("categoria")
        if not atende_requisito(campeao, arma):
            atk = max(1, int(atk * 0.5))
            if categoria == "arco":
                penalidades["erro_extra"] += 20
            if categoria == "cajado":
                penalidades["custo_mana_extra"] += 10
        if categoria == "machado" and atributo_total(campeao, "forca") >= 15:
            atk += 3

    if armadura and not atende_requisito(campeao, armadura):
        defesa = max(0, defesa - 5)

    if acessorio:
        mana_total += acessorio.get("mana", 0)

    for bencao in campeao["estado"]["pacto_sombrio"]["bencoes"]:
        dano_percentual += bencao.get("dano_percentual", 0)

    return {
        "nome": campeao["nome"],
        "hp": campeao["estado"]["hp_atual"],
        "atk": atk,
        "def": defesa,
        "crit": crit,
        "esq": esq,
        "esq_base": esq,
        "mana_total": mana_total,
        "penalidades": penalidades,
        "dano_percentual": dano_percentual,
        "efeitos": dict(campeao["estado"].get("efeitos", {})),
        "defendendo": False,
    }


def escolher_acao_inimigo(inimigo):
    if inimigo["ia"] == "agressivo":
        return "atacar"
    if inimigo["ia"] == "defensivo":
        return random.choice(["atacar", "defender", "atacar"])
    if inimigo["ia"] == "estrategico":
        return random.choice(["atacar", "defender", "atacar", "habilidade"])
    return "atacar"


def aplicar_efeito(efeito, alvo):
    if efeito == "veneno":
        alvo["efeitos"]["veneno"] = 3
    elif efeito == "sangramento":
        alvo["efeitos"]["sangramento"] = 3
    elif efeito == "debuff_defesa":
        alvo["efeitos"]["debuff_defesa"] = 2
    elif efeito == "stun":
        alvo["efeitos"]["stun"] = 1
    elif efeito == "buff_defesa":
        alvo["efeitos"]["buff_defesa"] = 2
    elif efeito == "buff_esquiva":
        alvo["efeitos"]["buff_esquiva"] = 2


def ataque(atacante, defensor, area, efeito_extra=None):
    chance_erro = 0
    if area["nome"] == "Lago Amaldicoado":
        chance_erro = 12
    chance_erro += atacante.get("penalidades", {}).get("erro_extra", 0)

    if random.randint(1, 100) <= chance_erro:
        print(f"{atacante['nome']} errou o ataque por causa da nevoa!")
        return

    esquiva_defensor = defensor["esq"]
    if defensor["efeitos"].get("buff_esquiva", 0) > 0:
        esquiva_defensor += 15

    if random.randint(1, 100) <= chance_esquiva(esquiva_defensor, area):
        print(f"{defensor['nome']} esquivou do ataque!")
        return

    critico = random.randint(1, 100) <= atacante["crit"]
    defesa_alvo = defensor["def"] // 2 if defensor["defendendo"] else defensor["def"]

    if defensor["efeitos"].get("debuff_defesa", 0) > 0:
        defesa_alvo = max(0, defesa_alvo - 3)
    if defensor["efeitos"].get("buff_defesa", 0) > 0:
        defesa_alvo += 4

    ataque_base = atacante["atk"]
    if atacante["efeitos"].get("buff_atk", 0) > 0:
        ataque_base += 4
    ataque_base = int(ataque_base * (1 + atacante.get("dano_percentual", 0)))

    dano = dano_ataque(ataque_base, defesa_alvo, critico)
    defensor["hp"] -= dano
    print(f"{atacante['nome']} causou {dano} de dano em {defensor['nome']}.")

    if critico:
        print("Foi um ataque critico!")

    if efeito_extra is not None and defensor["hp"] > 0 and random.randint(1, 100) <= 35:
        aplicar_efeito(efeito_extra, defensor)
        print(f"{defensor['nome']} recebeu o efeito {efeito_extra}.")


def registrar_maestria(campeao):
    arma = nome_equipado(campeao, "arma")
    if arma is None:
        return

    maestria = campeao["estado"]["maestria"].setdefault(arma, {"uso": 0, "upgrade": 0})
    maestria["uso"] += 1
    if arma.startswith("Espada") and maestria["uso"] in (5, 10):
        maestria["upgrade"] += 1
        print(f"Sua maestria com {arma} aumentou. +1 dano com essa arma.")
    if "Arco" in arma and maestria["uso"] in (5, 10):
        campeao["crit"] += 1
        print(f"Sua maestria com {arma} aumentou. +1 crit permanente.")


def usar_habilidade(campeao, jogador, inimigo, area):
    habilidades = habilidades_da_classe(campeao)
    if not habilidades:
        print("Sua classe ainda nao possui habilidades.")
        return False

    print("\n===== HABILIDADES =====")
    opcoes_validas = set()
    for indice, habilidade in enumerate(habilidades, start=1):
        cd = cooldown_atual(campeao, habilidade["id"])
        estado_cd = f"CD {cd}" if cd > 0 else "Pronta"
        print(f"{indice} - {habilidade['nome']} | Mana {habilidade['mana']} | {estado_cd}")
        print(habilidade["descricao"])
        opcoes_validas.add(str(indice))
    voltar = str(len(habilidades) + 1)
    print(f"{voltar} - Voltar")
    opcoes_validas.add(voltar)

    escolha = _ler_escolha_valida(opcoes_validas)
    if escolha == voltar:
        return False

    habilidade = habilidades[int(escolha) - 1]
    if cooldown_atual(campeao, habilidade["id"]) > 0:
        print("Essa habilidade ainda esta em cooldown.")
        return False

    custo_mana = habilidade["mana"] + jogador.get("penalidades", {}).get("custo_mana_extra", 0)
    if campeao["estado"]["mana_atual"] < custo_mana:
        print("Mana insuficiente.")
        return False

    campeao["estado"]["mana_atual"] -= custo_mana
    campeao["estado"]["combate"]["cooldowns"][habilidade["id"]] = habilidade["cooldown"] + 1
    habilidade_id = habilidade["id"]

    if habilidade_id == "golpe_pesado":
        dano = max(1, int((jogador["atk"] * 1.8) - (inimigo["def"] / 2)))
        inimigo["hp"] -= dano
        print(f"Golpe Pesado causou {dano} de dano.")
    elif habilidade_id == "muralha":
        aplicar_efeito("buff_defesa", jogador)
        print("Voce ergueu uma Muralha e ganhou defesa extra.")
    elif habilidade_id == "bola_fogo_jogador":
        dano = max(1, int((jogador["atk"] + atributo_total(campeao, "inteligencia")) - (inimigo["def"] / 3)))
        inimigo["hp"] -= dano
        print(f"Bola de Fogo causou {dano} de dano magico.")
    elif habilidade_id == "congelar":
        dano = max(1, int((jogador["atk"] * 1.2) - (inimigo["def"] / 3)))
        inimigo["hp"] -= dano
        aplicar_efeito("stun", inimigo)
        print(f"Congelar causou {dano} de dano e travou o inimigo.")
    elif habilidade_id == "corte_heroico":
        dano = max(1, int((jogador["atk"] * 1.5) - (inimigo["def"] / 2)))
        inimigo["hp"] -= dano
        print(f"Corte Heroico causou {dano} de dano.")
    elif habilidade_id == "grito_guerra":
        jogador["efeitos"]["buff_atk"] = 3
        print("Seu ataque aumentou por 3 turnos.")
    elif habilidade_id == "tiro_duplo":
        print("Voce disparou duas flechas.")
        ataque(jogador, inimigo, area)
        if inimigo["hp"] > 0:
            ataque(jogador, inimigo, area)
    elif habilidade_id == "tiro_preciso":
        crit_original = jogador["crit"]
        jogador["crit"] += 35
        ataque(jogador, inimigo, area)
        jogador["crit"] = crit_original
    elif habilidade_id == "ataque_sombrio":
        dano = max(1, int((jogador["atk"] * 1.7) - (inimigo["def"] / 2)))
        inimigo["hp"] -= dano
        if random.randint(1, 100) <= 60:
            aplicar_efeito("sangramento", inimigo)
        print(f"Ataque Sombrio causou {dano} de dano.")
    elif habilidade_id == "bomba_fumaca":
        aplicar_efeito("buff_esquiva", jogador)
        print("A fumaca cobre o campo e sua esquiva aumentou.")
    elif habilidade_id == "golpe_sagrado":
        dano = max(1, int((jogador["atk"] * 1.4) - (inimigo["def"] / 2)))
        cura = 18 + atributo_total(campeao, "inteligencia")
        inimigo["hp"] -= dano
        jogador["hp"] = min(vida_maxima(campeao), jogador["hp"] + cura)
        print(f"Golpe Sagrado causou {dano} e curou {cura}.")
    elif habilidade_id == "aura_protetora":
        jogador["efeitos"]["buff_defesa"] = 3
        print("Uma aura sagrada envolve seu corpo.")
    elif habilidade_id == "maldicao":
        aplicar_efeito("debuff_defesa", inimigo)
        dano = max(1, int((jogador["atk"] * 1.1) - (inimigo["def"] / 3)))
        inimigo["hp"] -= dano
        print(f"Maldicao enfraqueceu o alvo e causou {dano}.")
    elif habilidade_id == "dreno_vital":
        dano = max(1, int((jogador["atk"] * 1.3) - (inimigo["def"] / 3)))
        cura = max(8, dano // 2)
        inimigo["hp"] -= dano
        jogador["hp"] = min(vida_maxima(campeao), jogador["hp"] + cura)
        print(f"Dreno Vital causou {dano} e restaurou {cura} de vida.")
    elif habilidade_id == "familiar_arcano":
        jogador["efeitos"]["buff_atk"] = 3
        campeao["estado"]["mana_atual"] = min(mana_maxima(campeao), campeao["estado"]["mana_atual"] + 8)
        print("Um familiar arcano reforcou seu poder.")
    elif habilidade_id == "ruptura_astral":
        dano = max(1, int((jogador["atk"] + atributo_total(campeao, "inteligencia") * 1.5) - (inimigo["def"] / 3)))
        inimigo["hp"] -= dano
        print(f"Ruptura Astral explodiu em {dano} de dano.")

    return True


def habilidade_inimiga(inimigo, jogador):
    habilidade = inimigo.get("habilidade")

    if habilidade == "ataque_duplo":
        print(f"{inimigo['nome']} entra em frenesi e ataca duas vezes!")
        return "ataque_duplo"

    if habilidade == "regeneracao":
        inimigo["hp"] = min(inimigo["vida"], inimigo["hp"] + 12)
        print(f"{inimigo['nome']} regenerou 12 de vida.")
        return "regenerou"

    if habilidade == "veneno_turno":
        aplicar_efeito("veneno", jogador)
        print(f"{inimigo['nome']} aplicou veneno continuo.")
        return "veneno"

    if habilidade == "bola_fogo":
        print(f"{inimigo['nome']} conjurou uma bola de fogo.")
        return "bola_fogo"

    if habilidade == "resistencia":
        inimigo["defendendo"] = True
        print(f"{inimigo['nome']} reforcou sua defesa.")
        return "resistencia"

    if habilidade == "roubo":
        return "roubo"

    if habilidade == "dividir":
        if random.randint(1, 100) <= 20:
            inimigo["hp"] = min(inimigo["vida"], inimigo["hp"] + 15)
            print(f"{inimigo['nome']} se dividiu e recuperou 15 de vida.")
            return "dividir"
        return "falhou_dividir"

    if habilidade == "fase_final":
        return "fase_final"

    return None


def tratar_habilidade_passiva_inimigo(inimigo, jogador):
    if inimigo.get("nome") in ("Rei Demonio", "Senhor das Sombras") and inimigo["hp"] <= inimigo["vida"] // 2 and not inimigo.get("fase_2"):
        inimigo["fase_2"] = True
        inimigo["atk"] += 6
        inimigo["crit"] += 15
        jogador["efeitos"]["debuff_defesa"] = 3
        print(f"{inimigo['nome']} entrou na fase 2! O dano dele aumentou e sua defesa foi reduzida.")

    if inimigo.get("habilidade") == "reviver" and inimigo["hp"] <= 0 and not inimigo["reviveu"]:
        if random.randint(1, 100) <= 35:
            inimigo["reviveu"] = True
            inimigo["hp"] = 20
            print(f"{inimigo['nome']} se reergueu das sombras!")


def receber_recompensas(campeao, inimigo, area, foi_boss):
    campeao["xp"] += inimigo["xp"]
    campeao["ouro"] += inimigo["ouro"]
    campeao["estado"]["missoes"]["eliminacoes"] += 1

    if area["nome"] == "Caverna Escura" and random.randint(1, 100) <= 45:
        campeao["inventario"].append("Pocao pequena")
        print("Voce encontrou uma Pocao pequena na caverna.")

    if random.randint(1, 100) <= 20:
        campeao["inventario"].append("Pocao media")
        print("Voce encontrou uma Pocao media.")

    material = None
    if foi_boss:
        material = "Essencia Sombria" if area["nome"] == "Castelo do Rei Demonio" else "Cristal"
    else:
        rolagem = random.randint(1, 100)
        if rolagem <= 35:
            material = "Ferro"
        elif rolagem <= 50:
            material = "Aco"
        elif area["nome"] in ("Caverna Escura", "Deserto Esquecido") and rolagem <= 60:
            material = "Cristal"

    if material is not None:
        campeao["estado"]["materiais"][material] += 1
        print(f"Voce obteve material: {material}.")

    print(f"Recompensas: +{inimigo['xp']} XP e +{inimigo['ouro']} ouro.")

    if foi_boss:
        campeao["pontos_atributo"] += 10
        if area["nome"] not in campeao["estado"]["bosses_derrotados"]:
            campeao["estado"]["bosses_derrotados"].append(area["nome"])
        liberar_proxima_area(campeao, area["nome"])
        print("Boss derrotado! Voce ganhou +10 pontos de atributo.")

    verificar_subida_nivel(campeao)
    verificar_missao(campeao)
    salvar_personagem(campeao)


def verificar_missao(campeao):
    missao = campeao["estado"]["missoes"]
    if missao["eliminacoes"] >= missao["meta"]:
        campeao["ouro"] += missao["recompensa_ouro"]
        campeao["inventario"].append(missao["recompensa_item"])
        print(
            f"Missao do Cacador concluida! +{missao['recompensa_ouro']} ouro e {missao['recompensa_item']}."
        )
        missao["eliminacoes"] = 0
        missao["meta"] += 2
        missao["recompensa_ouro"] += 20


def aplicar_pacto_sombrio(campeao, oferta):
    efeitos = oferta["efeitos"]
    pacto = campeao["estado"]["pacto_sombrio"]

    campeao["atk"] += efeitos.get("atk", 0)
    campeao["def"] += efeitos.get("def", 0)
    campeao["vida"] += efeitos.get("vida", 0)
    campeao["mana"] += efeitos.get("mana", 0)
    campeao["esq"] += efeitos.get("esq", 0)

    if "vida_percentual" in efeitos:
        campeao["vida"] = max(20, int(campeao["vida"] * (1 + efeitos["vida_percentual"])))
    if "def_percentual" in efeitos:
        campeao["def"] = max(0, int(campeao["def"] * (1 + efeitos["def_percentual"])))

    campeao["estado"]["hp_atual"] = min(campeao["estado"]["hp_atual"], vida_maxima(campeao))
    campeao["estado"]["mana_atual"] = min(campeao["estado"]["mana_atual"], mana_maxima(campeao))
    campeao["estado"]["corrupcao"] += oferta["corrupcao"]

    if efeitos.get("sangramento"):
        campeao["estado"]["efeitos"]["sangramento"] = efeitos["sangramento"]
    if efeitos.get("bloqueio_cura"):
        pacto["bloqueio_cura_turnos"] = efeitos["bloqueio_cura"]
    if efeitos.get("npc_medo"):
        pacto["efeito_escondido"] = True
    if "dano_percentual" in efeitos:
        pacto["bencoes"].append({"nome": oferta["nome"], "dano_percentual": efeitos["dano_percentual"]})
    else:
        pacto["bencoes"].append({"nome": oferta["nome"]})

    salvar_personagem(campeao)


def encontro_pacto_sombrio(campeao):
    pacto = campeao["estado"]["pacto_sombrio"]
    encontro = pacto["encontros"] + 1
    if encontro not in PACTO_SOMBRIO:
        return

    print('\n[ Kael, o Marcado ]')
    print('"...voce sobreviveu."')
    print('"Poucos conseguem isso aqui."')
    if encontro == 1:
        print('"Existe uma coisa nesse lugar... um tipo de pacto."')
        print('"Ele te da poder. Mas tira algo de voce."')
        print('"Eu ja aceitei esse poder. E paguei o preco."')
        print('"Se for tentar... faca sabendo disso: nao existe volta."')

    opcoes = random.sample(PACTO_SOMBRIO[encontro], 3)
    print('\nO ar fica pesado...')
    print("Uma presenca envolve sua mente.")
    for indice, oferta in enumerate(opcoes, start=1):
        print(f"{indice} - {oferta['nome']} [{oferta['raridade']}] -> {oferta['descricao']}")
    print("4 - Recusar")

    escolha = _ler_escolha_valida({"1", "2", "3", "4"})
    if escolha == "4":
        print("Voce resistiu ao pacto desta vez.")
        pacto["encontros"] += 1
        salvar_personagem(campeao)
        return

    oferta = opcoes[int(escolha) - 1]
    print(f'Voce aceitou: {oferta["nome"]}.')
    aplicar_pacto_sombrio(campeao, oferta)
    pacto["encontros"] += 1
    salvar_personagem(campeao)


def liberar_proxima_area(campeao, area_nome):
    if area_nome not in ORDEM_PROGRESSAO:
        return

    indice = ORDEM_PROGRESSAO.index(area_nome)
    if indice + 1 < len(ORDEM_PROGRESSAO):
        proxima_area = ORDEM_PROGRESSAO[indice + 1]
        if proxima_area not in campeao["estado"]["areas_liberadas"]:
            campeao["estado"]["areas_liberadas"].append(proxima_area)
            print(f"Nova area liberada: {proxima_area}.")


def determinar_tipo_final(campeao):
    moral = campeao["estado"]["moral"]
    corrupcao = campeao["estado"]["corrupcao"]

    if corrupcao >= 8 and moral <= 2:
        return "vilao"
    if moral >= 8 and corrupcao <= 3:
        return "heroi"
    return "equilibrio"


def exibir_final(campeao, tipo_final):
    print("\n===== FIM DA CAMPANHA =====")
    if tipo_final == "heroi":
        print("Voce recusou o pior da corrupcao.")
        print("Ainda havia luz em voce.")
        print("FINAL HEROI: voce salvou o mundo sem se render ao poder sombrio.")
    elif tipo_final == "vilao":
        print("Voce aceitou o poder ate o fim.")
        print("O mundo venceu a guerra, mas perdeu a si mesmo.")
        print("FINAL VILAO: voce se tornou aquilo que jurou destruir.")
    elif tipo_final == "equilibrio":
        print("Voce nao foi puro, mas tambem nao se perdeu por completo.")
        print("Agora carrega o peso de sustentar o equilibrio.")
        print("FINAL EQUILIBRIO: o mundo sobreviveu, mas depende de voce.")
    elif tipo_final == "morte":
        print("Voce caiu no ultimo confronto.")
        print("Ninguem veio no seu lugar.")
        print("FINAL MORTE: a campanha terminou em derrota.")


def encerrar_campanha(campeao, tipo_final):
    campeao["estado"]["campanha_concluida"] = True
    campeao["estado"]["tipo_final"] = tipo_final
    salvar_personagem(campeao)
    exibir_final(campeao, tipo_final)


def restaurar_pos_combate(campeao, jogador):
    campeao["estado"]["hp_atual"] = max(0, min(jogador["hp"], vida_maxima(campeao)))
    campeao["estado"]["efeitos"] = jogador["efeitos"]


def combate(campeao, area, dados_inimigo, foi_boss=False):
    inimigo = criar_inimigo(dados_inimigo)
    jogador = criar_combatente_jogador(campeao)
    aplicar_modificadores_narrativos(campeao, area, jogador, inimigo, foi_boss)
    campeao["estado"]["combate"]["pocoes_usadas"] = 0
    campeao["estado"]["combate"]["cooldown_pocao"] = 0
    campeao["estado"]["combate"]["cooldowns"] = {}

    print(f"\n===== COMBATE: {campeao['nome']} vs {inimigo['nome']} =====")

    while jogador["hp"] > 0 and inimigo["hp"] > 0:
        reduzir_cooldowns(campeao)
        if campeao["estado"]["combate"]["cooldown_pocao"] > 0:
            campeao["estado"]["combate"]["cooldown_pocao"] -= 1
        if campeao["estado"]["pacto_sombrio"]["bloqueio_cura_turnos"] > 0:
            campeao["estado"]["pacto_sombrio"]["bloqueio_cura_turnos"] -= 1
        jogador["defendendo"] = False
        inimigo["defendendo"] = False

        aplicar_mecanica_area(area, jogador, campeao["nome"])
        if jogador["hp"] <= 0:
            break

        if aplicar_efeitos_no_inicio(jogador, campeao["nome"]):
            acao_jogador = "stun"
        else:
            print(f"\nSua vida: {jogador['hp']}/{vida_maxima(campeao)} | Vida inimiga: {inimigo['hp']}/{inimigo['vida']}")
            print("1 - Atacar")
            print("2 - Defender")
            print("3 - Usar item")
            print("4 - Fugir")
            print("5 - Habilidade")
            escolha = input("Escolha: ")

            if escolha == "1":
                ataque(jogador, inimigo, area)
                acao_jogador = "atacar"
            elif escolha == "2":
                jogador["defendendo"] = True
                print("Voce se preparou para reduzir o dano recebido.")
                acao_jogador = "defender"
            elif escolha == "3":
                if tentar_usar_item(campeao):
                    jogador["hp"] = campeao["estado"]["hp_atual"]
                acao_jogador = "item"
            elif escolha == "4":
                if random.randint(1, 100) <= 50:
                    print("Voce fugiu com sucesso.")
                    restaurar_pos_combate(campeao, jogador)
                    salvar_personagem(campeao)
                    return "fuga"
                print("Falha ao fugir.")
                acao_jogador = "falha_fuga"
            elif escolha == "5":
                if usar_habilidade(campeao, jogador, inimigo, area):
                    acao_jogador = "habilidade"
                else:
                    acao_jogador = "erro"
            else:
                print("Opcao invalida! Voce perdeu o turno.")
                acao_jogador = "erro"

        tratar_habilidade_passiva_inimigo(inimigo, jogador)
        if inimigo["hp"] <= 0:
            break

        aplicar_mecanica_area(area, inimigo, inimigo["nome"])
        if inimigo["hp"] <= 0:
            break

        turno_perdido_inimigo = aplicar_efeitos_no_inicio(inimigo, inimigo["nome"])
        tratar_habilidade_passiva_inimigo(inimigo, jogador)
        if inimigo["hp"] <= 0:
            break

        if turno_perdido_inimigo:
            continue

        acao_inimigo = escolher_acao_inimigo(inimigo)
        if acao_inimigo == "defender":
            inimigo["defendendo"] = True
            print(f"{inimigo['nome']} assumiu uma postura defensiva.")
        elif acao_inimigo == "habilidade":
            resultado = habilidade_inimiga(inimigo, jogador)
            if resultado == "ataque_duplo":
                ataque(inimigo, jogador, area, inimigo.get("efeito"))
                if jogador["hp"] > 0:
                    ataque(inimigo, jogador, area, inimigo.get("efeito"))
            elif resultado == "bola_fogo":
                dano = max(1, int(inimigo["atk"] - (jogador["def"] / 4)))
                jogador["hp"] -= dano
                print(f"{inimigo['nome']} causou {dano} de dano magico em {jogador['nome']}.")
            elif resultado == "roubo":
                ouro_roubado = min(12, campeao["ouro"])
                campeao["ouro"] -= ouro_roubado
                print(f"{inimigo['nome']} roubou {ouro_roubado} ouro.")
            elif resultado in ("resistencia", "dividir", "falhou_dividir"):
                pass
            elif resultado == "fase_final":
                ataque(inimigo, jogador, area, inimigo.get("efeito"))
            elif resultado not in ("regenerou", "veneno"):
                ataque(inimigo, jogador, area, inimigo.get("efeito"))
        else:
            ataque(inimigo, jogador, area, inimigo.get("efeito"))

        if acao_jogador == "defender":
            jogador["defendendo"] = False

    restaurar_pos_combate(campeao, jogador)
    campeao["estado"]["combate"]["pocoes_usadas"] = 0
    campeao["estado"]["combate"]["cooldown_pocao"] = 0
    campeao["estado"]["combate"]["cooldowns"] = {}

    if jogador["hp"] <= 0:
        campeao["estado"]["local_atual"] = "Vila Inicial"
        campeao["estado"]["hp_atual"] = max(1, vida_maxima(campeao) // 2)
        campeao["estado"]["efeitos"] = {}
        print("Voce foi derrotado e retornou para a Vila Inicial.")
        salvar_personagem(campeao)
        return "derrota"

    receber_recompensas(campeao, inimigo, area, foi_boss)
    registrar_maestria(campeao)
    return "vitoria"


def explorar_area(campeao, area):
    campeao["estado"]["local_atual"] = area["nome"]
    evento = random.choice(["ouro", "item", "emboscada", "npc", "armadilha", "nada", "combate"])

    print(f"\n===== EXPLORANDO {area['nome'].upper()} =====")
    print(area["descricao"])
    print(f"Mecanica da area: {area['mecanica']}")

    if evento == "ouro":
        ganho = random.randint(10, 35)
        campeao["ouro"] += ganho
        print(f"Voce encontrou {ganho} ouro pelo caminho.")
    elif evento == "item":
        item = random.choice(["Pocao pequena", "Pocao media", "Pocao de mana"])
        campeao["inventario"].append(item)
        print(f"Voce encontrou o item {item}.")
    elif evento == "npc":
        print("Um viajante apareceu e contou uma dica: bosses costumam punir quem chega sem pocoes.")
    elif evento == "armadilha":
        dano = random.randint(6, 15)
        campeao["estado"]["hp_atual"] = max(1, campeao["estado"]["hp_atual"] - dano)
        print(f"Voce caiu em uma armadilha e perdeu {dano} de vida.")
    elif evento == "emboscada":
        print("Voce sofreu uma emboscada!")
        inimigo = random.choice(area["inimigos"])
        combate(campeao, area, inimigo)
    elif evento == "combate":
        inimigo = random.choice(area["inimigos"])
        combate(campeao, area, inimigo)
    else:
        print("Nada aconteceu desta vez.")

    salvar_personagem(campeao)


def enfrentar_boss_area(campeao, area):
    if area["boss"] is None:
        print("Essa area nao possui boss principal.")
        return

    if area["nome"] in campeao["estado"]["bosses_derrotados"]:
        print("Boss dessa area ja foi derrotado.")
        return

    resultado = combate(campeao, area, area["boss"], foi_boss=True)
    if resultado == "vitoria" and area["nome"] == "Floresta Sombria":
        evento_pos_boss_floresta(campeao)
    if resultado == "vitoria" and area["nome"] == "Caverna Escura":
        historia = campeao["estado"]["historia"]
        if not historia["boss_caverna_dialogo"]:
            print('\n"Esse poder... esta crescendo."')
            historia["boss_caverna_dialogo"] = True
            salvar_personagem(campeao)
    if area["nome"] == "Castelo do Rei Demonio":
        if resultado == "vitoria":
            encerrar_campanha(campeao, determinar_tipo_final(campeao))
        elif resultado == "derrota":
            encerrar_campanha(campeao, "morte")


def menu_mapa(campeao):
    if campeao["estado"].get("campanha_concluida"):
        print("Essa campanha ja foi concluida.")
        exibir_final(campeao, campeao["estado"].get("tipo_final"))
        return

    while True:
        areas_disponiveis = [buscar_area(nome) for nome in campeao["estado"]["areas_liberadas"]]

        print("\n===== MAPA =====")
        for indice, area in enumerate(areas_disponiveis, start=1):
            print(f"{indice} - {area['nome']} | Dificuldade: {area['dificuldade']}")
        print(f"{len(areas_disponiveis) + 1} - Voltar")

        escolha = input("Escolha uma area: ")
        if not escolha.isdigit():
            print("Opcao invalida!")
            continue

        escolha_numero = int(escolha)
        if escolha_numero == len(areas_disponiveis) + 1:
            break

        if not 1 <= escolha_numero <= len(areas_disponiveis):
            print("Opcao invalida!")
            continue

        area = areas_disponiveis[escolha_numero - 1]

        if area["tipo"] == "hub":
            menu_vila(campeao)
            continue

        if area["nome"] == "Floresta Sombria":
            evento_floresta_mercenario(campeao)
            evento_altar_floresta(campeao)
        elif area["nome"] == "Campos Abertos":
            evento_campos_abertos(campeao)
            evento_mercenario_campos(campeao)
        elif area["nome"] == "Caverna Escura":
            evento_caverna_escura(campeao)
            evento_npc_preso_caverna(campeao)

        while True:
            print(f"""
===== {area["nome"].upper()} =====
1 - Explorar
2 - Enfrentar boss
3 - Voltar
""")
            acao = input("Escolha: ")

            if acao == "1":
                explorar_area(campeao, area)
            elif acao == "2":
                enfrentar_boss_area(campeao, area)
            elif acao == "3":
                break
            else:
                print("Opcao invalida!")


def npc_sabio(campeao):
    proxima = None
    for area in ORDEM_PROGRESSAO:
        if area not in campeao["estado"]["bosses_derrotados"]:
            proxima = area
            break

    print("\nSabio: prepare pocoes antes dos bosses e invista em defesa se estiver sofrendo muito dano.")
    if proxima is not None:
        print(f"Sabio: seu proximo grande desafio esta em {proxima}.")


def npc_viajante(campeao):
    evento = random.choice(["troca", "aposta", "raro"])

    if evento == "troca":
        if "Pocao pequena" in campeao["inventario"]:
            campeao["inventario"].remove("Pocao pequena")
            campeao["inventario"].append("Pocao media")
            print("Viajante trocou sua Pocao pequena por uma Pocao media.")
        else:
            print("Viajante queria trocar, mas voce nao tinha o item pedido.")
    elif evento == "aposta":
        if campeao["ouro"] >= 15 and random.randint(1, 100) <= 50:
            campeao["ouro"] += 20
            print("Voce venceu a aposta e ganhou 20 ouro.")
        elif campeao["ouro"] >= 15:
            campeao["ouro"] -= 15
            print("Voce perdeu a aposta e 15 ouro.")
        else:
            print("Voce nao tem ouro suficiente para apostar.")
    else:
        campeao["inventario"].append("Pocao forte")
        print("Evento raro! O viajante lhe deu uma Pocao forte.")

    salvar_personagem(campeao)


def npc_cacador(campeao):
    missao = campeao["estado"]["missoes"]
    restante = max(0, missao["meta"] - missao["eliminacoes"])
    print("\nCacador de Recompensas:")
    print(f"Elimine mais {restante} inimigos para receber {missao['recompensa_ouro']} ouro e {missao['recompensa_item']}.")


def loja(campeao):
    while True:
        print(f"\n===== LOJA =====\nSeu ouro: {campeao['ouro']}")
        print("1 - Pocao pequena (30 ouro)")
        print("2 - Pocao media (60 ouro)")
        print("3 - Pocao de mana (45 ouro)")
        print("4 - Pocao forte (90 ouro)")
        print("5 - Equipamentos")
        print("6 - Voltar")
        escolha = input("Escolha: ")

        if escolha == "1":
            item = "Pocao pequena"
        elif escolha == "2":
            item = "Pocao media"
        elif escolha == "3":
            item = "Pocao de mana"
        elif escolha == "4":
            item = "Pocao forte"
        elif escolha == "5":
            itens_loja = [
                "Espada Curta", "Espada Longa", "Machado de Guerra", "Arco Composto",
                "Cajado Arcano", "Armadura Leve", "Armadura Media", "Armadura Pesada",
                "Amuleto do Vigor", "Anel do Foco",
            ]
            for indice, nome in enumerate(itens_loja, start=1):
                dados = ITENS_LOJA[nome]
                print(f"{indice} - {nome} ({dados['valor']} ouro)")
            print(f"{len(itens_loja)+1} - Voltar")
            escolha_item = _ler_escolha_valida({str(i) for i in range(1, len(itens_loja)+2)})
            if escolha_item == str(len(itens_loja)+1):
                continue
            item = itens_loja[int(escolha_item) - 1]
        elif escolha == "6":
            break
        else:
            print("Opcao invalida!")
            continue

        valor = ITENS_LOJA[item]["valor"]
        if campeao["ouro"] < valor:
            print("Ouro insuficiente.")
            continue

        campeao["ouro"] -= valor
        campeao["inventario"].append(item)
        print(f"Voce comprou {item}.")
        salvar_personagem(campeao)


def curandeiro(campeao):
    custo = 25
    print(f"\nCurandeiro: cura total por {custo} ouro.")
    escolha = input("Deseja curar? (s/n): ").strip().lower()

    if escolha != "s":
        return

    if campeao["ouro"] < custo:
        print("Ouro insuficiente.")
        return

    campeao["ouro"] -= custo
    campeao["estado"]["hp_atual"] = vida_maxima(campeao)
    campeao["estado"]["mana_atual"] = campeao["mana"]
    campeao["estado"]["efeitos"] = {}
    print("Sua vida e mana foram restauradas.")
    salvar_personagem(campeao)


def ferreiro(campeao):
    while True:
        print(f"""
===== FERREIRO =====
Seu ouro: {campeao["ouro"]}
1 - Melhorar arma equipada
2 - Melhorar armadura equipada
3 - Voltar
""")
        escolha = input("Escolha: ")

        if escolha == "1":
            arma = campeao["estado"]["equipamentos"].get("arma")
            if arma is None:
                print("Nenhuma arma equipada.")
                continue
            melhoria = MELHORIAS_FERREIRO.get(arma["nome"], [])
            nivel_atual = arma.get("upgrade", 0)
            proxima = next((m for m in melhoria if m["nivel"] == nivel_atual + 1), None)
            if proxima is None:
                print("Essa arma nao possui mais upgrades.")
                continue
            if campeao["ouro"] < proxima["ouro"]:
                print("Ouro insuficiente.")
                continue
            faltando = [mat for mat, qtd in proxima["materiais"].items() if campeao["estado"]["materiais"].get(mat, 0) < qtd]
            if faltando:
                print(f"Materiais insuficientes: {', '.join(faltando)}.")
                continue
            campeao["ouro"] -= proxima["ouro"]
            for material, qtd in proxima["materiais"].items():
                campeao["estado"]["materiais"][material] -= qtd
            arma["upgrade"] = proxima["nivel"]
            campeao["estado"]["maestria"].setdefault(arma["nome"], {"uso": 0, "upgrade": 0})["upgrade"] = proxima["atk_extra"]
            print("Sua arma foi melhorada.")
        elif escolha == "2":
            armadura = campeao["estado"]["equipamentos"].get("armadura")
            if armadura is None:
                print("Nenhuma armadura equipada.")
                continue
            if campeao["ouro"] < 90 or campeao["estado"]["materiais"]["Ferro"] < 2:
                print("Voce precisa de 90 ouro e 2 Ferro para reforcar a armadura.")
                continue
            campeao["ouro"] -= 90
            campeao["estado"]["materiais"]["Ferro"] -= 2
            campeao["estado"]["armadura_bonus"] += 2
            print("Sua armadura foi melhorada.")
        elif escolha == "3":
            break
        else:
            print("Opcao invalida!")
            continue

        salvar_personagem(campeao)


def menu_vila(campeao):
    campeao["estado"]["local_atual"] = "Vila Inicial"
    evento_vila_inicial(campeao)

    while True:
        print(f"""
===== VILA INICIAL =====
1 - Loja
2 - Curandeiro
3 - Ferreiro
4 - Sabio
5 - Viajante
6 - Cacador de Recompensas
7 - Voltar
""")
        escolha = input("Escolha: ")

        if escolha == "1":
            loja(campeao)
        elif escolha == "2":
            curandeiro(campeao)
        elif escolha == "3":
            ferreiro(campeao)
        elif escolha == "4":
            npc_sabio(campeao)
        elif escolha == "5":
            npc_viajante(campeao)
        elif escolha == "6":
            npc_cacador(campeao)
        elif escolha == "7":
            break
        else:
            print("Opcao invalida!")


def criar_personagem():
    classes = {
        "1": {"classe": "Tank", "vida": 125, "atk": 10, "def": 8, "crit": 5, "esq": 4, "mana": 35},
        "2": {"classe": "Mago", "vida": 85, "atk": 14, "def": 4, "crit": 10, "esq": 8, "mana": 80},
        "3": {"classe": "Guerreiro", "vida": 110, "atk": 12, "def": 6, "crit": 9, "esq": 6, "mana": 45},
        "4": {"classe": "Arqueiro", "vida": 95, "atk": 11, "def": 5, "crit": 16, "esq": 12, "mana": 50},
        "5": {"classe": "Assassino", "vida": 90, "atk": 12, "def": 4, "crit": 20, "esq": 16, "mana": 45},
        "6": {"classe": "Paladino", "vida": 120, "atk": 11, "def": 7, "crit": 8, "esq": 5, "mana": 60},
        "7": {"classe": "Bruxo", "vida": 92, "atk": 13, "def": 4, "crit": 12, "esq": 8, "mana": 75},
        "8": {"classe": "Invocador", "vida": 100, "atk": 10, "def": 5, "crit": 10, "esq": 8, "mana": 85},
    }

    nome = input("Digite o nome do personagem: ").strip()
    if not nome:
        print("Nome invalido!")
        return None

    while True:
        print("""
!!!! ESCOLHA SUA CLASSE !!!!
1 - Tank        | Vida:125 | Atk:10 | Def:8  | Crit:5  | Esq:4  | Mana:35
2 - Mago        | Vida:85  | Atk:14 | Def:4  | Crit:10 | Esq:8  | Mana:80
3 - Guerreiro   | Vida:110 | Atk:12 | Def:6  | Crit:9  | Esq:6  | Mana:45
4 - Arqueiro    | Vida:95  | Atk:11 | Def:5  | Crit:16 | Esq:12 | Mana:50
5 - Assassino   | Vida:90  | Atk:12 | Def:4  | Crit:20 | Esq:16 | Mana:45
6 - Paladino    | Vida:120 | Atk:11 | Def:7  | Crit:8  | Esq:5  | Mana:60
7 - Bruxo       | Vida:92  | Atk:13 | Def:4  | Crit:12 | Esq:8  | Mana:75
8 - Invocador   | Vida:100 | Atk:10 | Def:5  | Crit:10 | Esq:8  | Mana:85
9 - Sair
""")
        escolha = input("Escolha: ")

        if escolha == "9":
            print("Saindo da criacao de personagem...")
            return None

        if escolha in classes:
            campeao = {
                "nome": nome,
                "nivel": 1,
                "xp": 0,
                "ouro": 80,
                "pontos_atributo": 0,
                "inventario": ["Pocao pequena", "Pocao pequena", "Pocao de mana"],
            }
            campeao.update(classes[escolha])
            campeao["estado"] = criar_estado_inicial(campeao["vida"], campeao["mana"])
            if escolha == "1":
                campeao["estado"]["atributos"] = {"forca": 12, "agilidade": 6, "inteligencia": 5}
            elif escolha == "2":
                campeao["estado"]["atributos"] = {"forca": 4, "agilidade": 7, "inteligencia": 12}
            elif escolha == "3":
                campeao["estado"]["atributos"] = {"forca": 10, "agilidade": 7, "inteligencia": 6}
            elif escolha == "4":
                campeao["estado"]["atributos"] = {"forca": 6, "agilidade": 12, "inteligencia": 6}
            elif escolha == "5":
                campeao["estado"]["atributos"] = {"forca": 6, "agilidade": 13, "inteligencia": 5}
            elif escolha == "6":
                campeao["estado"]["atributos"] = {"forca": 10, "agilidade": 6, "inteligencia": 8}
            elif escolha == "7":
                campeao["estado"]["atributos"] = {"forca": 5, "agilidade": 7, "inteligencia": 11}
            elif escolha == "8":
                campeao["estado"]["atributos"] = {"forca": 5, "agilidade": 6, "inteligencia": 12}
            tocar_prologo(campeao)
            salvar_personagem(campeao)
            print(f'\nPersonagem "{campeao["nome"]}" criado e salvo com sucesso!')
            return campeao

        print("Opcao invalida! Tente novamente.")


def menu_jogador(campeao):
    while True:
        print(f"""
===== MENU DO JOGADOR =====
Jogador: {campeao["nome"]} | Classe: {campeao["classe"]} | Vida: {campeao["estado"]["hp_atual"]}/{vida_maxima(campeao)}
1 - Ver status
2 - Inventario
3 - Equipamentos
4 - Vila Inicial
5 - Mapa
6 - Distribuir pontos
7 - Voltar
""")
        escolha = input("Escolha: ")

        if escolha == "1":
            mostrar_status(campeao)
        elif escolha == "2":
            mostrar_inventario(campeao)
        elif escolha == "3":
            gerenciar_equipamentos(campeao)
        elif escolha == "4":
            menu_vila(campeao)
        elif escolha == "5":
            menu_mapa(campeao)
        elif escolha == "6":
            if campeao["pontos_atributo"] > 0:
                distribuir_pontos(campeao)
            else:
                print("\nVoce nao tem pontos para distribuir.")
        elif escolha == "7":
            salvar_personagem(campeao)
            break
        else:
            print("Opcao invalida!")
