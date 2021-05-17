from nubia import command, argument, context

from dnikma_integrity_checker.commands.db_connect.mysql.mysql_conn import MySQLConn
from dnikma_integrity_checker.helpers.utils import dicprint, Severity, get_row_at_pos, read_sql_file, \
    DicLoadingSpinner, dicprint_table
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
    @argument('pk_ids',
              description='Comma-separated IDs from the "pfkd" command output. Format example: "5, 18, 38".',
              positional=True,
              type=str)
    def pfkd(self, pk_ids):
        """
        Find orphaned records from parent/child record output from the 'pfkd' command.
        Note that the "pfkd" command must be run at least once before this command.
        """
        ids = [i.strip() for i in pk_ids.split(',')]
        # if any(not isinstance(val, int) for val in ids):
        try:
            ids = [int(i) for i in ids]
        except ValueError:
            dicprint("Error: One or more supplied IDs are not convertible to integer type.", Severity.ERROR)
            dicprint("Please supply only comma-separated numbers as an argument.", Severity.INFO)

        with DicLoadingSpinner():
            pfkd_out = self.ctx.get_obj('pfkd_out')
            pfkd_out = [get_row_at_pos(pfkd_out, i) for i in ids]
            pairs = [p[-4:] for p in pfkd_out]  # Stripping all but last 4 helper-columns

            def query_builder() -> []:
                rows = []
                for p in pairs:
                    curs = self.db.query(query, params={'child_tab': p[2],
                                                        'child_col': p[3],
                                                        'parent_tab': p[0],
                                                        'parent_col': p[1]})
                    r = curs.fetchone()
                    rows.append(r)
                return rows

            qb_rows = _run_orphaned(query_builder)

            def orphaned() -> []:
                rows = []
                for q in qb_rows:
                    curs = self.db.query(q[0])
                    r = curs.fetchall()
                    rows.extend(r)  # extend() is called, as r may be a list of n results.
                return rows

            orows = _run_orphaned(orphaned)
        dicprint_table(orows, orphaned_cols)

    @command()
    @argument('parent',
              description="Parent table and column. Format: '{parent_table}.{parent_column}'",
              type=str)
    @argument('child',
              description="Child table and column. Format: '{child_table}.{child_column}'",
              type=str)
    def input(self, parent: str, child: str):
        """
        Find orphaned records from manually specified parent/child record input.
        """
        pass

    # def _run_orphaned_query_builder(self, pairs: []) -> []:
    #     rows = []
    #     try:
    #         for pair in pairs:
    #             row = self.db.query(query, params={'child_tab': pair[0],
    #                                                'child_col': pair[1],
    #                                                'parent_tab': pair[2],
    #                                                'parent_col': pair[3]})
    #             rows.append(row)
    #     except Exception as ex:
    #         dicprint("An unknown error occurred. We are very sorry. Details:", Severity.ERROR)
    #         dicprint(f'{ex}', Severity.NONE)
    #         dicprint(
    #             "Do not hesitate to reach out to us with an issue on the official GitHub repository, "
    #             "describing the error in detail.",
    #             Severity.INFO)
    #     finally:
    #         return rows


def _run_orphaned(inner_func) -> []:
    rows = []
    try:
        rows = inner_func()
        # for q in qb_queries:
        #     row = self.db.query(q)
        #     rows.append(row)
    except Exception as ex:
        dicprint("An unknown error occurred. We are very sorry. Details:", Severity.ERROR)
        dicprint(f'{ex}', Severity.NONE)
        dicprint(
            "Do not hesitate to reach out to us with an issue on the official GitHub repository, "
            "describing the error in detail.",
            Severity.INFO)
    finally:
        return rows
