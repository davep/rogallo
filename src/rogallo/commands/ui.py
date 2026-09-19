"""Provides commands related to the user interface."""

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
class JumpToSidePanel(Command):
    """Jump to the side panel"""

    BINDING_KEY = "ctrl+3"


##############################################################################
class ToggleSidePanel(Command):
    """Toggle the visibility of the side panel"""

    BINDING_KEY = "ctrl+l"


##############################################################################
class ToggleCosyLinkNumbers(Command):
    """Toggle the position of link numbers when they're being displayed"""

    BINDING_KEY = "super+f8"


### ui.py ends here
