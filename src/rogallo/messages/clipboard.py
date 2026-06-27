"""messages relating to the clipboard."""

##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
# Textual imports.
from textual.message import Message


##############################################################################
@dataclass
class CopyToClipboard(Message):
    """Request that some text is copied to the clipboard."""

    text: str
    """The text to copy to the clipboard."""
    description: str | None = None
    """A description of the text to copy to the clipboard."""


### clipboard.py ends here
