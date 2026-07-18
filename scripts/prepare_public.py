"""
Prepara a pasta public/ para a Vercel servir o front e as imagens via CDN.

Na Vercel, arquivos em public/ são servidos pelo CDN (mais rápido).
O FastAPI fica responsável apenas pela API (/figurinhas).
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "i-arq-ia-alura-album-main"
IMAGENS = ROOT / "figurinhas"
PUBLIC = ROOT / "public"


def main() -> None:
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)

    for nome in ("index.html", "style.css", "app.js"):
        origem = FRONTEND / nome
        if not origem.is_file():
            raise FileNotFoundError(f"Arquivo do frontend ausente: {origem}")
        shutil.copy2(origem, PUBLIC / nome)

    destino_imgs = PUBLIC / "imgs"
    destino_imgs.mkdir()
    for arquivo in IMAGENS.iterdir():
        if arquivo.is_file():
            shutil.copy2(arquivo, destino_imgs / arquivo.name)

    total = sum(1 for _ in destino_imgs.iterdir())
    print(f"public/ pronto: frontend + {total} imagens em public/imgs/")


if __name__ == "__main__":
    main()
