"""The main application class."""

##############################################################################
# Python imports.
from argparse import Namespace

##############################################################################
# Textual imports.
from textual.app import InvalidThemeError
from textual.screen import Screen

##############################################################################
# Textual enhanced imports.
from textual_enhanced.app import EnhancedApp

##############################################################################
# Local imports.
from . import __version__
from .data import (
    load_configuration,
    update_configuration,
)
from .screens import Main


##############################################################################
class Rogallo(EnhancedApp[None]):
    """The main application class."""

    HELP_TITLE = f"Rogallo v{__version__}"
    HELP_ABOUT = """
    `Rogallo` is a terminal-based client for the Gemini protocol; it was
    created by and is maintained by Dave Pearson; it is Free Software and
    can be found on GitHub.
    """
    HELP_LICENSE = """
    Rogallo - A client for the Gemini protocol for the terminal.  \n    Copyright (C) 2026 Dave Pearson

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

    def __init__(self, arguments: Namespace) -> None:
        """Initialise the application.

        Args:
            The command line arguments passed to the application.
        """
        self._arguments = arguments
        """The command line arguments passed to the application."""
        super().__init__()
        configuration = load_configuration()
        if configuration.theme is not None:
            try:
                self.theme = arguments.theme or configuration.theme
            except InvalidThemeError:
                pass
        self.update_keymap(configuration.bindings)

    def watch_theme(self) -> None:
        """Save the application's theme when it's changed."""
        with update_configuration() as config:
            config.theme = self.theme

    def get_default_screen(self) -> Screen[None]:
        return Main()


### rogallo.py ends here
