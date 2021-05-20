import re

from nubia import command, argument, context

from dnikma_integrity_checker.commands.db_connect.mysql.mysql_conn import MySQLConn
from dnikma_integrity_checker.helpers.utils import dicprint, Severity, get_row_at_pos, read_sql_file, \
    DicLoadingSpinner, dicprint_table, db_ok
from dnikma_integrity_checker.shell.configs.dic_context import DicContext

query = read_sql_file('orphaned.sql')
orphaned_cols = ['orphan', 'parent', 'orphan_val']


@command('orphaned')
class Orphaned:
    """
    Find orphaned records in the current schema.
    This feature is powered by dnikma's orphaned algorithm.
    --------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self):
        self._ctx = context.get_context()
        self._db = self._ctx.get_mysql()

    @property
    def ctx(self) -> DicContext:
        return self._ctx

    @property
    def db(self) -> MySQLConn:
        return self._db

    @command()
    @argument('pfk_ids',
              description='Comma-separated IDs from the "pfkd" command output. Format example: "5, 18, 38".',
              positional=True,
              type=str)
    def pfkd(self, pfk_ids):
        """
        Find orphaned records from parent/child record output from the 'pfkd' command.
        Note that the "pfkd" command must be run at least once before this command.
        """
        if not db_ok(self.db):
            return

        ids = [i.strip() for i in pfk_ids.split(',')]
        try:
            ids = [int(i) for i in ids]
            if not ids:
                raise ValueError
        except (ValueError, TypeError):
            dicprint("Error: One or more supplied IDs are not convertible to integer type.", Severity.ERROR)
            dicprint("Please supply only comma-separated numbers as an argument.", Severity.INFO)
            return

        pfkd_out = self.ctx.get_obj('pfkd_out')
        if not pfkd_out:
            dicprint("Error: Could not find 'pfkd' output results", Severity.ERROR)
            dicprint("Please make sure to run the 'pfkd' command with valid output before running this command.",
                     Severity.INFO)
            return

        with DicLoadingSpinner():
            pfkd_out = [get_row_at_pos(pfkd_out, i) for i in ids]
            pairs = [p[-4:] for p in pfkd_out]  # Stripping all but last 4 helper-columns

            qb_rows = _run_orphaned(pairs, self._query_builder)
            orows = _run_orphaned(qb_rows, self._orphaned)
        dicprint_table(orows, orphaned_cols)

    @command()
    @argument('parent',
              description='Parent table and column. Format: "{parent_table}.{parent_column}"',
              type=str)
    @argument('child',
              description='Child table and column. Format: "{child_table}.{child_column}"',
              type=str)
    def input(self, parent: str, child: str):
        """
        Find orphaned records from manually specified parent/child record input.
        """
        if not db_ok(self.db):
            return

        regexp = r'\{(.*?)\}'  # Fetching strings between starting- ({) and closing (}) brackets

        mp = re.findall(regexp, parent)
        mc = re.findall(regexp, child)

        if (not mp or not mc) or (len(mp) < 2 or len(mc) < 2):
            dicprint("Error: Could not parse input parent- or child tables and columns.", Severity.ERROR)
            dicprint('Please make sure to follow the format of: "{parent_table}.{parent_column}"', Severity.INFO)
            return

        pairs = [(mp + mc)]  # Transforming pairs to fit the _query_builder function

        with DicLoadingSpinner():
            qb_rows = _run_orphaned(pairs, self._query_builder)
            if None in qb_rows:
                dicprint("Error: Database engine returned NULL.", Severity.ERROR)
                dicprint("It is possible that the specified table/column combinations could not be found "
                         "in the current schema.", Severity.ERROR)
                dicprint(f"Please verify input parent/child table/column combinations: {mp}, {mc}",
                         Severity.INFO)
                return
            orows = _run_orphaned(qb_rows, self._orphaned)
        dicprint_table(orows, orphaned_cols)

    def _query_builder(self, pairs: []) -> []:
        rows = []
        for p in pairs:
            curs = self.db.query(query, params={'child_tab': p[2],
                                                'child_col': p[3],
                                                'parent_tab': p[0],
                                                'parent_col': p[1]})
            r = curs.fetchone()
            rows.append(r)
        return rows

    def _orphaned(self, qb_rows) -> []:
        rows = []
        for q in qb_rows:
            curs = self.db.query(q[0])  # Index 0, as we know there is only one output from orphaned query builder.
            r = curs.fetchall()
            rows.extend(r)  # extend() is called, as r may be a list of n results.
        return rows


def _run_orphaned(elements: [], inner_func) -> []:
    """
    Wrapper function for orphaned functionality, contains error handling.
    :param elements: List of elements to pass to specified function.
    :param inner_func: Orphaned-related function, must accept a list of elements.
    :return: List of database engine output rows.
    """
    rows = []
    try:
        rows = inner_func(elements)
    except Exception as ex:
        dicprint("An unknown error occurred. We are very sorry. Details:", Severity.ERROR)
        dicprint(f'{ex}', Severity.NONE)
        dicprint(
            "Do not hesitate to reach out to us with an issue on the official GitHub repository, "
            "describing the error in detail.",
            Severity.INFO)
    finally:
        return rows
