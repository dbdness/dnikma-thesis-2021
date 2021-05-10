"""
Misc. helper utilities.
"""
from enum import Enum
from pathlib import Path

from halo import Halo
from prettytable import PrettyTable
from termcolor import cprint


class Severity(Enum):
    INFO = 'yellow'
    SUCCESS = 'green'
    ERROR = 'red'
    NONE = 'white'


def dicprint(txt, severity: Severity):
    if severity is Severity.NONE:
        print(txt)
        return
    cprint(txt, severity.value)


def dicprint_table(rows: [], columns: [], row_numbers: bool = False):
    cprint('')
    if row_numbers:
        columns.insert(0, '#')
    table = PrettyTable(columns)
    table.align = 'l'
    for row in rows:
        table.add_row(row)
    dicprint(table, Severity.NONE)


def stringify_query_build_rows(qb_rows: [], order_by_desc: str = None) -> str:
    """
    'Stringify' supplied rows by concatenating them, removing the final, dangling 'UNION ALL' keyword, and
    optionally appending an 'ORDER BY' clause.
    Intended for use with output rows of query builder algorithms.
    :param qb_rows: Output query builder rows.
    :param order_by_desc: Order by the specified field, descending.
    :return: Full query as string.
    """
    qb_str = ' '.join(r[0] for r in qb_rows)[:-9]
    if order_by_desc:
        qb_str += f' ORDER BY {order_by_desc} DESC'
    return qb_str


def assign_row_numbers(rows: []) -> []:
    """
    Append enumerator index (start 1) to each tuple element in supplied list.
    :param rows: MySQL runner query execution output; a list of tuples.
    :return: A new list of tuples with enumerated index number appended as the first item.
    """
    return [(idx,) + row for idx, row in enumerate(rows, start=1)]


def get_row_at_pos(nrows: [], pos: int) -> ():
    """
    Attempt to get the row at the specified position (index) of supplied numbered row output.
    :param nrows: Numbered rows. A index number must be the first part of the tuple.
    :param pos: Position/index of requested row.
    :return: The specified row as a tuple, if found.
    """
    row = [r for r in nrows if r[0] == pos]
    if not row:
        dicprint(f'Error: The specified output row number of {pos} could not be found.', Severity.ERROR)
        dicprint(
            "Please make sure that an appropriate command (such as 'pfkd' or 'ppkd') with valid output has been run "
            "before this command, and that the specified row number was present.", Severity.INFO)
        return None
    return row[0]


def db_ok(db) -> bool:
    if db is None:
        dicprint("Error: No active connection to a MySQL instance was found.", Severity.ERROR)
        dicprint("Please make sure to connect to a MySQL instance with the command 'connect-mysql' "
                 "before using this command.", Severity.INFO)
        return False
    return True


def read_sql_file(filename: str) -> str:
    wd = Path().absolute() / 'sql-queries'
    file = Path(wd / filename)
    if not file.is_file():
        # Fix for runs from source tree through runner.py
        wd = Path().absolute().parent / 'sql-queries'
        file = Path(wd / filename)
        if not file.is_file():
            dicprint("Error: The .sql file containing this query can not be found.", Severity.ERROR)
            dicprint(
                "Please make sure that a valid folder named 'sql-queries' exists one directory up from "
                "the main 'dnikma_integrity_checker directory.", Severity.INFO)
    return file.read_text()


class DicLoadingSpinner(object):
    def __init__(self):
        self.spinner = Halo(text='Loading', spinner='dots', color='green')

    def __enter__(self):
        self.spinner.start()
        return self.spinner

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.spinner.stop()
        self.spinner.clear()
