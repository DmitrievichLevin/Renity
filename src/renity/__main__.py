"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Renity."""


if __name__ == "__main__":
    main(prog_name="burgos")  # pragma: no cover
