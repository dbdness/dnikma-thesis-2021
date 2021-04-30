"""
The entry point and feature configurations for the Primary Key Detection, 'pkd', command.
"""
import requests
from nubia import command, context

from dnikma_integrity_checker.helpers.utils import dicprint_table, verify_db

query_page = requests.get(
    "https://raw.githubusercontent.com/dbdness/dnikma-thesis-2021/master/sql-queries/subqueries/pkd.sql?token=ACJ6L5NMY4QFYNCZKXZ5VBTASWYUS")


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

    verify_db(db)

    curs = db.query(query, verbose)
    r = curs.fetchall()

    dicprint_table(r, ["column_name", "table_name", "data_type"])
