"""Central registry mapping cipher names to their implementations.

Add a new entry here to make a cipher available to all CLI tools (e.g.
``powerset-cipher``) without modifying them.
"""

from __future__ import annotations

from collections.abc import Callable

from locker_cipher.ciphers.f3 import f3_cipher

CipherFunc = Callable[[int], int]

# Maps each cipher's public name to its callable implementation.
CIPHERS: dict[str, CipherFunc] = {
    "f3": f3_cipher,
}
