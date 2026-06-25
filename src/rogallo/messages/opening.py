"""Messages for opening things."""

##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
# Textual imports.
from textual.message import Message

##############################################################################
# Local imports.
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
class OpenText(Message):
    """Open the given text for viewing."""

    text: str
    """The text to open."""
    originally_from: GeminiLocation | None = None
    """The location the text was originally from, if any."""


### opening.py ends here
