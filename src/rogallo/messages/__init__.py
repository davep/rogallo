"""Provides application-wide messages."""

##############################################################################
# Local imports.
from .clipboard import CopyToClipboard
from .data_modification import (
    BookmarksModified,
    ClientCertificatesModified,
    HistoryModified,
)
from .opening import (
    OpenFromFileSystem,
    OpenLocation,
    OpenURI,
)

##############################################################################
# Exports.
__all__ = [
    "BookmarksModified",
    "CopyToClipboard",
    "ClientCertificatesModified",
    "HistoryModified",
    "OpenFromFileSystem",
    "OpenLocation",
    "OpenURI",
]


### __init__.py ends here
