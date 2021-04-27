"""
Very simple command to display a banner along with information on the tool.
Due to the simplicity of this command, it is not created as its own module.
"""
from nubia import command
from termcolor import cprint

from dnikma_integrity_checker.helpers.banner import banner


@command()
def about():
    """
    About this tool.

    Display a welcome message containing relevant information on the tool.
    """
    cprint(banner)
    cprint("\n")
    cprint("Welcome to the dnikma MySQL Integrity Checker.")
    cprint("This tool has been developed as a part of Danny and Kim's 2021 thesis project at Roskilde University.")
    cprint("Please refer to the GitHub repository for more details: https://github.com/dbdness/dnikma-thesis-2021")
