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
class JumpToSidebar(Command):
    """Jump to the sidebar"""

    BINDING_KEY = "ctrl+3"


##############################################################################
class ChangeCommandLineLocation(Command):
    """Swap the position of the command line between top and bottom"""

    BINDING_KEY = "ctrl+up, ctrl+down"


##############################################################################
class ToggleHistoryManager(Command):
    """Toggle the display of the history viewer"""

    BINDING_KEY = "shift+f2"


##############################################################################
class ToggleBookmarksManager(Command):
    """Toggle the display of the bookmarks viewer"""

    BINDING_KEY = "shift+f3"


##############################################################################
class ToggleClientCertificateManager(Command):
    """Toggle the display of the client certificate manager"""

    BINDING_KEY = "shift+f4"


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
