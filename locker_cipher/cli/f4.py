"""CLI entry point for the F4 cipher.
"""

from __future__ import annotations

import click

from locker_cipher.ciphers.f4 import f4_cipher


@click.command()
@click.argument("value", type=int)
def main(value: int) -> None:
    """Run the F4 cipher."""
    click.echo(f"F4: {value} --> {f4_cipher(value)}")


if __name__ == "__main__":
    main()
