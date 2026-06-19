"""Provides the main screen."""

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.getters import query_one
from textual.widgets import Footer, Header

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import ChangeTheme, Command, Help, Quit
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Wasat imports.
from wasat import Client, ConnectionError, GeminiURI, SecurityError

##############################################################################
# Local imports.
from ... import __version__
from ..commands import ChangeCommandLineLocation
from ..data import (
    load_command_history,
    load_configuration,
    save_command_history,
    trust_file,
    update_configuration,
)
from ..messages import OpenLocation, OpenText
from ..providers import MainCommands
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
        .panel {
            background: $surface;
            &:focus-within {
                background: $panel 80%;
            }
            * {
                scrollbar-background: $surface;
                scrollbar-background-hover: $surface;
                scrollbar-background-active: $surface;
            }
            &:focus-within * {
                scrollbar-background: $panel;
                scrollbar-background-hover: $panel;
                scrollbar-background-active: $panel;
            }
        }
    }
    """

    COMMAND_MESSAGES = [
        # Keep these together as they're bound to function keys and destined
        # for the footer.
        Help,
        Quit,
        # Everything else.
        ChangeTheme,
        ChangeCommandLineLocation,
    ]

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)

    COMMANDS = {MainCommands}

    _viewer = query_one(Viewer)
    """The viewer widget."""
    _command_line = query_one(CommandLine)
    """The command line widget."""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with VerticalGroup():
            yield Viewer(classes="panel")
            yield CommandLine()
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        config = load_configuration()
        self._command_line.dock_top = config.command_line_on_top
        self._command_line.history = load_command_history()

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
            async with await Client(
                verify_mode="tofu", trust_store_path=trust_file()
            ).request(uri) as response:
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

    def action_change_command_line_location_command(self) -> None:
        """Change the location of the command line."""
        self._command_line.dock_top = not self._command_line.dock_top
        with update_configuration() as config:
            config.command_line_on_top = self._command_line.dock_top

    @on(CommandLine.HistoryUpdated)
    def _save_command_line_history(self, message: CommandLine.HistoryUpdated) -> None:
        """Save the command line history when it is updated.

        Args:
            message: The message containing the command line whose history was updated.
        """
        save_command_history(message.command_line.history)

    @on(Quit)
    def action_quit_command(self) -> None:
        """Quit the application."""
        self.app.exit()

    @on(Help)
    async def _show_help(self) -> None:
        """Handle the help action."""
        await self.run_action("help_command")


### main.py ends here
