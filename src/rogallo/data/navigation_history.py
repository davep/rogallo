"""Provides code for saving and loading the navigation history."""

##############################################################################
# Python imports.
from json import dumps, loads
from pathlib import Path
from typing import NamedTuple

##############################################################################
# BagOfStuff imports.
from bagofstuff.history import NavigableHistory

##############################################################################
# Local imports.
from ..preflight import make_location
from ..types import RogalloLocation
from .locations import data_dir


##############################################################################
class NavigationPosition(NamedTuple):
    """A position in the navigation history."""

    location: RogalloLocation
    """The location at the position in the history."""

    focused_link: int | None = None
    """The index of the position in the history."""


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
        dumps(
            [
                {
                    "location": str(entry.location),
                    "focused_link": entry.focused_link,
                }
                for entry in history
            ],
            indent=4,
        ),
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
            NavigationPosition(
                make_location(entry["location"]),
                entry.get("focused_link"),
            )
            for entry in loads(history.read_text(encoding="utf-8"))
        ]
        if (history := navigation_history_file()).exists()
        else []
    )


### navigation_history.py ends here
