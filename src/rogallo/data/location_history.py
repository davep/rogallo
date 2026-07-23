"""Provides code for saving and loading the location history."""

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from datetime import datetime
from json import dumps, loads
from pathlib import Path
from typing import Self

##############################################################################
# BagOfStuff imports.
from bagofstuff.history import RecencyHistory

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
@dataclass(frozen=True)
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

    @property
    def as_json(self) -> dict[str, str]:
        """Get the visit as a JSON-serialisable dictionary.

        Returns:
            The visit as a JSON-serialisable dictionary.
        """
        return {
            "location": str(self.location),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_json(cls, data: dict[str, str]) -> Self:
        """Create a visit from a JSON-serialisable dictionary.

        Args:
            data: The JSON-serialisable dictionary.

        Returns:
            The visit.
        """
        return cls(
            make_location(data["location"]),
            datetime.fromisoformat(data["timestamp"]),
        )


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
        dumps([entry.as_json for entry in history], indent=4),
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
            LocationVisit.from_json(entry)
            for entry in loads(history.read_text(encoding="utf-8"))
        ]
        if (history := location_history_file()).exists()
        else []
    )


### location_history.py ends here
