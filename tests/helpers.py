"""Utilitários compartilhados pelos testes."""


def parse_slot_id(texto: str) -> int:
    """Espelha a lógica do app.js: '#01' -> 1."""
    return int(texto.replace("#", "").strip())
