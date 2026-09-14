"""Provides code for loading the Gopher configuration."""

##############################################################################
# Future imports.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from functools import cache

##############################################################################
# GopherMap imports.
from gophermap import ItemType

##############################################################################
# Local imports.
from ._loader import load_configuration_into


##############################################################################
@dataclass(frozen=True)
class GopherConfiguration:
    """Gopher configuration."""

    show_type_badges: bool = True
    """Whether to show type badges in the Gopher view."""
    type_badges: dict[str, str] = field(
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


##############################################################################
@cache
def load_gopher() -> GopherConfiguration:
    """Load the Gopher configuration.

    Returns:
        The loaded Gopher configuration.
    """
    return load_configuration_into(GopherConfiguration, "gopher")


### gopher.py ends here
