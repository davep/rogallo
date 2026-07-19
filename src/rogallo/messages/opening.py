"""Messages for opening things."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from pathlib import Path

##############################################################################
# Textual imports.
from textual.message import Message

##############################################################################
# Local imports.
from ..document import Document
from ..input_content import InputContent
from ..types import GeminiLocation


##############################################################################
@dataclass
class OpenURI(Message):
    """Open a given URI for viewing."""

    uri: str
    """The URI to open."""
    allow_cached: bool = True
    """Whether to allow opening the URI from cache."""


##############################################################################
@dataclass
class OpenLocation(Message):
    """Open a given location for viewing."""

    location: GeminiLocation
    """The location to open."""
    do_not_record_in_history: bool = False
    """Whether we should avoid recording this in history."""
    allow_cached: bool = True
    """Whether to allow opening the location from cache."""
    associated_input: InputContent | None = None
    """The input content associated with this location, if any."""


##############################################################################
@dataclass
class OpenDocument(Message):
    """Open the given document for viewing."""

    document: Document
    """The document to open."""
    original_request: OpenLocation
    """The original request that led to this text being opened."""


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

    location: GeminiLocation
    """The unsupported location to open."""
    mime_type: str
    """The unsupported MIME type of the location."""


##############################################################################
@dataclass
class OpenFromFileSystem(Message):
    """Browse for a file to view, from the local filesystem."""

    start_from: Path = Path(".")
    """The path to start browsing from."""


### opening.py ends here
