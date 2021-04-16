import click


@click.command('pfkd')
@click.option('--name-like-id', is_flag=True,
              help="Only include potential foreign key columns with a name pattern like “%id%”")
def pfkd(name_like_id):
    click.echo("I will soon perform pfkd queries.")
    if name_like_id:
        click.echo("Now starting to find potential foreign keys with %id% name pattern...")
        f_name_like_id()


def f_name_like_id():
    pass
