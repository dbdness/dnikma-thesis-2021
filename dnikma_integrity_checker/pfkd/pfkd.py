"""
The entry point and feature configurations for the Potential Foreign Key Detection, 'pfkd', command.
"""
import click


@click.command('pfkd')
@click.option('--name-like-id', is_flag=True,
              help="Consider only columns with a name pattern like “%id%” as potential foreign keys.")
def pfkd(name_like_id):
    """
    Find potential foreign key combinations in the current schema.
    This feature is powered by dnikma's Potential Foreign Key Detection (PfkD) algorithm.

    DISCLAIMER: Results may vary between different schemas. Please validate the outcome before applying it.
    """
    if name_like_id:
        click.echo("I will soon find potential foreign keys with %id% name pattern...")
        __f_name_like_id()
    else:
        click.echo("I will soon perform pfkd queries...")
        click.echo("Try running me with --name-like-id to see an example of a flag.")


def __f_name_like_id():
    pass
