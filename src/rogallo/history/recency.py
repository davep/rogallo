"""Provides a recency history class."""

##############################################################################
# Python imports.
from collections import deque
from collections.abc import Iterator, Sequence
from typing import Self


##############################################################################
class RecencyHistory[T]:
    """A history that keeps track of the most recent items.

    The history attempts to stay unique, so if an item is added that already
    exists in the history, it is moved to the end of the history. Already
    existing is defined by an item that has equality to an item that already
    exists in the history.
    """

    def __init__(
        self, history: Sequence[T] | None = None, max_length: int = 500
    ) -> None:
        """Initialise the history object.

        Args:
            history: Set to the given history.
            max_length: Optional maximum length for the history.
        """
        self._history: deque[T] = deque(history or [], maxlen=max_length)
        """The history."""
        self._current_index = max(len(self._history) - 1, 0)
        """The current index in the history."""

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
        self._history.append(item)
        return self

    def __len__(self) -> int:
        """The length of the history."""
        return len(self._history)

    def __iter__(self) -> Iterator[T]:
        """Support iterating through the history."""
        return iter(self._history)


### recency.py ends here
