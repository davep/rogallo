"""Provides code for loading the Gopher configuration."""

##############################################################################
# Future imports.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import asdict, dataclass, field
from functools import cache
from typing import TypedDict, cast

##############################################################################
# GopherMap imports.
from gophermap import ItemType

##############################################################################
# Local imports.
from ._loader import load_configuration

##############################################################################
type GopherTypeBadges = dict[str, str]
"""Type for Gopher type badges."""


##############################################################################
class GopherConfigurationData(TypedDict):
    """The shape of the Gopher configuration data."""

    show_type_badges: bool
    """Whether to show type badges in the Gopher view."""
    type_badges: GopherTypeBadges
    """The type badges to use in the Gopher view."""


##############################################################################
@dataclass(frozen=True)
class GopherConfiguration:
    """Gopher configuration."""

    show_type_badges: bool = True
    """Whether to show type badges in the Gopher view."""
    type_badges: GopherTypeBadges = field(
        default_factory=lambda: {
            ItemType.TEXT.value: "📄",
            ItemType.MENU.value: "📁",
            ItemType.CSO.value: "📇",
            ItemType.ERROR.value: "❌",
            ItemType.BINHEX.value: "📦",
            ItemType.DOS_FILE.value: "💾",
            ItemType.UUENCODED.value: "📜",
            ItemType.INDEX_SEARCH.value: "🔍",
            ItemType.TELNET.value: "🖥️",
            ItemType.BINARY.value: "📦",
            ItemType.INFO.value: "ℹ️",
            ItemType.GIF.value: "🖼️",
            ItemType.IMAGE.value: "🖼️",
            ItemType.HTML.value: "🌐",
            ItemType.DOCUMENT.value: "📄",
            ItemType.AUDIO.value: "🎵",
            ItemType.PDF.value: "📄",
            ItemType.XML.value: "📄",
            ItemType.UNKNOWN.value: "❓",
        }
    )
    """The type badges to use in the Gopher view."""

    @classmethod
    def from_dict(cls, data: GopherConfigurationData) -> GopherConfiguration:
        """Load a Gopher configuration from a dictionary.

        Args:
            data: The data to load from.

        Returns:
            A fresh instance of a Gopher configuration.
        """
        return cls(
            show_type_badges=data.get("show_type_badges", True),
            type_badges=data.get("type_badges", {}),
        )


##############################################################################
@cache
def load_gopher() -> GopherConfiguration:
    """Load the Gopher configuration.

    Returns:
        The loaded Gopher configuration.
    """
    return GopherConfiguration.from_dict(
        cast(
            GopherConfigurationData,
            load_configuration("gopher", asdict(GopherConfiguration())),
        )
    )


### gopher.py ends here
