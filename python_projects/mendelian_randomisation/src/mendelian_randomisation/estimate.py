import sys

import click


@click.command()
def estimate() -> None:
    """Estimate causal effects using the IVW estimator. Not yet implemented."""
    click.echo("The estimate command is not yet implemented.", err=True)
    sys.exit(1)


if __name__ == "__main__":
    estimate()
