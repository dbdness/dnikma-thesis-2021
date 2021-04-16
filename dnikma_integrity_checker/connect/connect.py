import click


@click.command('connect')
@click.argument('connection_string')
def connect_mysql(connection_string):
    click.echo("Attempting to connect to your MySQL instance at: " + connection_string)
