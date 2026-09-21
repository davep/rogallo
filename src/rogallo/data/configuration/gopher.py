"""Provides code for loading the Gopher configuration."""

##############################################################################
# Future imports.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from functools import cache, cached_property
from typing import Final

##############################################################################
# GopherMap imports.
from gophermap import ItemType

##############################################################################
# Local imports.
from ._io import load_configuration_into

##############################################################################
type BadgeMapping = dict[str, str]
"""A mapping of Gopher item types to their corresponding badge strings."""

##############################################################################
_DEFAULT_TYPE_BADGES: Final[BadgeMapping] = {
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
"""The default type badges to use in the Gopher view."""


##############################################################################
@dataclass(frozen=True)
class GopherConfiguration:
    """Gopher configuration."""

    show_type_badges: bool = True
    """Whether to show type badges in the Gopher view."""
    type_badges: BadgeMapping = field(
        default_factory=lambda: _DEFAULT_TYPE_BADGES.copy()
    )
    """The type badges to use in the Gopher view."""

    @cached_property
    def badge_mappings(self) -> BadgeMapping:
        """Get the badge mappings for the Gopher view.

        Returns:
            The badge mappings for the Gopher view.
        """
        return (
            (_DEFAULT_TYPE_BADGES | self.type_badges) if self.show_type_badges else {}
        )


##############################################################################
@cache
def load_gopher() -> GopherConfiguration:
    """Load the Gopher configuration.

    Returns:
        The loaded Gopher configuration.
    """
    return load_configuration_into(GopherConfiguration, "gopher")


### gopher.py ends here
