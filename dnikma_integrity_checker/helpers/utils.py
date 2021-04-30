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
