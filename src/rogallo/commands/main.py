"""Main commands for the application."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class JumpToCommandLine(Command):
    """Jump to the command line"""

    BINDING_KEY = "/, ctrl+1"


##############################################################################
class JumpToDocument(Command):
    """Jump to the document viewer"""

    BINDING_KEY = "ctrl+slash, ctrl+g, ctrl+2"


##############################################################################
class ChangeCommandLineLocation(Command):
    """Swap the position of the command line between top and bottom"""

    BINDING_KEY = "ctrl+up, ctrl+down"


##############################################################################
class ToggleHistory(Command):
    """Toggle the display of the history viewer"""

    BINDING_KEY = "f2, ctrl+3"
    SHOW_IN_FOOTER = True
    FOOTER_TEXT = "History"


##############################################################################
class Reload(Command):
    """Reload the current document"""

    BINDING_KEY = "ctrl+r, f5"


##############################################################################
class ToggleView(Command):
    """Toggle between rendered and source view of the document"""

    BINDING_KEY = "f3"


##############################################################################
class GoHome(Command):
    """Go to the home page"""

    BINDING_KEY = "ctrl+h"


##############################################################################
class SetHomeToCurrentLocation(Command):
    """Set the home page to the current location"""

    BINDING_KEY = "ctrl+shift+h"


### main.py ends here
