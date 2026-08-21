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
from ..input_content import InputContent
from ..types import RogalloLocation


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

    location: RogalloLocation
    """The location to open."""
    avoid_history: bool = False
    """Whether we should avoid recording this in history."""
    from_history: bool = False
    """Whether this request came from navigating history."""
    allow_cached: bool = True
    """Whether to allow opening the location from cache."""
    associated_input: InputContent | None = None
    """The input content associated with this location, if any."""


##############################################################################
@dataclass
class OpenFromFileSystem(Message):
    """Browse for a file to view, from the local filesystem."""

    start_from: Path = Path(".")
    """The path to start browsing from."""


### opening.py ends here
