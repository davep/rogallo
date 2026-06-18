"""Main commands for the application."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class ChangeCommandLineLocation(Command):
    """Swap the position of the command line between top and bottom"""

    BINDING_KEY = "ctrl+up, ctrl+down"


### main.py ends here
