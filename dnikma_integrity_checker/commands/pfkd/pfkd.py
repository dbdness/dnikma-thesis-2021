"""
The entry point and feature configurations for the Potential Foreign Key Detection, 'pfkd', command.
"""
from nubia import command, argument, context

from dnikma_integrity_checker.commands.pkd.pkd import run_pkd
from dnikma_integrity_checker.helpers.utils import db_ok, read_sql_file, dicprint_table, DicLoadingSpinner, \
    dicprint, Severity, run_query_builder
from dnikma_integrity_checker.shell.configs.dic_context import DicContext

_query = read_sql_file('pfkd-v2.sql')
_query_f_name_like_id = read_sql_file('pfkd-flags/name-like-id.sql')
_pfkd_cols = ['left_col', 'right_col', 'count_left', 'count_right', 'diff_equal', 'distinct_left',
              'distinct_right', 'diff_distinct', 'percent_match']


@command('pfkd')
@argument('name_like_id',
          description="Consider only columns with a name pattern like “%id%” as potential foreign keys.",
          choices=['YES', 'NO'])
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

    ids = ['id', '_id', 'test', 'lygtemund']
    in_placeholders = ', '.join(map(lambda x: '%s', ids))

    q = _query % (in_placeholders, in_placeholders)
    params = ids
    params.extend(ids)
    # params.extend(ids)

    curs = db.query(q, params)
    r = curs.fetchall()
    return

    rows = _try_get_pks(ctx, db)
    if not rows:
        # No PK constraints or ppkd output. Output error and hint and return early.
        dicprint("Error: No primary keys could be found in the current schema.", Severity.ERROR)
        dicprint("Primary keys are necessary for outputting optimal potential foreign keys pais.", Severity.INFO)
        dicprint("Please either create primary key constraints in the current schema manually, or run the 'ppkd' "
                 "command before this command.", Severity.INFO)
        return
        # PKs okay, continue pfkd
    try:
        if name_like_id == 'YES':
            # FLAG: name-like-id
            with DicLoadingSpinner():
                nrows = _f_name_like_id(db)
                ctx.store_obj('pfkd_out', nrows)
            dicprint_table(nrows, _pfkd_cols, row_numbers=True)
        else:
            # No flag, normal execution
            with DicLoadingSpinner():
                nrows = run_pfkd(db)
                ctx.store_obj('pfkd_out', nrows)
            dicprint_table(nrows, _pfkd_cols, row_numbers=True)
    except Exception as ex:
        dicprint("An unknown error occurred. We are very sorry. Details:", Severity.ERROR)
        dicprint(f'{ex}', Severity.NONE)
        dicprint(
            "Do not hesitate to reach out to us with an issue on the official GitHub repository, "
            "describing the error in detail.",
            Severity.INFO)


def run_pfkd(db) -> []:
    nrows = run_query_builder(db, _query,
                              assign_row_numbers=True,
                              order_by_desc='percent_match')
    return nrows


def _f_name_like_id(db) -> []:
    nrows = run_query_builder(db, _query_f_name_like_id,
                              assign_row_numbers=True,
                              order_by_desc='percent_match')
    return nrows


def _try_get_pks(ctx: DicContext, db) -> []:
    # Attempt to get PK constraints
    rows = run_pkd(db)
    if not rows:
        # No PK constraints. Attempt to get ppkd output
        rows = ctx.get_obj('ppkd_out')
        pk_cols = [r[5:5] for r in rows]
    return rows
