"""F3 cipher: maps integers to ASCII code points via a fixed 7-character alphabet."""

from __future__ import annotations

ALPHABET = "nouseai"


def f3_cipher(value: int, alphabet: str = ALPHABET) -> int:
    """Map an integer to an ASCII code point using the F3 cipher alphabet.

    The mapping wraps cyclically, so all integers (including negative) produce
    a valid result.

    Args:
        value: The integer to encode (e.g. a locker number or subset sum).
        alphabet: The cipher alphabet to draw characters from.  Defaults to the
            standard F3 alphabet ``"nouseai"``.

    Returns:
        The ASCII code point of the mapped character.
    """
    index = value % len(alphabet)
    return ord(alphabet[index])
