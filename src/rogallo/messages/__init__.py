"""Provides application-wide messages."""

##############################################################################
# Local imports.
from .clipboard import CopyToClipboard
from .opening import (
    OpenDocument,
    OpenFromFileSystem,
    OpenLocation,
    OpenUnsupportedMIMEType,
    OpenUnsupportedURI,
    OpenURI,
)

##############################################################################
# Exports.
__all__ = [
    "CopyToClipboard",
    "OpenDocument",
    "OpenFromFileSystem",
    "OpenLocation",
    "OpenUnsupportedMIMEType",
    "OpenUnsupportedURI",
    "OpenURI",
]


### __init__.py ends here
