"""
The entry point and feature configurations for the Foreign Key Detection, 'fkd', command.
"""
import requests
from nubia import command, context

from dnikma_integrity_checker.helpers.utils import dicprint, dicprint_table, Severity, verify_db

query_page = requests.get(
    "")


@command('fkd')
def fkd():
    """
    Find all existing foreign key constraints in the current schema.
    This feature is powered by dnikma's Foreign Key Detection (fkD) algorithm.
    --------------------------------------------------------------------------------------------------------------------
    """

    query = query_page.text

    ctx = context.get_context()
    verbose = ctx.args.verbose
    db = ctx.obj.get('mysql')

    verify_db(db)

    curs = db.query(query, verbose)
    r = curs.fetchall()

    dicprint_table(r, ["column_name", "table_name", "data_type"])
