from nubia import command

from ..connect.connect import open_connection


@command(':development')
def development():
    """
    Activate development mode.
    A MySQL connection to a local 'northwind_nofks' schema will be established.
    --------------------------------------------------------------------------------------------------------------------
    """
    open_connection({'host': '127.0.0.1', 'database': 'northwind_nofks', 'user': 'root'})
