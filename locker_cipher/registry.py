"""Central registry mapping cipher names to their implementations.

Add a new entry here to make a cipher available to all CLI tools (e.g.
``powerset-cipher``) without modifying them.
"""

from __future__ import annotations

from collections.abc import Callable

from locker_cipher.ciphers.f3 import f3_cipher

CipherFunc = Callable[[int], int]

# Maps each cipher's public name (lowercase) to its callable implementation.
CIPHERS: dict[str, CipherFunc] = {
    "f3": f3_cipher,
}


def get_cipher(name: str) -> CipherFunc:
    """Return the cipher registered under ``name``, case-insensitively.

    Raises:
        KeyError: If no cipher is registered under ``name``.  The error message
            includes the list of valid cipher names.
    """
    try:
        return CIPHERS[name.lower()]
    except KeyError:
        valid = ", ".join(sorted(CIPHERS))
        raise KeyError(f"Unknown cipher '{name}'. Valid ciphers: {valid}") from None
