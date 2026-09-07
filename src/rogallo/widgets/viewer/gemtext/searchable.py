"""Provides the protocol for searchable Gemtext widgets."""

##############################################################################
# Python imports.
from typing import Protocol, runtime_checkable


##############################################################################
@runtime_checkable
class Searchable(Protocol):
    """A protocol for searchable Gemtext widgets."""

    def find_next_text(self, text: str) -> bool:
        """Get the text to be searched in the widget.

        Returns:
            `True` if the text was found, `False` otherwise.
        """
        ...


### searchable.py ends here
