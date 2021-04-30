"""
The entry point and feature configurations for the Primary Key Detection, 'pkd', command.
"""
import requests
from nubia import command, context

from dnikma_integrity_checker.helpers.utils import dicprint_table, db_ok

query_page = requests.get(
    "https://raw.githubusercontent.com/dbdness/dnikma-thesis-2021/master/sql-queries/pkd.sql?token=ACJ6L5I6QQJCQIEZQU2LBS3ASW3SY")


@command('pkd')
def pkd():
    """
    Find all existing primary key constraints in the current schema.
    This feature is powered by dnikma's Primary Key Detection (pkD) algorithm.
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

    dicprint_table(r, ["column_name", "table_name", "data_type"])
