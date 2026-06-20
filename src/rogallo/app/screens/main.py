"""Provides the main screen."""

##############################################################################
# Python imports.
from webbrowser import open as open_in_browser

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
from wasat import Client, ConnectionError, GeminiURI, Response, SecurityError, URIError

##############################################################################
# Local imports.
from ... import __version__
from ..commands import ChangeCommandLineLocation, JumpToCommandLine, JumpToDocument
from ..data import (
    load_command_history,
    load_configuration,
    save_command_history,
    trust_file,
    update_configuration,
)
from ..messages import OpenLocation, OpenText, OpenURI
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
        VerticalGroup {
            hatch: right $surface;
        }
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
        JumpToCommandLine,
        JumpToDocument,
    ]

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)
    COMMANDS = {MainCommands}
    AUTO_FOCUS = "CommandLine Input"

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

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Check if an action is possible to perform right now.

        Args:
            action: The action to perform.
            parameters: The parameters of the action.

        Returns:
            `True` if it can perform, `False` or `None` if not.
        """
        if not self.is_mounted:
            return True
        if action == JumpToDocument.action_name():
            return bool(self._viewer.document)
        if action == JumpToCommandLine.action_name():
            return not self._command_line.has_control
        return True

    @on(OpenText)
    def open_text(self, message: OpenText) -> None:
        """Open text in the viewer.

        Args:
            message: The message containing the text to open.
        """
        self._viewer.document = Viewer.Document(message.originally_from, message.text)

    @on(OpenURI)
    def open_uri(self, message: OpenURI) -> None:
        """Open a URI in the viewer.

        Args:
            message: The message containing the URI to open.
        """

        # Does it look like a Gemini URI?
        try:
            self.post_message(OpenLocation(GeminiURI(message.to_open)))
            return
        except URIError:
            pass

        # TODO: Handle gmi files in the filesystem.

        # Otherwise, try to open it in the system browser.
        open_in_browser(message.to_open)

    async def _handle_response(self, response: Response, uri: GeminiURI) -> None:
        """Handle a response from a Gemini request.

        Args:
            response: The response to handle.
            uri: The URI the response was received from.
        """
        if not response.status.is_success:
            self.notify(
                f"Error loading {uri}:\n\n{response.status.value} {response.status.name}\n{response.meta}",
                severity="error",
                title="Request Error",
            )
            return
        if response.content_type not in load_configuration().displayable_content_types:
            self.notify(
                f"Error loading {uri}:\n\nUnsupported MIME type: {response.mime_type}",
                severity="error",
                title="Request Error",
            )
            return
        self.post_message(OpenText(await response.text(), uri))

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
                await self._handle_response(response, uri)
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

    def action_jump_to_command_line_command(self) -> None:
        """Jump to the command line."""
        assert self.AUTO_FOCUS is not None
        self.query_one(self.AUTO_FOCUS).focus()

    def action_jump_to_document_command(self) -> None:
        """Jump to the document."""
        if self._viewer.document:
            self._viewer.focus()


### main.py ends here
