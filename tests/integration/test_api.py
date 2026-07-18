"""
Camada de INTEGRAÇÃO (meio da pirâmide):
valida API FastAPI + arquivos estáticos trabalhando juntos.
"""
import pytest


@pytest.mark.integration
def test_get_figurinhas_retorna_200_e_lista(client):
    resposta = client.get("/figurinhas")
    assert resposta.status_code == 200
    dados = resposta.json()
    assert isinstance(dados, list)
    assert len(dados) == 29


@pytest.mark.integration
def test_get_figurinhas_contrato_json(client):
    dados = client.get("/figurinhas").json()
    for fig in dados:
        assert set(fig.keys()) >= {"id", "nome", "categoria", "imagem_url"}


@pytest.mark.integration
def test_cors_libera_origem(client):
    origem = "http://localhost:5500"
    resposta = client.get(
        "/figurinhas",
        headers={"Origin": origem},
    )
    assert resposta.status_code == 200
    # Com allow_origins=["*"] e credentials=False, o header deve ser "*"
    assert resposta.headers.get("access-control-allow-origin") == "*"


@pytest.mark.integration
def test_cors_preflight_options(client):
    origem = "http://localhost:5500"
    resposta = client.options(
        "/figurinhas",
        headers={
            "Origin": origem,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert resposta.status_code in (200, 204)
    assert resposta.headers.get("access-control-allow-origin") == "*"
    assert "GET" in (resposta.headers.get("access-control-allow-methods") or "").upper()


@pytest.mark.integration
def test_cada_imagem_url_da_api_e_servida(client, catalogo):
    falhas = []
    for fig in catalogo:
        resp = client.get(fig["imagem_url"])
        if resp.status_code != 200:
            falhas.append(f"{fig['id']} {fig['imagem_url']} -> {resp.status_code}")
            continue
        if not resp.content:
            falhas.append(f"{fig['id']} {fig['imagem_url']} -> corpo vazio")
    assert not falhas, "Imagens inacessíveis via /imgs:\n" + "\n".join(falhas)


@pytest.mark.integration
def test_frontend_index_e_assets_basicos(client):
    index = client.get("/")
    assert index.status_code == 200
    assert "text/html" in index.headers.get("content-type", "")
    assert b"sticker-slot" in index.content

    css = client.get("/style.css")
    assert css.status_code == 200

    js = client.get("/app.js")
    assert js.status_code == 200
    assert b"preencherFigurinhas" in js.content


@pytest.mark.integration
def test_imagem_inexistente_retorna_404(client):
    resp = client.get("/imgs/arquivo-que-nao-existe.jpg")
    assert resp.status_code == 404
