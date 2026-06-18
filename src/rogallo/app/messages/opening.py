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
class OpenLocation(Message):
    """Open a given location for viewing."""

    to_open: GeminiLocation
    """The location to open."""


### opening.py ends here
