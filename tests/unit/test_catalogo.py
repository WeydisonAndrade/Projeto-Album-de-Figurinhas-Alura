"""
Camada UNITÁRIA (base da pirâmide):
valida regras isoladas do catálogo, mapeamento id↔imagem e consistência de dados.
"""
import re
from pathlib import Path

import pytest

from main import PASTA_BASE, PASTA_FRONTEND, figurinhas
from tests.helpers import parse_slot_id

CAMPOS_OBRIGATORIOS = {"id", "nome", "categoria", "imagem_url"}
CATEGORIAS_VALIDAS = {
    "IA",
    "PYTHON",
    "BANCO DE DADOS",
    "SISTEMAS OPERACIONAIS",
    "BRASIL",
}


def extrair_fallback_js(conteudo_js: str) -> list[dict]:
    """Extrai id, nome e imagem_url do FIGURINHAS_FALLBACK em app.js."""
    bloco = re.search(
        r"const FIGURINHAS_FALLBACK\s*=\s*\[(.*?)\];",
        conteudo_js,
        re.DOTALL,
    )
    assert bloco, "FIGURINHAS_FALLBACK não encontrado em app.js"
    itens = re.findall(
        r"\{\s*id:\s*(\d+)\s*,\s*nome:\s*\"([^\"]+)\"\s*,\s*imagem_url:\s*\"([^\"]+)\"\s*\}",
        bloco.group(1),
    )
    return [
        {"id": int(i), "nome": nome, "imagem_url": url}
        for i, nome, url in itens
    ]


@pytest.mark.unit
def test_catalogo_tem_29_figurinhas():
    assert len(figurinhas) == 29


@pytest.mark.unit
def test_ids_sao_unicos_e_sequenciais():
    ids = [f["id"] for f in figurinhas]
    assert ids == list(range(1, 30))


@pytest.mark.unit
def test_cada_figurinha_tem_campos_obrigatorios():
    for fig in figurinhas:
        faltando = CAMPOS_OBRIGATORIOS - set(fig.keys())
        assert not faltando, f"Figurinha {fig.get('id')} sem campos: {faltando}"
        assert isinstance(fig["id"], int)
        assert fig["nome"].strip()
        assert fig["categoria"] in CATEGORIAS_VALIDAS
        assert fig["imagem_url"].startswith("/imgs/")


@pytest.mark.unit
def test_nomes_nao_sao_duplicados():
    nomes = [f["nome"] for f in figurinhas]
    assert len(nomes) == len(set(nomes))


@pytest.mark.unit
def test_arquivo_de_imagem_existe_para_cada_figurinha(pasta_imagens):
    ausentes = []
    for fig in figurinhas:
        nome_arquivo = fig["imagem_url"].removeprefix("/imgs/")
        caminho = pasta_imagens / nome_arquivo
        if not caminho.is_file():
            ausentes.append(f"id={fig['id']} -> {nome_arquivo}")
    assert not ausentes, "Arquivos de imagem ausentes:\n" + "\n".join(ausentes)


@pytest.mark.unit
def test_parse_slot_id_espelha_frontend():
    assert parse_slot_id("#01") == 1
    assert parse_slot_id("#09") == 9
    assert parse_slot_id("#29") == 29
    assert parse_slot_id("#30") == 30


@pytest.mark.unit
def test_mapeamento_slot_para_figurinha():
    """Regra de negócio: slot #N deve receber a figurinha com id N."""
    por_id = {f["id"]: f for f in figurinhas}
    for n in range(1, 30):
        assert n in por_id
        assert por_id[n]["id"] == parse_slot_id(f"#{n:02d}")
    assert 30 not in por_id  # slot "Você" propositalmente sem figurinha


@pytest.mark.unit
def test_fallback_js_sincronizado_com_backend():
    js = (Path(PASTA_FRONTEND) / "app.js").read_text(encoding="utf-8")
    fallback = extrair_fallback_js(js)
    assert len(fallback) == len(figurinhas)

    por_id_api = {f["id"]: f for f in figurinhas}
    for item in fallback:
        api = por_id_api[item["id"]]
        assert item["nome"] == api["nome"]
        assert item["imagem_url"] == api["imagem_url"]


@pytest.mark.unit
def test_pastas_do_projeto_existem():
    base = Path(PASTA_BASE)
    assert (base / "figurinhas").is_dir()
    assert (base / "i-arq-ia-alura-album-main" / "index.html").is_file()
    assert (base / "i-arq-ia-alura-album-main" / "app.js").is_file()
