"""Provides the main screen."""

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.getters import query_one
from textual.widgets import Footer, Header

##############################################################################
# Textual enhanced imports.
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Wasat imports.
from wasat import Client, ConnectionError, GeminiURI, SecurityError

##############################################################################
# Local imports.
from ... import __version__
from ..messages import OpenLocation, OpenText
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

    _viewer = query_one(Viewer)
    """The viewer widget."""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        yield Viewer()
        yield CommandLine()
        yield Footer()

    @on(OpenText)
    def open_text(self, message: OpenText) -> None:
        """Open text in the viewer.

        Args:
            message: The message containing the text to open.
        """
        self._viewer.document = message.text

    @work
    async def _load_from_capsule(self, uri: GeminiURI) -> None:
        """Load a document from a Gemini URI.

        Args:
            uri: The Gemini URI to load the document from.
        """
        try:
            # TODO: Configure where the trust store is located.
            async with await Client(verify_mode="tofu").request(uri) as response:
                self.post_message(OpenText(await response.text(), uri))
        except ConnectionError as error:
            self.notify(
                f"Error loading {uri}:\n\n{error}",
                severity="error",
                title="Connection Error",
            )
        except SecurityError as error:
            self.notify(
                f"Error loading {uri}:\n\n{error}",
                severity="error",
                title="Security Error",
            )

    @on(OpenLocation)
    def open_location(self, message: OpenLocation) -> None:
        """Open a location in the viewer.

        Args:
            message: The message containing the location to open.
        """
        if isinstance(message.to_open, GeminiURI):
            self._load_from_capsule(message.to_open)


### main.py ends here
