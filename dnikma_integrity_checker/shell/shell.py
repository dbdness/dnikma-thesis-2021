"""
This is the main entry point file for the tool.
This is where all appropriate CLI commands, feature flags etc. are defined.
Major commands and features should call functionality from the appropriate modules from the
parent package (dnikma_integrity_checker)
"""

import sys

from nubia import Nubia, Options

import dnikma_integrity_checker.commands as commands
from .configs.dic_plugin import DicPlugin


def entry_point():
    plugin = DicPlugin()
    shell = Nubia(
        name="dnikma MySQL Integrity Checker",
        command_pkgs=commands,
        plugin=plugin,
        options=Options(
            persistent_history=False, auto_execute_single_suggestions=False
        ),
    )
    sys.exit(shell.run())
