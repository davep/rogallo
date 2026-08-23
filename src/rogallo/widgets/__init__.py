"""Provides widgets for the application."""

##############################################################################
# Local imports.
from .bookmarks import BookmarksViewer
from .client_certificates import ClientCertificateManager
from .command_line import CommandLine
from .history import HistoryViewer
from .toolbar import Toolbar
from .viewer import Viewer

##############################################################################
# Exports.
__all__ = [
    "BookmarksViewer",
    "ClientCertificateManager",
    "CommandLine",
    "HistoryViewer",
    "Toolbar",
    "Viewer",
]


### __init__.py ends here
