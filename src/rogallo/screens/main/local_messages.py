"""Message that are purely local to the main screen."""

##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
# Textual imports.
from textual.message import Message

##############################################################################
# Local imports.
from ...document import Document
from ...types import RogalloLocation


##############################################################################
@dataclass
class OpenDocument(Message):
    """Open the given document for viewing."""

    document: Document
    """The document to open."""
    from_history: bool = False
    """Whether this document was opened from history."""


##############################################################################
@dataclass
class OpenUnsupportedURI(Message):
    """Open the given location in an external application."""

    uri: str
    """The unsupported URI to open."""


##############################################################################
@dataclass
class OpenUnsupportedMIMEType(Message):
    """Open the given location in an external application."""

    location: RogalloLocation
    """The unsupported location to open."""
    mime_type: str
    """The unsupported MIME type of the location."""


### local_messages.py ends here
