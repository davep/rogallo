"""Provides a widget to show a label and a value."""

##############################################################################
# Python imports.
from collections.abc import Iterator
from typing import Self

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Label


##############################################################################
class Data(HorizontalGroup):
    """A widget to show a label and a value."""

    DEFAULT_CSS = """
    Data {
        height: 1;
        width: auto;
        #label {
            text-style: bold;
            color: $text-accent;
            padding-right: 1;
        }
    }
    """

    def __init__(self, label: str, value: str | bool) -> None:
        """Initialise the widget."""
        super().__init__()
        self._data_label = label
        """The label of the data."""
        self._data_value = (
            value if isinstance(value, str) else ("Yes" if value else "No")
        )
        """The value of the data."""

    def compose(self) -> ComposeResult:
        """Compose the widget."""
        yield Label(f"{self._data_label}:", id="label")
        yield Label(self._data_value, id="value", markup=False)

    @classmethod
    def maybe(cls, label: str, value: str | bool | None) -> Iterator[Self]:
        """Yield a `Data` widget if there's something to show.

        Args:
            label: The label of the data.
            value: The value of the data.

        Yields:
            A `Data` widget if there is something to show.
        """
        if value is None or (isinstance(value, str) and not value):
            return
        yield cls(label, value)


### data.py ends here
