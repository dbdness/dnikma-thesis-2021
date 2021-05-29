"""
The entry point and feature configurations for the 'db-connect' commands, to handle connections to database instances.
"""
from nubia import command, argument, context

from dnikma_integrity_checker.helpers.utils import dicprint, Severity, DicLoadingSpinner
from dnikma_integrity_checker.shell.configs.dic_context import DicContext
from .mysql.mysql_conn import mysql_conn, MySQLConn


@command()
@argument('connection_string', type=str, positional=True,
          description="Format: host=myHostAddress;database=myDatabase;user=myUsername;password=myPassword;")
def db_connect(connection_string: str):
    """
    Connect to specified MySQL instance using a connection string.
    Most commands in this tool are dependent on an active MySQL connection.

    CONNECTION_STRING should be a valid MySQL connection string in the format:
    "host=myHostAddress;database=myDatabase;user=myUsername;password=myPassword;"
    --------------------------------------------------------------------------------------------------------------------
    """
    if connection_string.startswith("'") or connection_string.endswith("'"):
        dicprint('Error: Please use double quotes (") instead of single quotes to enclose the connection string.',
                 Severity.ERROR)
        return

    parsed = _parse_conn_str(connection_string)

    if not parsed:
        dicprint("Error: Connection string could not be parsed. Please be sure to follow the format as specified "
                 "in the 'help connect_mysql' menu.", Severity.ERROR)
        return

    redacted = parsed.copy()
    redacted['password'] = '*****'
    dicprint(str(redacted), Severity.INFO)
    dicprint("Attempting to connect to MySQL instance supplied...", Severity.INFO)
    open_connection(parsed)


def _parse_conn_str(conn_string: str) -> dict:
    params = {}
    try:
        params = dict(entry.split('=') for entry in conn_string.split(';') if entry)
    finally:
        return params


def open_connection(params) -> MySQLConn:
    ctx: DicContext = context.get_context()
    verbose = ctx.args.verbose
    try:
        with DicLoadingSpinner():
            db = mysql_conn.connect(params)
        dicprint(
            f"Connection to MySQL instance {params.get('database')}@{params.get('host')} successfully established.",
            Severity.SUCCESS)
        ctx.store_obj('mysql', db)
        if verbose:
            dicprint("Memory id of instance object: " + str(id(db)), Severity.INFO)
        return db
    except Exception as ex:
        dicprint("Connection to MySQL instance failed. A connection error occurred:", Severity.ERROR)
        dicprint(f'"{ex}"', Severity.NONE)
        dicprint("Please verify the specified connection string and make sure that an active MySQL instance exists on "
                 "the specified host.", Severity.ERROR)
