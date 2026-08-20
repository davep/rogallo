"""Provides code for saving and loading the navigation history."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from json import dumps, loads
from pathlib import Path
from typing import Any, Self

##############################################################################
# BagOfStuff imports.
from bagofstuff.history import NavigableHistory

##############################################################################
# Local imports.
from ..preflight import make_location
from ..types import RogalloLocation
from .locations import data_dir


##############################################################################
@dataclass(frozen=True)
class NavigationPosition:
    """A position in the navigation history."""

    location: RogalloLocation
    """The location at the position in the history."""

    focused_link: int | None = None
    """The index of the position in the history."""

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, NavigationPosition):
            return self.location == value.location
        return NotImplemented

    @property
    def as_json(self) -> dict[str, Any]:
        """Get the visit as a JSON-serialisable dictionary.

        Returns:
            The visit as a JSON-serialisable dictionary.
        """
        return {
            "location": str(self.location),
            "focused_link": self.focused_link,
        }

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        """Create a visit from a JSON-serialisable dictionary.

        Args:
            data: The JSON-serialisable dictionary.

        Returns:
            The visit.
        """
        return cls(
            make_location(str(data["location"])),
            data.get("focused_link"),
        )


##############################################################################
class NavigationHistory(NavigableHistory[NavigationPosition]):
    """The navigation history."""


##############################################################################
def navigation_history_file() -> Path:
    """Get the path for the navigation history file.

    Returns:
        The path for the navigation history file.
    """
    return data_dir() / "navigation-history.json"


##############################################################################
def save_naviagation_history(history: NavigationHistory) -> None:
    """Save the navigation history to storage.

    Args:
        history: The navigation history to save.
    """
    navigation_history_file().write_text(
        dumps([entry.as_json for entry in history], indent=4),
        encoding="utf-8",
    )


##############################################################################
def load_navigation_history() -> NavigationHistory:
    """Load the navigation history from storage.

    Returns:
        The navigation history.
    """
    return NavigationHistory(
        [
            NavigationPosition.from_json(entry)
            for entry in loads(history.read_text(encoding="utf-8"))
        ]
        if (history := navigation_history_file()).exists()
        else []
    )


### navigation_history.py ends here
