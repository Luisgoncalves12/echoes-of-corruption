import json
import sqlite3


DB_PATH = "rpg.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def _garantir_coluna(cursor, nome_coluna, definicao):
    cursor.execute("PRAGMA table_info(personagens)")
    colunas = [linha[1] for linha in cursor.fetchall()]

    if nome_coluna not in colunas:
        cursor.execute(f"ALTER TABLE personagens ADD COLUMN {nome_coluna} {definicao}")


def inicializar_banco():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS personagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                classe TEXT NOT NULL,
                nivel INTEGER NOT NULL,
                xp INTEGER NOT NULL,
                ouro INTEGER NOT NULL,
                pontos_atributo INTEGER NOT NULL,
                vida INTEGER NOT NULL,
                atk INTEGER NOT NULL,
                def INTEGER NOT NULL,
                crit INTEGER NOT NULL,
                esq INTEGER NOT NULL,
                mana INTEGER NOT NULL,
                inventario TEXT NOT NULL
            )
            """
        )
        _garantir_coluna(cursor, "estado", "TEXT NOT NULL DEFAULT '{}'")
        conn.commit()


def salvar_personagem(campeao):
    inventario_json = json.dumps(campeao["inventario"], ensure_ascii=True)
    estado_json = json.dumps(campeao["estado"], ensure_ascii=True)

    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO personagens (
                nome, classe, nivel, xp, ouro, pontos_atributo,
                vida, atk, def, crit, esq, mana, inventario, estado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(nome) DO UPDATE SET
                classe = excluded.classe,
                nivel = excluded.nivel,
                xp = excluded.xp,
                ouro = excluded.ouro,
                pontos_atributo = excluded.pontos_atributo,
                vida = excluded.vida,
                atk = excluded.atk,
                def = excluded.def,
                crit = excluded.crit,
                esq = excluded.esq,
                mana = excluded.mana,
                inventario = excluded.inventario,
                estado = excluded.estado
            """,
            (
                campeao["nome"],
                campeao["classe"],
                campeao["nivel"],
                campeao["xp"],
                campeao["ouro"],
                campeao["pontos_atributo"],
                campeao["vida"],
                campeao["atk"],
                campeao["def"],
                campeao["crit"],
                campeao["esq"],
                campeao["mana"],
                inventario_json,
                estado_json,
            ),
        )
        conn.commit()


def listar_personagens():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT nome, classe, nivel, xp, ouro
            FROM personagens
            ORDER BY id
            """
        )
        return cursor.fetchall()


def _estado_padrao():
    return {
        "hp_atual": None,
        "mana_atual": None,
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


def carregar_personagem(nome):
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personagens WHERE nome = ?", (nome,))
        linha = cursor.fetchone()

    if linha is None:
        return None

    campeao = dict(linha)
    campeao["inventario"] = json.loads(campeao["inventario"])

    estado_salvo = {}
    if campeao.get("estado"):
        estado_salvo = json.loads(campeao["estado"])

    estado = _estado_padrao()
    for chave, valor in estado_salvo.items():
        if isinstance(estado.get(chave), dict) and isinstance(valor, dict):
            estado[chave].update(valor)
        else:
            estado[chave] = valor

    if estado["hp_atual"] is None:
        estado["hp_atual"] = campeao["vida"]

    if estado["mana_atual"] is None:
        estado["mana_atual"] = campeao["mana"]

    campeao["estado"] = estado
    return campeao
