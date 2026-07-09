"""Messages for opening things."""

##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
# Textual imports.
from textual.message import Message

##############################################################################
# Local imports.
from ..document import Document
from ..types import GeminiLocation


##############################################################################
@dataclass
class OpenURI(Message):
    """Open a given URI for viewing."""

    uri: str
    """The URI to open."""


##############################################################################
@dataclass
class OpenLocation(Message):
    """Open a given location for viewing."""

    location: GeminiLocation
    """The location to open."""
    from_history: bool = False
    """Whether the location is being opened from history."""


##############################################################################
@dataclass
class OpenDocument(Message):
    """Open the given document for viewing."""

    document: Document
    """The document to open."""
    original_request: OpenLocation
    """The original request that led to this text being opened."""
    originally_from: GeminiLocation
    """The location the text was originally from, if any."""


### opening.py ends here
