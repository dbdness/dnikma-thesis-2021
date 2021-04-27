"""
The entry point and feature configurations for the 'connect' command, to handle connections to database instances.
"""
from nubia import command, argument, context
from termcolor import cprint

from .mysql.mysql_conn import mysql_conn


@command()
@argument('connection_string', positional=True)
def connect_mysql(connection_string):
    """
    Connect to specified MySQL instance using a connection string.
    Any subsequent commands are dependent on an active MySQL connection.

    CONNECTION_STRING should be a valid MySQL connection string in the format:
    "host=myHostAddress;database=myDatabase;user=myUsername;password=myPassword;"
    """
    if connection_string.startswith("'") or connection_string.endswith("'"):
        cprint('Please use double quotes (") instead of single quotes to enclose the connection string.')
        return
    parsed = __parse_conn_str(connection_string)
    cprint("Parsed the following connection details:")
    redacted = parsed.copy()
    redacted['password'] = '*****'
    cprint(str(redacted))
    cprint("Attempting to connect to MySQL instance supplied...")

    try:
        db = mysql_conn.connect(parsed)
        cprint("Id of db: " + str(id(db)))
        ctx = context.get_context()
        ctx.obj['mysql'] = db
    except Exception as ex:
        cprint("Connection to MySQL instance failed. A connection error occurred:")
        cprint(f'{ex}')
        cprint("Please verify the specified connection string.")


def __parse_conn_str(conn_string: str):
    params = dict(entry.split('=') for entry in conn_string.split(';') if entry)
    return params
