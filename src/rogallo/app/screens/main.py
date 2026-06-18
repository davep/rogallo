"""Provides the main screen."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.widgets import Footer, Header

##############################################################################
# Textual enhanced imports.
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Local imports.
from ... import __version__


##############################################################################
class Main(EnhancedScreen[None]):
    """The main screen for the application."""

    TITLE = f"Rogallo v{__version__}"

    HELP = """
    ## Main application keys and commands

    The following keys and commands can be used anywhere here on the main screen.
    """

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        yield Footer()


### main.py ends here
