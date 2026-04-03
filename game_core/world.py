AREAS = [
    {
        "nome": "Vila Inicial",
        "tipo": "hub",
        "dificuldade": 0,
        "descricao": "Hub seguro com servicos e NPCs.",
        "mecanica": "Sem combate.",
        "inimigos": [],
        "boss": {"nome": "Capitao Bandido", "vida": 165, "atk": 16, "def": 8, "crit": 18, "esq": 10, "ia": "agressivo", "efeito": "sangramento", "habilidade": "roubo", "xp": 240, "ouro": 130},
    },
    {
        "nome": "Floresta Sombria",
        "tipo": "combate",
        "dificuldade": 1,
        "descricao": "Uma floresta fechada onde criaturas atacam entre as sombras.",
        "mecanica": "Maior esquiva para todos em combate.",
        "inimigos": [
            {"nome": "Lobo Selvagem", "vida": 60, "atk": 8, "def": 2, "crit": 8, "esq": 16, "ia": "agressivo", "efeito": None, "habilidade": "ataque_duplo", "xp": 20, "ouro": 15},
            {"nome": "Goblin Ladrao", "vida": 50, "atk": 7, "def": 3, "crit": 8, "esq": 12, "ia": "estrategico", "efeito": None, "habilidade": "roubo", "xp": 18, "ouro": 25},
            {"nome": "Slime", "vida": 80, "atk": 5, "def": 5, "crit": 4, "esq": 5, "ia": "defensivo", "efeito": None, "habilidade": "dividir", "xp": 15, "ouro": 10},
        ],
        "boss": {"nome": "Lobo Alfa", "vida": 140, "atk": 14, "def": 5, "crit": 12, "esq": 14, "ia": "agressivo", "efeito": None, "habilidade": "ataque_duplo", "xp": 220, "ouro": 110},
    },
    {
        "nome": "Campos Abertos",
        "tipo": "combate",
        "dificuldade": 2,
        "descricao": "Planicies amplas dominadas por saqueadores e arqueiros.",
        "mecanica": "Sem mecanica especial.",
        "inimigos": [
            {"nome": "Bandido", "vida": 95, "atk": 13, "def": 6, "crit": 16, "esq": 10, "ia": "agressivo", "efeito": "sangramento", "xp": 48, "ouro": 40},
            {"nome": "Aranha Gigante", "vida": 85, "atk": 10, "def": 5, "crit": 8, "esq": 10, "ia": "estrategico", "efeito": "veneno", "habilidade": None, "xp": 45, "ouro": 28},
        ],
        "boss": {"nome": "Capitao Bandido", "vida": 165, "atk": 16, "def": 8, "crit": 18, "esq": 10, "ia": "agressivo", "efeito": "sangramento", "habilidade": "roubo", "xp": 240, "ouro": 130},
    },
    {
        "nome": "Caverna Escura",
        "tipo": "combate",
        "dificuldade": 3,
        "descricao": "Uma caverna antiga cheia de ecos, ossos e magia sombria.",
        "mecanica": "Maior chance de loot.",
        "inimigos": [
            {"nome": "Esqueleto Guerreiro", "vida": 90, "atk": 12, "def": 6, "crit": 8, "esq": 8, "ia": "defensivo", "efeito": None, "habilidade": "resistencia", "xp": 40, "ouro": 30},
            {"nome": "Mago Sombrio", "vida": 70, "atk": 15, "def": 4, "crit": 12, "esq": 10, "ia": "estrategico", "efeito": "debuff_defesa", "habilidade": "bola_fogo", "xp": 50, "ouro": 35},
        ],
        "boss": {"nome": "Troll", "vida": 180, "atk": 18, "def": 9, "crit": 10, "esq": 5, "ia": "defensivo", "efeito": None, "habilidade": "regeneracao", "xp": 260, "ouro": 140},
    },
    {
        "nome": "Deserto Esquecido",
        "tipo": "combate",
        "dificuldade": 4,
        "descricao": "Areias violentas e ruinas escondidas sob o calor extremo.",
        "mecanica": "Perde vida ao longo do tempo.",
        "inimigos": [
            {"nome": "Cavaleiro Corrompido", "vida": 140, "atk": 18, "def": 10, "crit": 10, "esq": 6, "ia": "defensivo", "efeito": None, "habilidade": "resistencia", "xp": 90, "ouro": 70},
            {"nome": "Elemental de Fogo", "vida": 110, "atk": 20, "def": 6, "crit": 12, "esq": 10, "ia": "agressivo", "efeito": "sangramento", "habilidade": "bola_fogo", "xp": 100, "ouro": 80},
        ],
        "boss": {"nome": "Rei Escorpiao", "vida": 210, "atk": 19, "def": 10, "crit": 12, "esq": 8, "ia": "estrategico", "efeito": "veneno", "habilidade": "veneno_turno", "xp": 320, "ouro": 180},
    },
    {
        "nome": "Lago Amaldicoado",
        "tipo": "combate",
        "dificuldade": 4,
        "descricao": "Uma nevoa pesada encobre criaturas que surgem da agua e da escuridao.",
        "mecanica": "Chance extra de errar ataques.",
        "inimigos": [
            {"nome": "Sombra", "vida": 80, "atk": 17, "def": 4, "crit": 20, "esq": 20, "ia": "agressivo", "efeito": None, "habilidade": None, "xp": 55, "ouro": 38},
        ],
        "boss": {"nome": "Guardiao do Lago", "vida": 210, "atk": 21, "def": 9, "crit": 20, "esq": 18, "ia": "estrategico", "efeito": "stun", "habilidade": "bola_fogo", "xp": 340, "ouro": 190},
    },
    {
        "nome": "Castelo Abandonado",
        "tipo": "combate",
        "dificuldade": 5,
        "descricao": "Salas antigas guardadas por aço enferrujado e sombras vivas.",
        "mecanica": "Sem mecanica especial.",
        "inimigos": [
            {"nome": "Guardiao Sombrio", "vida": 120, "atk": 18, "def": 10, "crit": 12, "esq": 10, "ia": "defensivo", "efeito": None, "habilidade": "resistencia", "xp": 95, "ouro": 75},
        ],
        "boss": {"nome": "Cavaleiro da Ruina", "vida": 230, "atk": 22, "def": 14, "crit": 14, "esq": 10, "ia": "defensivo", "efeito": "debuff_defesa", "habilidade": "resistencia", "xp": 360, "ouro": 210},
    },
    {
        "nome": "Montanha Vulcanica",
        "tipo": "combate",
        "dificuldade": 5,
        "descricao": "Rocha incandescente, explosoes e criaturas moldadas pelo magma.",
        "mecanica": "Sem mecanica especial.",
        "inimigos": [
            {"nome": "General Demonio", "vida": 140, "atk": 19, "def": 11, "crit": 14, "esq": 10, "ia": "estrategico", "efeito": "stun", "habilidade": None, "xp": 100, "ouro": 80},
        ],
        "boss": {"nome": "Coracao do Vulcao", "vida": 245, "atk": 24, "def": 12, "crit": 16, "esq": 8, "ia": "agressivo", "efeito": "sangramento", "habilidade": "bola_fogo", "xp": 380, "ouro": 230},
    },
    {
        "nome": "Castelo do Rei Demonio",
        "tipo": "combate",
        "dificuldade": 6,
        "descricao": "Ultima fortaleza antes do confronto final.",
        "mecanica": "Sem mecanica especial.",
        "inimigos": [],
        "boss": {"nome": "Senhor das Sombras", "vida": 250, "atk": 22, "def": 12, "crit": 15, "esq": 12, "ia": "estrategico", "efeito": None, "habilidade": "fase_final", "xp": 420, "ouro": 220},
    },
]

