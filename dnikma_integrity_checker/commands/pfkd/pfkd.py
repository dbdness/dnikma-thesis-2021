"""
The entry point and feature configurations for the Potential Foreign Key Detection, 'pfkd', command.
"""
from nubia import command, argument, context
from termcolor import cprint


@command('pfkd')
@argument('name_like_id',
          description="Consider only columns with a name pattern like “%id%” as potential foreign keys.",
          positional=False)
def pfkd(name_like_id=None):
    """
    Find potential foreign key combinations in the current schema.
    This feature is powered by dnikma's Potential Foreign Key Detection (PfkD) algorithm.

    DISCLAIMER: Results may vary between different schemas. Please validate the outcome before applying it.
    --------------------------------------------------------------------------------------------------------------------
    """
    if name_like_id:
        cprint("I will soon find potential foreign keys with %id% name pattern...")
        __f_name_like_id()
    else:
        ctx = context.get_context()
        db = ctx.obj['mysql']
        curs = db.query("SELECT * FROM employees LIMIT 1")
        r = curs.fetchone()
        cprint(str(r))


def __f_name_like_id():
    pass
