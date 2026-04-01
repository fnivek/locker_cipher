from __future__ import annotations

from itertools import combinations

import click

from locker_cipher.registry import CIPHERS


def format_subset(values: tuple[int, ...]) -> str:
    """Format a subset as a human-readable sum expression."""
    return (
        "+".join(str(v) for v in values) + f" ({sum(values)})"
        if len(values) > 1
        else str(values[0])
    )


@click.command()
@click.argument("cipher_name", type=str)
@click.argument("values", nargs=-1, type=int)
def main(cipher_name: str, values: tuple[int, ...]) -> None:
    """Run a cipher over the non-empty power set sums of the given inputs."""
    if not values:
        raise click.UsageError("Provide at least one integer input.")

    try:
        cipher = CIPHERS[cipher_name]
    except KeyError as exc:
        valid = ", ".join(sorted(CIPHERS))
        raise click.UsageError(
            f"Unknown cipher '{cipher_name}'. Valid ciphers: {valid}"
        ) from exc

    for subset_size in range(1, len(values) + 1):
        for subset in combinations(values, subset_size):
            total = sum(subset)
            result = cipher(total)
            click.echo(f"{cipher_name}: {format_subset(subset)} --> {result}")


if __name__ == "__main__":
    main()
