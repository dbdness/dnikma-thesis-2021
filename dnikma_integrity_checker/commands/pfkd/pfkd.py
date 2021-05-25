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
_query_f_potential_pks = read_sql_file('pfkd-flags/potential-pks.sql')
_pfkd_cols = ['left_col', 'right_col', 'count_left', 'count_right', 'diff_equal', 'distinct_left',
              'distinct_right', 'diff_distinct', 'percent_match', 'percent_match_distinct']


@command('pfkd')
@argument('name_like_id',
          description="Consider only columns with a name pattern like “%id%” as potential foreign keys.",
          choices=['YES', 'NO'])
@argument('potential_pks',
          description='Detect and use potential primary keys in the potential foreign key detection. '
                      'NOTE: Before using this argument, make sure you have run the "ppkd" command at least once.',
          choices=['YES', 'NO'])
def pfkd(name_like_id='NO', potential_pks='NO'):
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

    rows = _try_get_pks(db)
    if not rows:
        # No PK constraints or ppkd output. Output error and hint and return early.
        dicprint("Error: No primary keys could be found in the current schema.", Severity.ERROR)
        dicprint("Primary keys are necessary for outputting optimal potential foreign keys pais.", Severity.INFO)
        dicprint("Please either create primary key constraints in the current schema manually, or run the 'ppkd' "
                 "command before this command. Use the argument 'potential-pks=YES' together with the 'ppkd' comand.",
                 Severity.INFO)
        return
        # PKs okay, continue pfkd
    try:
        if name_like_id == 'YES':
            # FLAG: name-like-id
            with DicLoadingSpinner():
                nrows = _f_name_like_id(db)
                ctx.store_obj('pfkd_out', nrows)
                nrows_stripped = [r[:-4] for r in nrows]
            dicprint_table(nrows_stripped, _pfkd_cols, row_numbers=True)
        elif potential_pks == 'YES':
            ppkd_nullable_rows = ctx.get_obj('ppkd_nullable_out')
            if ppkd_nullable_rows:
                dicprint("Error: The 'pfkd' command cannot be run with potential primary key combinations from 'ppkd' "
                         "that includes nullable columns. \nThe assumptions of the underlying algorithms would output "
                         "too many false positives as of this alpha release.", Severity.ERROR)
                dicprint("Please run the 'ppkd' command without the 'nullable=Yes' flag.", Severity.INFO)
                return
            ppkd_rows = ctx.get_obj('ppkd_out')
            if ppkd_rows is None:
                dicprint("Error: No previous run of 'ppkd' has been found.", Severity.ERROR)
                dicprint("Please run the 'ppkd' command before using the argument 'potential_pks'.", Severity.INFO)
                return
            with DicLoadingSpinner():
                nrows = _f_potential_pks(ppkd_rows, db)
                if nrows is None:
                    return
                ctx.store_obj('pfkd_out', nrows)
                nrows_stripped = [r[:-4] for r in nrows]
            dicprint_table(nrows_stripped, _pfkd_cols, row_numbers=True)
        else:
            # No flag, normal execution
            with DicLoadingSpinner():
                nrows = run_pfkd(db)
                ctx.store_obj('pfkd_out', nrows)
                nrows_stripped = [r[:-4] for r in nrows]
            dicprint_table(nrows_stripped, _pfkd_cols, row_numbers=True)
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
                              order_by_desc='percent_match_distinct')
    return nrows


def _f_name_like_id(db) -> []:
    nrows = run_query_builder(db, _query_f_name_like_id,
                              assign_row_numbers=True,
                              order_by_desc='percent_match_distinct')
    return nrows


def _try_get_pks(db) -> []:
    # Attempt to get PK constraints
    rows = run_pkd(db)
    if not rows:
        return None
    return rows


def _f_potential_pks(ppkd_rows: [], db) -> []:
    pk_col = [r[4:] for r in ppkd_rows]  # Gets the right column
    string_arr = [''.join(i) for i in pk_col]  # Converts tuple array to string array
    in_placeholders = ', '.join(map(lambda x: '%s', string_arr))  # Adding x number of %s placeholders
    query = _query_f_potential_pks % (in_placeholders, in_placeholders)  # Inserting the placeholders
    params = string_arr
    params.extend(string_arr)
    nrows = run_query_builder(db, query, assign_row_numbers=True, order_by_desc='percent_match_distinct', params=params)
    return nrows
