"""
The entry point and feature configurations for the Primary Key Detection, 'pkd', command.
"""
from nubia import command, context

from dnikma_integrity_checker.helpers.utils import dicprint_table, db_ok, read_sql_file, DicLoadingSpinner
from dnikma_integrity_checker.shell.configs.dic_context import DicContext

_query = read_sql_file('pkd.sql')


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
        rows = run_pkd(db)
    dicprint_table(rows, ["column_name", "table_name", "data_type"])


def run_pkd(db) -> []:
    curs = db.query(_query)
    r = curs.fetchall()
    return r