ITENS_LOJA = {
    "Pocao pequena": {"tipo": "cura", "valor": 30, "cura": 30},
    "Pocao media": {"tipo": "cura", "valor": 60, "cura": 60},
    "Pocao de mana": {"tipo": "mana", "valor": 45, "cura": 40},
    "Pocao forte": {"tipo": "cura", "valor": 90, "cura": 90},
    "Espada Curta": {"tipo": "arma", "valor": 90, "atk": 5, "requisito": {"forca": 5}, "categoria": "espada"},
    "Espada Longa": {"tipo": "arma", "valor": 160, "atk": 10, "requisito": {"forca": 10}, "categoria": "espada"},
    "Machado de Guerra": {"tipo": "arma", "valor": 220, "atk": 14, "requisito": {"forca": 12}, "categoria": "machado"},
    "Arco Composto": {"tipo": "arma", "valor": 170, "atk": 7, "crit": 6, "requisito": {"agilidade": 10}, "categoria": "arco"},
    "Cajado Arcano": {"tipo": "arma", "valor": 180, "atk": 8, "mana": 5, "requisito": {"inteligencia": 12}, "categoria": "cajado"},
    "Armadura Leve": {"tipo": "armadura", "valor": 120, "def": 5, "esq": 3, "requisito": {"agilidade": 8}, "categoria": "leve"},
    "Armadura Media": {"tipo": "armadura", "valor": 170, "def": 10, "requisito": {"forca": 8}, "categoria": "media"},
    "Armadura Pesada": {"tipo": "armadura", "valor": 240, "def": 15, "esq": -3, "requisito": {"forca": 12}, "categoria": "pesada"},
    "Amuleto do Vigor": {"tipo": "acessorio", "valor": 140, "vida": 20, "requisito": {}, "categoria": "amuleto"},
    "Anel do Foco": {"tipo": "acessorio", "valor": 150, "crit": 4, "mana": 10, "requisito": {}, "categoria": "anel"},
}

