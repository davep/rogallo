"""Main commands for the application."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class JumpToCommandLine(Command):
    """Jump to the command line"""

    BINDING_KEY = "/"


##############################################################################
class JumpToDocument(Command):
    """Jump to the markdown document"""

    BINDING_KEY = "ctrl+slash, ctrl+g"


##############################################################################
class ChangeCommandLineLocation(Command):
    """Swap the position of the command line between top and bottom"""

    BINDING_KEY = "ctrl+up, ctrl+down"


##############################################################################
class ToggleHistory(Command):
    """Toggle the display of the history viewer"""

    BINDING_KEY = "f2"
    SHOW_IN_FOOTER = True
    FOOTER_TEXT = "History"


### main.py ends here
