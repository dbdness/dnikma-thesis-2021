from nubia import command, argument

from ..db_connect.db_connect import open_connection


@command(':development')
@argument('schema', choices=['northwind_nofks', 'northwind'], description="Choose development schema")
def development(schema: str = 'northwind_nofks'):
    """
    Activate development mode.
    A MySQL connection to a local development schema will be established.
    --------------------------------------------------------------------------------------------------------------------
    """
    open_connection({'host': '127.0.0.1', 'database': schema, 'user': 'root'})
