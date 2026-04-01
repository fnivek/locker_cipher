from locker_cipher.ciphers.f3 import f3_cipher


def test_f3_cipher_basic() -> None:
    assert f3_cipher(12) == 97


def test_f3_cipher_small_values() -> None:
    assert f3_cipher(1) == 111  # o
    assert f3_cipher(2) == 117  # u
    assert f3_cipher(3) == 115  # s
