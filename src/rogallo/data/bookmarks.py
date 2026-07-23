"""provides code for saving and loading the bookmarks."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from functools import total_ordering
from json import dumps, loads
from pathlib import Path

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
@total_ordering
class Bookmark:
    """A bookmark."""

    title: str
    """The bookmark's title."""

    location: GeminiLocation
    """The location of the bookmark."""

    @property
    def as_json(self) -> dict[str, str]:
        """The bookmark in a JSON-friendly format."""
        return {
            "title": self.title,
            "location": str(self.location),
        }

    @classmethod
    def from_json(cls, data: dict[str, str]) -> Bookmark:
        """Load a bookmark from some JSON data.

        Args:
            data: The data to load from.

        Returns:
            A fresh instance of a bookmark.
        """
        return cls(
            data.get("title", ""),
            make_location(data.get("location", "")),
        )

    def __gt__(self, other: object, /) -> bool:
        if isinstance(other, Bookmark):
            return self.title > other.title
        return NotImplemented

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Bookmark):
            return self.location == other.location
        if isinstance(other, str):
            return self.title.casefold() == other.casefold()
        if isinstance(other, Path):
            return isinstance(self.location, Path) and self.location == other
        if isinstance(other, GeminiURI):
            return isinstance(self.location, GeminiURI) and self.location == other
        if isinstance(other, FingerURI):
            return isinstance(self.location, FingerURI) and self.location == other
        return NotImplemented


##############################################################################
type Bookmarks = list[Bookmark]
"""Type of a list of bookmarks."""


##############################################################################
def bookmarks_file() -> Path:
    """The path of the bookmarks file.

    Returns:
        The path for the bookmarks file.
    """
    return data_dir() / "bookmarks.json"


##############################################################################
def save_bookmarks(bookmarks: Bookmarks) -> None:
    """Save the bookmarks to storage.

    Args:
        bookmarks: The bookmarks to save.
    """
    bookmarks_file().write_text(
        dumps([bookmark.as_json for bookmark in bookmarks], indent=4), encoding="utf-8"
    )


##############################################################################
def load_bookmarks() -> Bookmarks:
    """Load bookmarks from storage.

    Returns:
        The bookmarks.
    """
    return (
        [
            Bookmark.from_json(data)
            for data in loads(bookmarks_file().read_text(encoding="utf-8"))
        ]
        if bookmarks_file().exists()
        else []
    )


### bookmarks.py ends here
