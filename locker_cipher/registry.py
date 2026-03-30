from __future__ import annotations

from collections.abc import Callable

from locker_cipher.ciphers.f3 import f3_cipher

CipherFunc = Callable[[int], int]

CIPHERS: dict[str, CipherFunc] = {
    "f3": f3_cipher,
}
