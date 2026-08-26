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
class ChangeCommandLineLocation(Command):
    """Swap the position of the command line between top and bottom"""

    BINDING_KEY = "ctrl+up, ctrl+down"


##############################################################################
class ToggleSidePanel(Command):
    """Toggle the visibility of the side panel"""

    BINDING_KEY = "ctrl+l"


##############################################################################
class StripeLinks(Command):
    """Toggle the striping of links in the document viewer"""

    BINDING_KEY = "f8"


##############################################################################
class ToggleLinkNumbers(Command):
    """Toggle the display of link numbers in the document viewer"""

    BINDING_KEY = "shift+f8"


##############################################################################
class ToggleCosyLinkNumbers(Command):
    """Toggle the position of link numbers when they're being displayed"""

    BINDING_KEY = "super+f8"


##############################################################################
class ToggleEmojiRemoval(Command):
    """Toggle the removal of emoji from text content"""

    BINDING_KEY = "f6"


##############################################################################
class ToggleANSIEscapeSequenceHandling(Command):
    """Toggle the handling of ANSI escape sequences in text content"""

    BINDING_KEY = "shift+f6"
    ACTION = "toggle_ansi_escape_sequence_handling_command"


### ui.py ends here
