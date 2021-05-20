from nubia import command, argument, context

from ..db_connect.db_connect import open_connection


@command(':development')
@argument('schema', choices=['northwind_nofks', 'northwind', 'northwind_orphaned'],
          description="Choose development schema.")
def development(schema: str = 'northwind_nofks'):
    """
    Activate development mode.
    A MySQL connection to a local development schema will be established.
    --------------------------------------------------------------------------------------------------------------------
    """
    context.get_context().args.verbose = 1
    open_connection({'host': '127.0.0.1', 'database': schema, 'user': 'root'})
