# locker-cipher

CLI tools for applying ciphers to locker numbers. Each cipher takes one or more integers and produces a new integer.

## Quick start

Run directly without cloning:

```bash
nix run github:fnivek/locker_cipher#f3 -- 12
nix run github:fnivek/locker_cipher#powerset-cipher -- f3 1 2 3
```

Or clone and enter the dev shell for interactive use:

```bash
nix develop
```

The dev shell sets up the environment and provides two commands:

```bash
# Run the F3 cipher on a single locker number
f3 12
# F3: 12 --> 97

# Run any cipher over every non-empty subset of a list of locker numbers
powerset-cipher f3 1 2 3
# f3: 1 --> 111
# f3: 2 --> 117
# f3: 3 --> 115
# f3: 1+2 (3) --> 115
# f3: 1+3 (4) --> 101
# f3: 2+3 (5) --> 97
# f3: 1+2+3 (6) --> 105
```

## Ciphers

| Name | Description |
|------|-------------|
| `f3` | Maps an integer to an ASCII code point via a fixed 7-character alphabet, wrapping cyclically. |

## Adding a cipher

1. Implement `my_cipher(value: int) -> int` in `locker_cipher/ciphers/my_cipher.py`
2. Register it in `locker_cipher/registry.py` under `CIPHERS`
3. Optionally add a dedicated CLI in `locker_cipher/cli/my_cipher.py`

`powerset-cipher` picks up any cipher registered in step 2 automatically.
