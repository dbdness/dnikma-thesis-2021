"""
This is the main entry point file for the tool.
This is where all appropriate CLI commands, feature flags etc. are defined.
Major commands and features should call functionality from the appropriate modules from the
parent package (dnikma_integrity_checker)
"""

import click

from .about import about
from ..connect import connect
from ..pfkd import pfkd


@click.group(help='dnikma MySQL Integrity Checker')
def entry_point():
    # Do nothing.
    pass


# Available commands are added in sequence to the main Click CLI group here.
entry_point.add_command(about)
entry_point.add_command(connect.connect_mysql)
entry_point.add_command(pfkd.pfkd)
