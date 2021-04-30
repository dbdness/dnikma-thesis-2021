"""
The entry point and feature configurations for the 'connect' commands, to handle connections to database instances.
"""
from nubia import command, argument, context

from dnikma_integrity_checker.helpers.utils import dicprint, Severity
from .mysql.mysql_conn import mysql_conn, MySQLConn


@command()
@argument('connection_string', type=str, positional=True,
          description="Format: host=myHostAddress;database=myDatabase;user=myUsername;password=myPassword;")
def connect_mysql(connection_string: str):
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

    parsed = __parse_conn_str(connection_string)

    if not parsed:
        dicprint("Error: Connection string could not be parsed. Please be sure to follow the format as specified "
                 "in the 'help connect_mysql' menu.", Severity.ERROR)
        return

    redacted = parsed.copy()
    redacted['password'] = '*****'
    dicprint(str(redacted), Severity.INFO)
    dicprint("Attempting to connect to MySQL instance supplied...", Severity.INFO)
    open_connection(parsed)


def __parse_conn_str(conn_string: str) -> dict:
    params = {}
    try:
        params = dict(entry.split('=') for entry in conn_string.split(';') if entry)
    finally:
        return params


def open_connection(params) -> MySQLConn:
    ctx = context.get_context()
    verbose = ctx.args.verbose
    try:
        db = mysql_conn.connect(params, verbose)
        dicprint(f"Connection to MySQL instance @ {params.get('host')} successfully established.", Severity.SUCCESS)
        ctx.obj['mysql'] = db
        if verbose:
            dicprint("Memory id of instance object: " + str(id(db)), Severity.INFO)
        return db
    except Exception as ex:
        dicprint("Connection to MySQL instance failed. A connection error occurred:", Severity.ERROR)
        dicprint(f'{ex}', Severity.ERROR)
        dicprint("Please verify the specified connection string.", Severity.ERROR)
