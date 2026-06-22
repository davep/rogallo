"""Provides a simple history class."""

##############################################################################
# Python imports.
from collections import deque
from collections.abc import Iterator, Sequence
from typing import Self

##############################################################################
# Textual imports.
from textual.geometry import clamp


##############################################################################
class SimpleHistory[T]:
    """A history class that implements a linear history."""

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

    @property
    def current_location(self) -> int | None:
        """The current integer location in the history.

        If there is no valid location the value is `None`.
        """
        try:
            _ = self._history[self._current_index]
        except IndexError:
            return None
        return self._current_index

    @property
    def current_item(self) -> T | None:
        """The current item in the history.

        If there is no current item in the history the value is `None`.
        """
        try:
            return self._history[self._current_index]
        except IndexError:
            return None

    @property
    def can_go_backward(self) -> bool:
        """Can history go backward?"""
        return bool(self._current_index)

    def backward(self) -> bool:
        """Go backward through the history.

        Returns:
            `True` if we moved through history, `False` if not.
        """
        if self.can_go_backward:
            self._current_index -= 1
            return True
        return False

    @property
    def can_go_forward(self) -> bool:
        """Can history go forward?"""
        return self._current_index < len(self._history) - 1

    def forward(self) -> bool:
        """Go forward through the history.

        Returns:
            `True` if we moved through history, `False` if not.
        """
        if self.can_go_forward:
            self._current_index += 1
            return True
        return False

    def goto(self, location: int) -> Self:
        """Jump to a specific location within history."""
        self._current_index = clamp(location, 0, len(self._history) - 1)
        return self

    def goto_end(self) -> Self:
        """Go to the end of the history."""
        self.goto(len(self) - 1)
        return self

    def add(self, item: T) -> Self:
        """Add an item to the history.

        Args:
            item: The item to add.

        Returns:
            Self.

        Note:
            When adding an item to the history, everything after the current
            location is removed from the history, and the new item is placed
            at the end.
        """
        self._history.append(item)
        return self.goto_end()

    def __len__(self) -> int:
        """The length of the history."""
        return len(self._history)

    def __iter__(self) -> Iterator[T]:
        """Support iterating through the history."""
        return iter(self._history)


### simple.py ends here
