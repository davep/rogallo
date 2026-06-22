"""Provides code for saving and loading the location history."""

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from datetime import datetime
from json import dumps, loads
from pathlib import Path
from typing import Self

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
# Local imports.
from ...history import RecencyHistory
from ..types import GeminiLocation
from .locations import data_dir


##############################################################################
@dataclass
class LocationVisit:
    """A record of a visit to a location."""

    location: GeminiLocation
    """The location that was visited."""

    timestamp: datetime = field(default_factory=datetime.now)
    """The timestamp of the visit."""

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, LocationVisit):
            return self.location == value.location
        return NotImplemented


##############################################################################
class LocationHistory(RecencyHistory[LocationVisit]):
    """The location history."""

    def add(self, item: LocationVisit) -> Self:
        """Add a visit to the history.

        Args:
            item: The visit to add.
        """
        return super().add(item)


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
                {
                    "type": "uri" if isinstance(entry.location, GeminiURI) else "path",
                    "location": str(entry.location),
                    "timestamp": entry.timestamp.isoformat(),
                }
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
            LocationVisit(
                (GeminiURI if entry["type"] == "uri" else Path)(entry["location"]),
                datetime.fromisoformat(entry["timestamp"]),
            )
            for entry in loads(history.read_text(encoding="utf-8"))
        ]
        if (history := location_history_file()).exists()
        else []
    )


### location_history.py ends here
