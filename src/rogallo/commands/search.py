"""Commands for searching for locations."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class SearchHistory(Command):
    """Search the history for a location"""

    BINDING_KEY = "f6"


##############################################################################
class SearchBookmarks(Command):
    """Search the bookmarks for a location"""

    BINDING_KEY = "f7"


### search.py ends here
