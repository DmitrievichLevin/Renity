"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Burgos."""


if __name__ == "__main__":
    main(prog_name="burgos-lib")  # pragma: no cover
