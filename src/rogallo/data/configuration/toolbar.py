"""Provides code for loading the toolbar configuration."""

##############################################################################
# Future imports.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from functools import cache
from typing import NotRequired, TypedDict

##############################################################################
# Local imports.
from ._io import load_configuration_into


##############################################################################
class ToolbarButton(TypedDict):
    """A button on the toolbar."""

    command: str
    """The command that the button runs."""
    label: NotRequired[str | None]
    """The label of the button."""


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


##############################################################################
@cache
def load_toolbar() -> ToolbarConfiguration:
    """Load the toolbar configuration.

    Returns:
        The loaded toolbar configuration.
    """
    return load_configuration_into(ToolbarConfiguration, "toolbar")


### toolbar.py ends here
