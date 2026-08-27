"""Provides application-wide messages."""

##############################################################################
# Local imports.
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
    "ClientCertificatesModified",
    "HistoryModified",
    "OpenFromFileSystem",
    "OpenLocation",
    "OpenURI",
]


### __init__.py ends here
