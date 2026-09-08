"""Provides the protocol for searchable Gemtext widgets."""

##############################################################################
# Python imports.
from typing import Final, Protocol, runtime_checkable

##############################################################################
NEEDLE: Final[str] = "gemtext--needle"
"""The CSS class name for the search needle."""


##############################################################################
@runtime_checkable
class Searchable(Protocol):
    """A protocol for searchable Gemtext widgets."""

    def find_reset(self) -> None:
        """Reset the search state of the widget."""
        ...

    def find_next_text(self, text: str) -> bool:
        """Get the text to be searched in the widget.

        Returns:
            `True` if the text was found, `False` otherwise.
        """
        ...


### searchable.py ends here
