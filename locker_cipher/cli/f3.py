from __future__ import annotations

import click

from locker_cipher.ciphers.f3 import f3_cipher


@click.command()
@click.argument("value", type=int)
def main(value: int) -> None:
    """Run the F3 cipher."""
    click.echo(f"F3: {value} --> {f3_cipher(value)}")


if __name__ == "__main__":
    main()
