"""Fixtures compartilhadas da suíte de testes."""
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import PASTA_FRONTEND, PASTA_IMAGENS, app, figurinhas


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def catalogo():
    return figurinhas


@pytest.fixture(scope="session")
def pasta_imagens():
    return Path(PASTA_IMAGENS)


@pytest.fixture(scope="session")
def pasta_frontend():
    return Path(PASTA_FRONTEND)


@pytest.fixture(scope="session")
def html_album(pasta_frontend):
    return (pasta_frontend / "index.html").read_text(encoding="utf-8")
