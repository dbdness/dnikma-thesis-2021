"""
The entry point and feature configurations for the Primary Key Detection, 'pkd', command.
"""
from nubia import command, context

from dnikma_integrity_checker.helpers.utils import dicprint_table, db_ok, read_sql_file, DicLoadingSpinner
from dnikma_integrity_checker.shell.configs.dic_context import DicContext

query = read_sql_file('pkd.sql')


@command('pkd')
def pkd():
    """
    Find all existing primary key constraints in the current schema.
    This feature is powered by dnikma's Primary Key Detection (pkD) algorithm.
    --------------------------------------------------------------------------------------------------------------------
    """
    ctx: DicContext = context.get_context()
    db = ctx.get_mysql()

    if not db_ok(db):
        return

    with DicLoadingSpinner():
        curs = db.query(query)
        r = curs.fetchall()
        dicprint_table(r, ["column_name", "table_name", "data_type"])
