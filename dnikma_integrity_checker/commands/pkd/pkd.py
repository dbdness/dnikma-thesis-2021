"""
The entry point and feature configurations for the Potential Foreign Key Detection, 'pkd', command.
"""
from nubia import command, argument, context
from termcolor import cprint
from prettytable import PrettyTable

pkdQuery = "SELECT sta.column_name, tab.table_name, cls.data_type FROM information_schema.TABLES AS tab INNER JOIN information_schema.statistics AS sta ON sta.table_schema = tab.table_schema AND sta.table_name = tab.table_name AND sta.index_name = 'primary' JOIN information_schema.`COLUMNS` AS cls ON tab.TABLE_SCHEMA = cls.TABLE_SCHEMA AND tab.TABLE_NAME = cls.TABLE_NAME AND sta.column_name = cls.column_name WHERE tab.table_schema = DATABASE() AND tab.table_type = 'BASE TABLE' ORDER BY tab.table_name"

@command('pkd')
def pkd():
    """
    Find all existing primary key constraints in the current schema.
    This feature is powered by dnikma's Primary Key Detection (pkD) algorithm.
    """

    ctx = context.get_context()
    db = ctx.obj.get('mysql')
    
    if db == None:
        cprint("No connection to MySQL instance was found. Please make sure to connect to a MySQL instance with the command 'connect-mysql CONNECTION_STRING' before using the 'pkd' command.")
        return
    
    curs = db.query(pkdQuery)
    r = curs.fetchall()

    x = PrettyTable(["column_name", "table_name", "data_type"])

    for row in r:
        x.add_row(row)

    x.align = "l"
    print(x)
    