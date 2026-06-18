"""The main application class."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.app import EnhancedApp

##############################################################################
# Local imports.
from .. import __version__


##############################################################################
class Rogallo(EnhancedApp[None]):
    """The main application class."""

    HELP_TITLE = f"Rogallo v{__version__}"
    HELP_ABOUT = """
    Rogallo is a terminal-based client for Gemini; it was created by and
    is maintained by Dave Pearson; it is Free Software and can be found on
    GitHub.
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


### rogallo.py ends here
