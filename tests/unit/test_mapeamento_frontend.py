"""
Testes unitários da lógica de colagem de figurinhas (espelho do app.js).
"""
from dataclasses import dataclass

import pytest

from tests.helpers import parse_slot_id


@dataclass
class SlotFake:
    numero: str
    imagens: list

    def query_selector_number(self):
        return self.numero


def aplicar_figurinhas(slots: list[dict], figurinhas: list[dict]) -> int:
    """Réplica da regra de aplicarFigurinhasNosSlots do app.js."""
    por_id = {f["id"]: f for f in figurinhas}
    coladas = 0
    for slot in slots:
        sid = parse_slot_id(slot["numero"])
        if sid not in por_id:
            continue
        if slot.get("ja_tem_imagem"):
            continue
        slot["imagem"] = por_id[sid]["imagem_url"]
        slot["nome_colado"] = por_id[sid]["nome"]
        coladas += 1
    return coladas


@pytest.mark.unit
def test_cola_apenas_slots_com_figurinha_correspondente():
    slots = [
        {"numero": "#01"},
        {"numero": "#02"},
        {"numero": "#30"},  # "Você" — sem figurinha
    ]
    figurinhas = [
        {"id": 1, "nome": "Alan Turing", "imagem_url": "/imgs/01-alan-turing.jpg"},
        {"id": 2, "nome": "John McCarthy", "imagem_url": "/imgs/02-john-mccarthy.jpg"},
    ]
    coladas = aplicar_figurinhas(slots, figurinhas)
    assert coladas == 2
    assert slots[0]["imagem"].endswith("01-alan-turing.jpg")
    assert slots[1]["nome_colado"] == "John McCarthy"
    assert "imagem" not in slots[2]


@pytest.mark.unit
def test_nao_cola_duas_vezes_no_mesmo_slot():
    slots = [{"numero": "#01", "ja_tem_imagem": True}]
    figurinhas = [
        {"id": 1, "nome": "Alan Turing", "imagem_url": "/imgs/01-alan-turing.jpg"},
    ]
    assert aplicar_figurinhas(slots, figurinhas) == 0
