# Echoes of Corruption

Um RPG de terminal sobre poder, corrupção e o custo das escolhas.

RPG de terminal feito em Python com combate por turno, progressão de personagem, escolhas morais, múltiplos finais e persistência local com SQLite.

## Visão Geral

Este projeto foi construído como um RPG jogável em terminal, com foco em:

- arquitetura modular simples e legível
- progressão de campanha do início ao fim
- sistema de combate por turno com habilidades por classe
- persistência de progresso com `SQLite`
- narrativa reativa baseada em `moral` e `corrupcao`

O jogo hoje possui campanha completa, com áreas destraváveis, bosses, sistema de equipamentos, materiais, upgrades, pacto sombrio e finais múltiplos.

## Lore

O mundo está sendo consumido por uma corrupção antiga. A `Vila Inicial` é um dos últimos refúgios seguros, cercada por áreas cada vez mais hostis e distorcidas por uma força sombria.

Tudo começa quando uma voz sem corpo chama o protagonista ainda no despertar:

> "Voce esta acordando..."
> "Mas ainda nao entende o que carrega."
> "Quando chegar a hora... voce vai precisar de mim."

Na vila, o `Sabio` percebe que algo mudou em você e revela que uma força antiga está retornando. A partir daí, a jornada deixa de ser apenas sobrevivência: ela passa a ser uma disputa entre resistir à corrupção, usar esse poder ou ser consumido por ele.

Ao longo da campanha, as decisões do jogador moldam o tom da história:

- na `Floresta Sombria`, surgem as primeiras escolhas morais
- nos `Campos Abertos`, o mundo reage ao que foi feito antes
- na `Caverna Escura`, o `Espirito Sombrio` e `Kael, o Marcado` aprofundam o conflito do poder com custo
- no castelo final, a campanha fecha com um final de `heroi`, `vilao`, `equilibrio` ou `morte`

## Features

- Criação e carregamento de personagem
- Persistência de save com `SQLite`
- Classes jogáveis com habilidades próprias
- Combate por turno com:
  - ataque
  - defesa
  - uso de item
  - fuga
  - habilidades com mana e cooldown
- Sistema de atributos:
  - forca
  - agilidade
  - inteligencia
- Equipamentos com requisitos mínimos
- Materiais de crafting e reforço
- Ferreiro com upgrades
- Pacto Sombrio com risco vs recompensa
- Sistema de moral e corrupção
- Progressão por mapa com bosses e mini-bosses
- Campanha zerável com múltiplos finais

## Stack

- `Python 3`
- `SQLite`

## Estrutura do Projeto

- [`menu.py`](C:\Users\User\Desktop\rpg\menu.py)
  - ponto de entrada do jogo
- [`game_core/main.py`](C:\Users\User\Desktop\rpg\game_core\main.py)
  - loop principal, criação e carregamento de personagem
- [`game_core/engine.py`](C:\Users\User\Desktop\rpg\game_core\engine.py)
  - combate, menus, progressão, narrativa e finais
- [`game_core/world.py`](C:\Users\User\Desktop\rpg\game_core\world.py)
  - áreas, bosses, itens, upgrades e pacto sombrio
- [`game_core/db.py`](C:\Users\User\Desktop\rpg\game_core\db.py)
  - persistência em banco local
- [`tests/test_campaign.py`](C:\Users\User\Desktop\rpg\tests\test_campaign.py)
  - testes de progressão e finais

## Como Rodar

```bash
python menu.py
```

## O Que Foi Validado

Atualmente o projeto já foi validado em:

- compilação dos módulos principais
- progressão de campanha área por área
- destravamento do mapa
- boss final
- final `heroi`
- final `vilao`
- final `equilibrio`
- final `morte`

## Decisões Técnicas

Algumas decisões importantes do projeto:

- `SQLite` foi escolhido por ser leve, local e suficiente para um RPG single-player em terminal
- o núcleo foi separado em `engine`, `world`, `db` e `main` para manter responsabilidades claras
- a maior parte do estado do personagem fica em uma estrutura única serializada no banco, reduzindo complexidade inicial
- a progressão da campanha foi mantida linear para evitar travas e facilitar testabilidade

## Roadmap

Melhorias futuras planejadas:

- mais polimento textual e narrativo
- talentos e evolução mais profunda por classe
- crafting completo
- reações mais fortes dos NPCs ao pacto sombrio
- possível versão futura com interface visual

## Aprendizados

Este projeto foi usado para praticar:

- modelagem de estado de jogo
- persistência de dados
- design de sistemas de RPG
- organização modular em Python
- fechamento de campanha e testes de fluxo
