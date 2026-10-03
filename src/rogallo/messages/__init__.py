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
    DownloadLocation,
    DownloadURI,
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
    "DownloadLocation",
    "DownloadURI",
    "HistoryModified",
    "OpenFromFileSystem",
    "OpenLocation",
    "OpenURI",
]


### __init__.py ends here
