"""
The entry point and feature configurations for the 'connect' command, to handle connections to database instances.
"""
import click


@click.command('connect')
@click.argument('connection_string')
def connect_mysql(connection_string):
    """
    Connect to specified MySQL instance using a connection string.
    Any subsequent commands are dependent on an active MySQL connection.

    CONNECTION_STRING should be a valid MySQL connection string in the format:
    Server=myServerAddress;Database=myDatabase;Uid=myUsername;Pwd=myPassword;
    """
    click.echo("Attempting to connect to your MySQL instance at: " + connection_string)
