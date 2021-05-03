from nubia import command, argument

from ..connect.connect import open_connection


@command(':development')
@argument('schema', choices=['northwind_nofks', 'northwind'])
def development(schema: str = 'northwind_nofks'):
    """
    Activate development mode.
    A MySQL connection to a local development schema will be established ('northwind_nofks' is the default choice).
    --------------------------------------------------------------------------------------------------------------------
    """
    open_connection({'host': '127.0.0.1', 'database': schema, 'user': 'root'})
