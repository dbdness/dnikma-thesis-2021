"""
The entry point and feature configurations for the 'connect' command, to handle connections to database instances.
"""
import click
import mysql.connector


@click.command('connect')
@click.argument('connection_string')
def connect_mysql(connection_string: str):
    """
    Connect to specified MySQL instance using a connection string.
    Any subsequent commands are dependent on an active MySQL connection.

    CONNECTION_STRING should be a valid MySQL connection string in the format:
    "host=myHostAddress;database=myDatabase;user=myUsername;password=myPassword;"
    """
    if connection_string.startswith("'") or connection_string.endswith("'"):
        click.echo('Please use double quotes (") instead of single quotes to enclose the connection string.')
        return
    parsed = __parse_conn_str(connection_string)
    click.echo("Parsed the following connection details:")
    redacted = parsed.copy()
    redacted['password'] = '*****'
    click.echo(redacted)
    click.echo("Attempting to connect to MySQL instance supplied...")

    try:
        cnx = mysql.connector.connect(**parsed)
        cur = cnx.cursor()
        cur.execute("SELECT CURDATE()")
        click.echo("Success! Connection established.")
        cnx.close()
    except Exception as ex:
        click.echo("Failed. A connection error occurred:")
        click.echo('"{}"'.format(ex))
        click.echo("Please verify the specified connection string.")


def __parse_conn_str(conn_string: str):
    params = dict(entry.split('=') for entry in conn_string.split(';') if entry)
    return params
