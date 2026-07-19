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
class Reload(Command):
    """Reload the current document"""

    BINDING_KEY = "ctrl+r, f5"


##############################################################################
class ToggleView(Command):
    """Toggle between rendered and source view of the document"""

    BINDING_KEY = "f4"


##############################################################################
class GoHome(Command):
    """Go to the home page"""

    BINDING_KEY = "ctrl+h"


##############################################################################
class SetHomeToCurrentLocation(Command):
    """Set the home page to the current location"""

    BINDING_KEY = "ctrl+shift+h"


##############################################################################
class SetHome(Command):
    """Set the home page to a specific location"""

    BINDING_KEY = "alt+h"


##############################################################################
class AddLocationToBookmarks(Command):
    """Add the current location to the bookmarks"""

    BINDING_KEY = "ctrl+b"


##############################################################################
class ClearCache(Command):
    """Clear the cache for all content"""

    BINDING_KEY = "shift+f5"


##############################################################################
class StripeLinks(Command):
    """Toggle the striping of links in the document viewer"""

    BINDING_KEY = "f8"


##############################################################################
class ToggleLinkNumbers(Command):
    """Toggle the display of link numbers in the document viewer"""

    BINDING_KEY = "shift+f8"


##############################################################################
class ToggleEmojiRemoval(Command):
    """Toggle the removal of emoji from text content"""

    BINDING_KEY = "f6"


##############################################################################
class ToggleANSIEscapeSequenceHandling(Command):
    """Toggle the handling of ANSI escape sequences in text content"""

    BINDING_KEY = "shift+f6"
    ACTION = "toggle_ansi_escape_sequence_handling_command"


### main.py ends here
