"""Provides a class for holding a user's input content."""

##############################################################################
# Python imports.
from typing import NamedTuple

##############################################################################
# Wasat imports.
from wasat import GeminiURI


##############################################################################
class InputContent(NamedTuple):
    """A class for holding a user's input content."""

    location: GeminiURI
    """The location that the input was requested from."""
    prompt: str
    """The prompt that was shown to the user."""
    sensitive: bool = False
    """Whether the input is sensitive (e.g. a password)."""
    content: str = ""
    """The content of the input."""

    def __eq__(self, other: object, /) -> bool:
        """Check if two InputContent objects are equal."""
        if isinstance(other, InputContent):
            return (
                self.location == other.location
                and self.prompt == other.prompt
                and self.sensitive == other.sensitive
            )
        return NotImplemented


### input_content.py ends here
