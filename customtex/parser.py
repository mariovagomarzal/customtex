"""This module contain the argument parser for the customtex command."""

import click

from customtex import __version__
from customtex.defaults import *


@click.command()
@click.argument("path", type=click.File(mode="w"))
def init(path, template_name, options, overwrite):
    pass
