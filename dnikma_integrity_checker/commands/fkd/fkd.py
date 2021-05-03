"""
The entry point and feature configurations for the Foreign Key Detection, 'fkd', command.
"""
import requests
from nubia import command, context

from dnikma_integrity_checker.helpers.utils import dicprint_table, db_ok

query_page = requests.get(
    "https://raw.githubusercontent.com/dbdness/dnikma-thesis-2021/master/sql-queries/fkd.sql?token=ACJ6L5K7EJ3D7PC5NOYM2Q3ASW3UK")


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

    if not db_ok(db):
        return

    curs = db.query(query, verbose)
    r = curs.fetchall()

    dicprint_table(r, ["table_name", "constraint_name"])
