"""
This is the main entry point file for the tool.
This is where all appropriate CLI commands, feature flags etc. are defined.
Major commands and features should call functionality from the appropriate modules from the
parent package (dnikma_integrity_checker)
"""

import click
import contextvars

from dnikma_integrity_checker.cli.about import about
from dnikma_integrity_checker.connect import connect
from dnikma_integrity_checker.pfkd import pfkd
from dnikma_integrity_checker.connect.mysql.conn import MySQLConn


@click.group(chain=True, invoke_without_command=True, help='dnikma MySQL Integrity Checker')
@click.option('--conn', type=click.Choice(['mysql'], case_sensitive=False))
@click.pass_context
def entry_point(ctx, conn):
    if conn:
        info = {'host': '127.0.0.1', 'database': 'northwind_nofks', 'user': 'root'}
        db = MySQLConn.Instance(info)
        print("Id of c1 : {}".format(str(id(db))))
        ctx.obj = db
        contextvars.ContextVar("db").set(db)
    pass

# # The connect functionality has to live here, in order to be able to pass a context.
# @entry_point.command(help='Connect to the specified database instance using a connection string.')
# @click.option('--dbms')
# @click.pass_obj
# def connect(obj, dbms):
#     """
#     Connect to specified MySQL instance using a connection string.
#     Any subsequent commands are dependent on an active MySQL connection.
#
#     CONNECTION_STRING should be a valid MySQL connection string in the format:
#     "host=myHostAddress;database=myDatabase;user=myUsername;password=myPassword;"
#     """
#     #ctx.obj = dbms
#     obj = dbms
#     click.echo("You chose type: " + dbms)


# Other available commands are added in sequence to the main Click CLI group here.
entry_point.add_command(about)
entry_point.add_command(connect.connect)
entry_point.add_command(pfkd.pfkd)
