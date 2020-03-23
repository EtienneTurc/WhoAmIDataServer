import click
import nose


@click.group()
def cli():
    pass


@cli.command()
def test():
    """
    Running tests with nose
    """
    nose.run()


if __name__ == "__main__":
    cli()
