from __future__ import annotations

ALPHABET = "nouseai"


def f3_cipher(value: int, alphabet: str = ALPHABET) -> int:
    """Return character selected by value modulo alphabet length."""
    index = value % len(alphabet)
    return ord(alphabet[index])
