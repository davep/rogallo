"""Provides code for saving and loading the location history."""

##############################################################################
# Python imports.
from json import dumps, loads
from pathlib import Path

##############################################################################
# Textual enhanced imports.
from textual_enhanced.tools import History

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
# Local imports.
from ..types import GeminiLocation
from .locations import data_dir


##############################################################################
class LocationHistory(History[GeminiLocation]):
    """The location history."""


##############################################################################
def location_history_file() -> Path:
    """Get the path for the location history file.

    Returns:
        The path for the location history file.
    """
    return data_dir() / "location-history.json"


##############################################################################
def save_location_history(history: LocationHistory) -> None:
    """Save the location history to storage.

    Args:
        history: The location history to save.
    """
    location_history_file().write_text(
        dumps(
            [
                ("uri" if isinstance(entry, GeminiURI) else "path", str(entry))
                for entry in history
            ],
            indent=4,
        ),
        encoding="utf-8",
    )


##############################################################################
def load_location_history() -> LocationHistory:
    """Load the location history from storage.

    Returns:
        The location history.
    """
    return LocationHistory(
        [
            (GeminiURI if entry_type == "uri" else Path)(entry)
            for entry_type, entry in loads(history.read_text(encoding="utf-8"))
        ]
        if (history := location_history_file()).exists()
        else []
    )


### location_history.py ends here
