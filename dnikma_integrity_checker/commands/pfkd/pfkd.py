"""
The entry point and feature configurations for the Potential Foreign Key Detection, 'pfkd', command.
"""
from nubia import command, argument, context

from dnikma_integrity_checker.commands.pkd.pkd import _run_pkd
from dnikma_integrity_checker.helpers.utils import db_ok, read_sql_file, dicprint_table, DicLoadingSpinner, \
    assign_row_numbers, stringify_query_build_rows, dicprint, Severity
from dnikma_integrity_checker.shell.configs.dic_context import DicContext

query = read_sql_file('pfkd-v2.sql')


@command('pfkd')
@argument('name_like_id',
          description="Consider only columns with a name pattern like “%id%” as potential foreign keys.",
          choices=['YES', 'NO'], positional=False)
def pfkd(name_like_id='NO'):
    """
    Find potential foreign key combinations in the current schema.
    This feature is powered by dnikma's Potential Foreign Key Detection (PfkD) algorithm.

    DISCLAIMER: Results may vary between different schemas. Please validate the outcome of this command before
    applying it to your own schema.
    --------------------------------------------------------------------------------------------------------------------
    """
    ctx: DicContext = context.get_context()
    db = ctx.get_mysql()

    if not db_ok(db):
        return

    rows = _get_pks(ctx, db)
    if not rows:
        # No PK constraints or ppkd output. Output error and hint and return early.
        dicprint("Error: No primary keys could be found in the current schema.", Severity.ERROR)
        dicprint("Primary keys are necessary for outputting optimal potential foreign keys pais.", Severity.INFO)
        dicprint("Please either create primary key constraints in the current schema manually, or run the 'ppkd' "
                 "command before this command.", Severity.INFO)
        return

    # PKs okay, continue pfkd
    if name_like_id == 'YES':
        dicprint("I will soon find potential foreign keys with %id% name pattern...", Severity.INFO)
        _f_name_like_id()
        return
    else:
        ctx.get_obj('ppkd_out')
        try:
            with DicLoadingSpinner():
                # Query build
                curs = db.query(query, params={"pk_nullable": 'NO'})
                rows = curs.fetchall()
                qb_str = stringify_query_build_rows(rows, order_by_desc='percent_match')
                # Executing mass query
                curs = db.query(qb_str)
                rows = curs.fetchall()
                nrows = assign_row_numbers(rows)
                ctx.store_obj('pfkd_out', nrows)
            dicprint_table(nrows,
                           ['left_col', 'right_col', 'count_left', 'count_right', 'diff_equal', 'distinct_left',
                            'distinct_right', 'diff_distinct', 'percent_match'], row_numbers=True)
        except Exception as ex:
            dicprint("An unknown error occurred. We are very sorry. Details:", Severity.ERROR)
            dicprint(f'{ex}', Severity.NONE)
            dicprint(
                "Do not hesitate to reach out to us with an issue on the official GitHub repository, "
                "describing the error in detail.",
                Severity.INFO)


def _f_name_like_id():
    pass


def _get_pks(ctx: DicContext, db) -> []:
    # Attempt to get PK constraints
    rows = _run_pkd(db)
    if not rows:
        # No PK constraints. Attempt to get ppkd output
        rows = ctx.get_obj('ppkd_out')
    return rows
