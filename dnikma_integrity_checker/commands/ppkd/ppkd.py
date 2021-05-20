"""
The entry point and feature configurations for the Potential primary Key Detection, 'ppkd', command.
"""

from nubia import command, argument, context

from dnikma_integrity_checker.helpers.utils import db_ok, read_sql_file, dicprint_table, DicLoadingSpinner, \
    dicprint, Severity, run_query_builder
from dnikma_integrity_checker.shell.configs.dic_context import DicContext

_query = read_sql_file('ppkd.sql')
_query_f_nullable = read_sql_file('ppkd-flags/nullable.sql')
_ppkd_cols = ['col', 'count_total', 'count_distinct', 'percent_match']


@command('ppkd')
@argument('nullable',
          description='Include columns where null values are allowed',
          choices=['YES', 'NO'])
def ppkd(nullable='NO'):
    """
    Find potential primary key combinations in the current schema.
    This feature is powered by dnikma's Potential Primary Key Detection (PpkD) algorithm.

    DISCLAIMER: Results may vary between different schemas. Please validate the outcome of this command before
    applying it to your own schema.
    --------------------------------------------------------------------------------------------------------------------
    """
    ctx: DicContext = context.get_context()
    db = ctx.get_mysql()

    if not db_ok(db):
        return

    try:
        if nullable == 'YES':
            with DicLoadingSpinner():
                nrows = _f_nullable(db)
                ctx.store_obj('ppkd_out', nrows)
                stripped_rows = [r[:-1] for r in nrows]
            dicprint_table(stripped_rows, _ppkd_cols)
        else:
            with DicLoadingSpinner():
                nrows = run_ppkd(db)
                ctx.store_obj('ppkd_out', nrows)
                stripped_rows = [r[:-1] for r in nrows]
            dicprint_table(stripped_rows, _ppkd_cols)

    except Exception as ex:
        dicprint("An unknown error occurred. We are very sorry. Details:", Severity.ERROR)
        dicprint(f'{ex}', Severity.NONE)
        dicprint(
            "Do not hesitate to reach out to us with an issue on the official GitHub repository, "
            "describing the error in detail.",
            Severity.INFO)


def run_ppkd(db) -> []:
    nrows = run_query_builder(db, _query, assign_row_numbers=False, order_by_desc='percent_match')
    return nrows


def _f_nullable(db) -> []:
    nrows = run_query_builder(db, _query_f_nullable, assign_row_numbers=False, order_by_desc='percent_match')
    return nrows
