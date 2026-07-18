"""Commands for searching for locations."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class SearchHistory(Command):
    """Search the history for a location"""

    BINDING_KEY = "f2"
    SHOW_IN_FOOTER = True
    FOOTER_TEXT = "History"


##############################################################################
class SearchBookmarks(Command):
    """Search the bookmarks for a location"""

    BINDING_KEY = "f3"
    SHOW_IN_FOOTER = True
    FOOTER_TEXT = "Bookmarks"


### search.py ends here
