"""
Misc. helper utilities.
"""

from enum import Enum

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


def dicprint_table(rows, columns: []):
    table = PrettyTable(columns)
    table.align = 'l'
    for row in rows:
        table.add_row(row)
    dicprint(table, Severity.NONE)


def verify_db(db):
    if db is None:
        dicprint("Error: No active connection to a MySQL instance was found.", Severity.ERROR)
        dicprint("Please make sure to connect to a MySQL instance with the command 'connect-mysql'"
                 "before using the 'pkd' command.", Severity.ERROR)
        return
