"""Main commands for the application."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class Reload(Command):
    """Reload the current document"""

    BINDING_KEY = "ctrl+r, f5"


##############################################################################
class ToggleView(Command):
    """Toggle between rendered and source view of the document"""

    BINDING_KEY = "f4"


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
class AboutThisPage(Command):
    """Show information about the current page"""

    BINDING_KEY = "f7"


##############################################################################
class PipeDocument(Command):
    """Pipe the current document to an external command"""

    BINDING_KEY = "ctrl+shift+p"


##############################################################################
class ViewChangeLog(Command):
    """View the Rogallo ChangeLog"""

    BINDING_KEY = "ctrl+shift+l"


##############################################################################
class HandOffToOperatingSystem(Command):
    """Hand off the current location to the operating system"""

    BINDING_KEY = "ctrl+shift+o"


##############################################################################
class SaveSource(Command):
    """Save the source of the current document to a file"""

    BINDING_KEY = "ctrl+s"


### main.py ends here