MELHORIAS_FERREIRO = {
    "Espada Longa": [
        {"nivel": 1, "ouro": 100, "materiais": {"Ferro": 2}, "atk_extra": 2},
        {"nivel": 2, "ouro": 200, "materiais": {"Aco": 1}, "atk_extra": 3},
    ],
    "Machado de Guerra": [
        {"nivel": 1, "ouro": 130, "materiais": {"Ferro": 2}, "atk_extra": 2},
        {"nivel": 2, "ouro": 240, "materiais": {"Aco": 1}, "atk_extra": 4},
    ],
    "Arco Composto": [
        {"nivel": 1, "ouro": 110, "materiais": {"Ferro": 1, "Cristal": 1}, "atk_extra": 2},
    ],
    "Cajado Arcano": [
        {"nivel": 1, "ouro": 120, "materiais": {"Cristal": 1}, "atk_extra": 2, "mana_extra": 5},
    ],
}

PACTO_SOMBRIO = {
    1: [
        {"nome": "Forca Instavel", "raridade": "Comum", "descricao": "+5 ATK / -5 DEF", "efeitos": {"atk": 5, "def": -5}, "corrupcao": 0},
        {"nome": "Vitalidade Roubada", "raridade": "Comum", "descricao": "+20 HP / -10 Mana", "efeitos": {"vida": 20, "mana": -10}, "corrupcao": 0},
        {"nome": "Mente Expandida", "raridade": "Comum", "descricao": "+15 Mana / -5 HP", "efeitos": {"mana": 15, "vida": -5}, "corrupcao": 0},
        {"nome": "Sangue Ardente", "raridade": "Corrompido", "descricao": "+10 ATK / sangramento inicial", "efeitos": {"atk": 10, "sangramento": 3}, "corrupcao": 1},
    ],
    2: [
        {"nome": "Reflexo Sombrio", "raridade": "Corrompido", "descricao": "+15 esquiva / -4 DEF", "efeitos": {"esq": 15, "def": -4}, "corrupcao": 1},
        {"nome": "Poder Instavel", "raridade": "Corrompido", "descricao": "+20% dano / mais chance de erro", "efeitos": {"dano_percentual": 0.2, "erro_extra": 10}, "corrupcao": 1},
        {"nome": "Pacto de Sangue", "raridade": "Profano", "descricao": "+15 ATK / -30 HP permanente", "efeitos": {"atk": 15, "vida": -30}, "corrupcao": 2},
        {"nome": "Alma Fragmentada", "raridade": "Profano", "descricao": "+30 Mana / +2 corrupcao", "efeitos": {"mana": 30}, "corrupcao": 2},
    ],
    3: [
        {"nome": "Forca Absoluta", "raridade": "Profano", "descricao": "+25 ATK / -50% DEF", "efeitos": {"atk": 25, "def_percentual": -0.5}, "corrupcao": 2},
        {"nome": "Ascensao Sombria", "raridade": "Extremo", "descricao": "+40 ATK / NPCs temem voce", "efeitos": {"atk": 40, "npc_medo": True}, "corrupcao": 3},
        {"nome": "Vida Profana", "raridade": "Extremo", "descricao": "+100 HP / sem cura por 3 turnos", "efeitos": {"vida": 100, "bloqueio_cura": 3}, "corrupcao": 2},
        {"nome": "Sacrificio Final", "raridade": "Extremo", "descricao": "+50% dano / perde 50% da vida maxima", "efeitos": {"dano_percentual": 0.5, "vida_percentual": -0.5}, "corrupcao": 3},
    ],
}

ORDEM_PROGRESSAO = [area["nome"] for area in AREAS if area["nome"] != "Vila Inicial"]


def buscar_area(nome_area):
    for area in AREAS:
        if area["nome"] == nome_area:
            return area
    return None
