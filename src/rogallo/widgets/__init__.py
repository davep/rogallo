"""Provides widgets for the application."""

##############################################################################
# Local imports.
from .bookmarks import BookmarksViewer
from .command_line import CommandLine
from .history import HistoryViewer
from .toolbar import Toolbar
from .viewer import Viewer

##############################################################################
# Exports.
__all__ = ["BookmarksViewer", "CommandLine", "HistoryViewer", "Toolbar", "Viewer"]


### __init__.py ends here
