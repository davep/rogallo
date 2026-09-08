"""Provides the protocol for searchable widgets."""

##############################################################################
# Python imports.
from typing import Final, Protocol, runtime_checkable

##############################################################################
# Textual imports.
from textual.geometry import Region

##############################################################################
NEEDLE: Final[str] = "searchable-widget--needle"
"""The CSS class name for the search needle."""


##############################################################################
@runtime_checkable
class Searchable(Protocol):
    """A protocol for searchable widgets."""

    def find_reset(self) -> None:
        """Reset the search state of the widget."""
        ...

    def find_next_text(self, text: str) -> bool:
        """Get the text to be searched in the widget.

        Returns:
            `True` if the text was found, `False` otherwise.
        """
        ...

    def found_region(self) -> Region:
        """Get the region of the found text in the widget.

        Returns:
            The region of the found text, or the widget's region.
        """
        ...


### searchable.py ends here
