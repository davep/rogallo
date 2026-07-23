"""Provides code for saving and loading the navigation history."""

##############################################################################
# Python imports.
from json import dumps, loads
from pathlib import Path
from typing import Any

##############################################################################
# BagOfStuff imports.
from bagofstuff.history import NavigableHistory

##############################################################################
# Port79 imports.
from port79 import FingerURI

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
# Local imports.
from ..preflight import is_finger_uri, is_gemini_uri, make_location
from ..types import GeminiLocation
from .locations import data_dir


##############################################################################
class NavigationHistory(NavigableHistory[GeminiLocation]):
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
                    "location": str(entry),
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
            make_location(entry["location"])
            for entry in loads(history.read_text(encoding="utf-8"))
        ]
        if (history := navigation_history_file()).exists()
        else []
    )


### navigation_history.py ends here
