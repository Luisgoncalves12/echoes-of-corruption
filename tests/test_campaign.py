import random
import unittest
from unittest.mock import patch

from game_core.engine import (
    criar_estado_inicial,
    determinar_tipo_final,
    enfrentar_boss_area,
    liberar_proxima_area,
)
from game_core.world import ORDEM_PROGRESSAO, buscar_area


class CampaignTests(unittest.TestCase):
    def make_champion(
        self,
        moral=0,
        corrupcao=0,
        vida=100,
        atk=20,
        defesa=10,
        crit=10,
        esq=8,
        mana=60,
        nivel=1,
        classe="Guerreiro",
    ):
        campeao = {
            "nome": "Teste",
            "classe": classe,
            "nivel": nivel,
            "xp": 0,
            "ouro": 0,
            "pontos_atributo": 0,
            "inventario": ["Pocao pequena"],
            "vida": vida,
            "atk": atk,
            "def": defesa,
            "crit": crit,
            "esq": esq,
            "mana": mana,
            "estado": criar_estado_inicial(vida, mana),
        }
        campeao["estado"]["atributos"] = {"forca": 12, "agilidade": 10, "inteligencia": 10}
        campeao["estado"]["moral"] = moral
        campeao["estado"]["corrupcao"] = corrupcao
        return campeao

    def test_all_progression_areas_have_boss(self):
        for area_nome in ORDEM_PROGRESSAO:
            area = buscar_area(area_nome)
            self.assertIsNotNone(area, f"Area ausente: {area_nome}")
            self.assertIsNotNone(area["boss"], f"Area sem boss/mini-boss: {area_nome}")

    def test_progression_unlocks_next_area(self):
        campeao = self.make_champion()
        self.assertEqual(campeao["estado"]["areas_liberadas"], ["Vila Inicial", "Floresta Sombria"])

        liberar_proxima_area(campeao, "Floresta Sombria")
        self.assertIn("Campos Abertos", campeao["estado"]["areas_liberadas"])

        liberar_proxima_area(campeao, "Campos Abertos")
        self.assertIn("Caverna Escura", campeao["estado"]["areas_liberadas"])

    def test_determine_final_types(self):
        heroi = self.make_champion(moral=9, corrupcao=1)
        vilao = self.make_champion(moral=1, corrupcao=9)
        equilibrio = self.make_champion(moral=5, corrupcao=5)

        self.assertEqual(determinar_tipo_final(heroi), "heroi")
        self.assertEqual(determinar_tipo_final(vilao), "vilao")
        self.assertEqual(determinar_tipo_final(equilibrio), "equilibrio")

    def test_final_boss_victory_concludes_campaign(self):
        campeao = self.make_champion(
            moral=9,
            corrupcao=1,
            vida=500,
            atk=80,
            defesa=40,
            crit=25,
            esq=18,
            mana=220,
            nivel=20,
            classe="Paladino",
        )
        campeao["estado"]["areas_liberadas"] = ["Vila Inicial"] + ORDEM_PROGRESSAO

        area_final = buscar_area("Castelo do Rei Demonio")
        random.seed(4)
        with patch("builtins.input", side_effect=["1"] * 200):
            enfrentar_boss_area(campeao, area_final)

        self.assertTrue(campeao["estado"]["campanha_concluida"])
        self.assertEqual(campeao["estado"]["tipo_final"], "heroi")

    def test_final_boss_defeat_sets_morte(self):
        campeao = self.make_champion(
            moral=1,
            corrupcao=1,
            vida=50,
            atk=5,
            defesa=1,
            crit=1,
            esq=1,
            mana=20,
            nivel=1,
            classe="Mago",
        )
        campeao["estado"]["areas_liberadas"] = ["Vila Inicial"] + ORDEM_PROGRESSAO

        area_final = buscar_area("Castelo do Rei Demonio")
        random.seed(1)
        with patch("builtins.input", side_effect=["1"] * 60):
            enfrentar_boss_area(campeao, area_final)

        self.assertTrue(campeao["estado"]["campanha_concluida"])
        self.assertEqual(campeao["estado"]["tipo_final"], "morte")


if __name__ == "__main__":
    unittest.main()
