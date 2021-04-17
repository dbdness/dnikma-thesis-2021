"""
Very simple command to display a banner along with information on the tool.
Due to the simplicity of this command, it is not created as its own module.
"""
import click

from .banner import banner


@click.command()
def about():
    """
    About this tool.

    Display a welcome message containing relevant information on the tool.
    """
    click.echo(banner)
    click.echo("\n")
    click.echo("Welcome to the dnikma MySQL Integrity Checker.")
    click.echo("This tool has been developed as a part of Danny and Kim's 2021 thesis project at Roskilde University.")
    click.echo("Please refer to the GitHub repository for more details: https://github.com/dbdness/dnikma-thesis-2021")
