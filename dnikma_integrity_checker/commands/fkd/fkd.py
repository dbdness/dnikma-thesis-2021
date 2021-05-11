"""
The entry point and feature configurations for the Foreign Key Detection, 'fkd', command.
"""
from nubia import command, context

from dnikma_integrity_checker.helpers.utils import dicprint_table, db_ok, read_sql_file, DicLoadingSpinner
from dnikma_integrity_checker.shell.configs.dic_context import DicContext

query = read_sql_file('fkd.sql')


@command('fkd')
def fkd():
    """
    Find all existing foreign key constraints in the current schema.
    This feature is powered by dnikma's Foreign Key Detection (fkD) algorithm.
    --------------------------------------------------------------------------------------------------------------------
    """
    ctx: DicContext = context.get_context()
    db = ctx.get_mysql()

    if not db_ok(db):
        return

    with DicLoadingSpinner():
        rows = _run_fkd(db)
    dicprint_table(rows, ["table_name", "constraint_name"])


def _run_fkd(db) -> []:
    curs = db.query(query)
    r = curs.fetchall()
    return r
