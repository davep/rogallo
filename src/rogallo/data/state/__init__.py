"""Provides code for managing the application's state data.

The data in this module is intended to be all the application-usage values
that will live in XDG_STATE_HOME.
"""

##############################################################################
# Local imports.
from .command_history import (
    CommandLineHistory,
    load_command_history,
    save_command_history,
)

##############################################################################
# Exports.
__all__ = [
    "CommandLineHistory",
    "load_command_history",
    "save_command_history",
]

### __init__.py ends here
