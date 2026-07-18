"""
Camada E2E (topo da pirâmide):
simula o fluxo completo do álbum — HTML dos slots ↔ API ↔ imagens.
"""
import re

import pytest
from bs4 import BeautifulSoup

from tests.helpers import parse_slot_id


def _slots_do_album(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    slots = []
    for slot in soup.select(".sticker-slot"):
        numero_el = slot.select_one(".slot-number")
        nome_el = slot.select_one(".slot-name")
        if not numero_el:
            continue
        slots.append(
            {
                "id": parse_slot_id(numero_el.get_text()),
                "nome": nome_el.get_text(strip=True) if nome_el else "",
                "numero_texto": numero_el.get_text(strip=True),
            }
        )
    return slots


@pytest.mark.e2e
def test_album_abre_e_api_responde(client):
    album = client.get("/")
    api = client.get("/figurinhas")
    assert album.status_code == 200
    assert api.status_code == 200
    assert len(api.json()) == 29


@pytest.mark.e2e
def test_slots_html_correspondem_aos_personagens_da_api(client):
    html = client.get("/").text
    slots = _slots_do_album(html)
    api = {f["id"]: f for f in client.get("/figurinhas").json()}

    assert len(slots) == 30, "Álbum deve ter 30 slots (#01–#30)"

    divergencias = []
    for slot in slots:
        sid = slot["id"]
        if sid == 30:
            assert slot["nome"] == "Você"
            assert sid not in api
            continue
        if sid not in api:
            divergencias.append(f"Slot {slot['numero_texto']} sem figurinha na API")
            continue
        if slot["nome"] != api[sid]["nome"]:
            divergencias.append(
                f"Slot {slot['numero_texto']}: HTML='{slot['nome']}' vs API='{api[sid]['nome']}'"
            )
    assert not divergencias, "Divergências HTML↔API:\n" + "\n".join(divergencias)


@pytest.mark.e2e
def test_fluxo_colar_figurinha_por_id(client):
    """
    Reproduz o fluxo do app.js:
    para cada slot com id na API, a imagem_url deve carregar (HTTP 200).
    """
    html = client.get("/").text
    slots = _slots_do_album(html)
    api = {f["id"]: f for f in client.get("/figurinhas").json()}

    coladas = 0
    falhas = []
    for slot in slots:
        fig = api.get(slot["id"])
        if not fig:
            continue
        img = client.get(fig["imagem_url"])
        if img.status_code != 200 or not img.content:
            falhas.append(f"#{slot['id']:02d} {fig['nome']} -> {fig['imagem_url']}")
        else:
            coladas += 1

    assert coladas == 29
    assert not falhas, "Falha ao 'colar' figurinhas:\n" + "\n".join(falhas)


@pytest.mark.e2e
def test_app_js_referencia_endpoint_e_seletores_do_album(client):
    js = client.get("/app.js").text
    assert "/figurinhas" in js
    assert "sticker-slot" in js
    assert "slot-number" in js
    assert "sticker-img" in js
    assert "aplicarFigurinhasNosSlots" in js or "colarFigurinhaNoSlot" in js


@pytest.mark.e2e
def test_css_define_estilo_da_figurinha_colada(client):
    css = client.get("/style.css").text
    assert ".sticker-img" in css
    assert ".slot-preenchido" in css
    assert re.search(r"sticker-aparecer", css)
