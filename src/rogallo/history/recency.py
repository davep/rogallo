"""Provides a recency history class."""

##############################################################################
# Python imports.
from collections.abc import Iterator
from typing import Self

##############################################################################
# Local imports.
from .simple import SimpleHistory


##############################################################################
class RecencyHistory[T](SimpleHistory[T]):
    """A history that keeps track of the most recent items.

    The history attempts to stay unique, so if an item is added that already
    exists in the history, it is moved to the end of the history. Already
    existing is defined by an item that has equality to an item that already
    exists in the history.
    """

    def add(self, item: T) -> Self:
        """Add an item to the history.

        Args:
            item: The item to add.

        Returns:
            Self.

        Note:
            When adding an item to the history, if the item already exists
            in the history, it is removed and added to the end of the history.
        """
        if item in self._history:
            self._history.remove(item)
        return super().add(item)


### recency.py ends here
