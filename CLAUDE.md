# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all tests
pytest tests/

# Run a single test
pytest tests/test_f3.py::test_f3_cipher_basic

# Run ciphers directly (from repo root with PYTHONPATH set)
PYTHONPATH=. python -m locker_cipher.cli.f3 <value>
PYTHONPATH=. python -m locker_cipher.cli.powerset_cipher <cipher_name> <values...>

# Nix: enter dev shell (sets PYTHONPATH and shell aliases automatically)
nix develop

# Nix: build and run
nix run .#f3 -- <value>
nix run .#powerset-cipher -- <cipher_name> <values...>
```

## Architecture

The project implements modular cipher CLI tools. There are two layers:

**Cipher functions** (`locker_cipher/ciphers/`): Pure functions `(int) -> int`. Each takes an integer input and returns an integer (ASCII code). `f3_cipher` maps `value % len(ALPHABET)` to the ordinal of the corresponding character in the alphabet `"nouseai"`.

**CLI commands** (`locker_cipher/cli/`): Click-based entrypoints. `f3.py` runs f3 directly on a single value. `powerset_cipher.py` takes a cipher name and a list of integers, then runs the cipher on the sum of every non-empty subset (the powerset of the inputs).

**Registry** (`locker_cipher/registry.py`): `CIPHERS` dict maps cipher name strings to their functions. `powerset_cipher` looks up ciphers here. When adding a new cipher, register it in `CIPHERS`.

**Adding a new cipher**: implement `my_cipher(value: int) -> int` in `locker_cipher/ciphers/my_cipher.py`, add it to `CIPHERS` in `registry.py`, and optionally add a dedicated CLI in `locker_cipher/cli/my_cipher.py`. The powerset CLI will pick it up automatically via the registry.
