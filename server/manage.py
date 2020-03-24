import os

import click
import nose
import redis

from helpers.service import Service
from services.service_list import google_mail_service
from helpers.redis_helpers import flushAllData


@click.group()
def cli():
    pass


@cli.command()
@click.option('--flush', is_flag=True)
def start(flush):
    """
    Starting all services. Waiting for MQTT messages.
    """
    if flush:
        flushAllData()
    s = Service([google_mail_service])


@cli.command()
def test():
    """
    Running tests with nose
    """
    nose.run()


if __name__ == "__main__":
    cli()
