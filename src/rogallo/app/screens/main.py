"""Provides the main screen."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.widgets import Footer, Header

##############################################################################
# Textual enhanced imports.
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Local imports.
from ... import __version__
from ..messages import OpenLocation
from ..widgets import CommandLine, Viewer


##############################################################################
class Main(EnhancedScreen[None]):
    """The main screen for the application."""

    TITLE = f"Rogallo v{__version__}"

    HELP = """
    ## Main application keys and commands

    The following keys and commands can be used anywhere here on the main screen.
    """

    DEFAULT_CSS = """
    Main {
        hatch: right $surface;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        yield Viewer()
        yield CommandLine()
        yield Footer()

    @on(OpenLocation)
    def open_location(self, message: OpenLocation) -> None:
        """Open a location in the viewer.

        Args:
            message: The message containing the location to open.
        """
        self.notify(f"Opening {message.to_open}...")


### main.py ends here
