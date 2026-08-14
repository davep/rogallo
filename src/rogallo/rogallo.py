"""The main application class."""

##############################################################################
# Python imports.
from argparse import Namespace
from os import getenv
from typing import Final

##############################################################################
# Textual imports.
from textual.app import InvalidThemeError
from textual.binding import Binding
from textual.screen import Screen

##############################################################################
# Textual enhanced imports.
from textual_enhanced.app import EnhancedApp

##############################################################################
# Local imports.
from . import __version__
from .data import (
    load_configuration,
    load_themes,
    update_configuration,
)
from .screens import Main

##############################################################################
ROGALLO_SCREENSHOTS: Final[bool] = bool(getenv("ROGALLO_SCREENSHOTS"))
"""Should we enable the ANSI screenshot feature?"""


##############################################################################
class Rogallo(EnhancedApp[None]):
    """The main application class."""

    HELP_TITLE = f"Rogallo v{__version__}"
    HELP_ABOUT = """
    `Rogallo` is a terminal-based client for small web protocols; it was
    created by and is maintained by Dave Pearson; it is Free Software and
    can be found on GitHub.
    """
    HELP_LICENSE = """
    Rogallo - A terminal-based client for small web protocols.  \n    Copyright (C) 2026 Dave Pearson

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
    more details.

    You should have received a copy of the GNU General Public License along with
    this program. If not, see <https://www.gnu.org/licenses/>.
    """

    COMMANDS = set()

    BINDINGS = (
        [
            Binding(
                "ctrl+shift+f12",
                "ansi_screenshot",
                "Take ANSI screenshot",
                priority=True,
                show=False,
            ),
        ]
        if ROGALLO_SCREENSHOTS
        else []
    )

    def __init__(self, arguments: Namespace) -> None:
        """Initialise the application.

        Args:
            The command line arguments passed to the application.
        """
        self._arguments = arguments
        """The command line arguments passed to the application."""
        super().__init__()
        for theme in load_themes():
            self.register_theme(theme)
        configuration = load_configuration()
        if configuration.theme is not None:
            try:
                self.theme = arguments.theme or configuration.theme
            except InvalidThemeError:
                pass
        self.update_keymap(configuration.bindings)
        if configuration.disable_animations:
            self.animation_level = "none"

    def watch_theme(self) -> None:
        """Save the application's theme when it's changed."""
        with update_configuration() as config:
            config.theme = self.theme

    def get_default_screen(self) -> Screen[None]:
        return Main(self._arguments)

    def action_ansi_screenshot(self) -> None:
        """Take an ANSI screenshot of the application."""
        if not ROGALLO_SCREENSHOTS:
            return
        from ._screenshot import save_ansi_screenshot

        save_ansi_screenshot(self, screenshot := "~/rogallo-screenshot.ansi")
        self.notify(screenshot, title="Saved")


### rogallo.py ends here
