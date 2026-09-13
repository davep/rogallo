"""Provides code for loading the toolbar configuration."""

##############################################################################
# Future imports.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import asdict, dataclass, field
from functools import cache
from pathlib import Path
from typing import NotRequired, TypedDict, cast

##############################################################################
# PyYAML imports.
from ..locations import config_dir

##############################################################################
# Local imports.
from ._loader import load_configuration


##############################################################################
def toolbar_file() -> Path:
    """The path to the file that configures the toolbar.

    Returns:
        The path to the toolbar file.
    """
    return config_dir() / "toolbar.yaml"


##############################################################################
class ToolbarButton(TypedDict):
    """A button on the toolbar."""

    command: str
    """The command that the button runs."""
    label: NotRequired[str | None]
    """The label of the button."""


###############################################################################
class ToolbarConfigurationData(TypedDict):
    """The shape of the toolbar configuration data."""

    visible: bool
    """Whether the toolbar is visible."""
    can_get_focus: bool
    """Whether the toolbar can get focus."""
    show_tooltips: bool
    """Whether the toolbar buttons have tooltips."""
    buttons: list[ToolbarButton]
    """The contents of the toolbar."""


##############################################################################
@dataclass(frozen=True)
class ToolbarConfiguration:
    """Toolbar configuration data."""

    visible: bool = True
    """Whether the toolbar is visible."""
    can_get_focus: bool = False
    """Whether the toolbar can get focus."""
    show_tooltips: bool = True
    """Whether the toolbar buttons have tooltips."""
    buttons: list[ToolbarButton] = field(
        default_factory=lambda: [
            ToolbarButton(command="GoHome", label="⌂"),
            ToolbarButton(command="Reload", label="↻"),
            ToolbarButton(command="Backward", label="◀◀"),
            ToolbarButton(command="Forward", label="▶▶"),
            ToolbarButton(command="GoToParent", label="↑"),
            ToolbarButton(command="GoToRoot", label="⇈"),
            ToolbarButton(command="SearchHistory", label="◷"),
            ToolbarButton(command="SearchBookmarks", label="★"),
            ToolbarButton(command="ToggleView", label="⇋"),
        ]
    )
    """The contents of the toolbar."""

    @classmethod
    def from_dict(cls, data: ToolbarConfigurationData) -> ToolbarConfiguration:
        """Load a toolbar configuration from a dictionary.

        Args:
            data: The data to load from.

        Returns:
            A fresh instance of a toolbar configuration.
        """
        return cls(
            visible=data.get("visible", True),
            can_get_focus=data.get("can_get_focus", False),
            show_tooltips=data.get("show_tooltips", True),
            buttons=data.get("buttons", []),
        )


##############################################################################
@cache
def load_toolbar() -> ToolbarConfiguration:
    """Load the toolbar configuration.

    Returns:
        The loaded toolbar configuration.
    """
    return ToolbarConfiguration.from_dict(
        cast(
            ToolbarConfigurationData,
            load_configuration("toolbar", default=asdict(ToolbarConfiguration())),
        )
    )


### toolbar.py ends here
