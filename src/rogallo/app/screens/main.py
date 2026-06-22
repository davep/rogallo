"""Provides the main screen."""

##############################################################################
# Python imports.
from webbrowser import open as open_in_browser

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.getters import query_one
from textual.reactive import var
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
from ..commands import (
    Backward,
    ChangeCommandLineLocation,
    Forward,
    JumpToCommandLine,
    JumpToDocument,
    ToggleHistory,
)
from ..data import (
    LocationHistory,
    NavigationHistory,
    load_command_history,
    load_configuration,
    load_location_history,
    load_navigation_history,
    save_command_history,
    save_location_history,
    save_naviagation_history,
    trust_file,
    update_configuration,
)
from ..messages import OpenLocation, OpenText, OpenURI
from ..providers import MainCommands
from ..widgets import CommandLine, HistoryViewer, Viewer


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
        #workspace {
            hatch: right $surface;
            height: 1fr;
            .panel {
                border-left: solid $panel;
                &:focus, &:focus-within {
                    border-left: solid $border;
                }
            }
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

        HistoryViewer {
            width: 30%;
            display: none;
        }

        &.--show-history HistoryViewer {
            display: block;
        }
    }
    """

    COMMAND_MESSAGES = [
        # Keep these together as they're bound to function keys and destined
        # for the footer.
        Help,
        ToggleHistory,
        Backward,
        Forward,
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
    _history_viewer = query_one(HistoryViewer)
    """The history viewer widget."""

    history: var[LocationHistory] = var(LocationHistory())
    """The location history."""

    _navigation_history: var[NavigationHistory] = var(NavigationHistory())
    """The navigation history."""

    _history_visible: var[bool] = var(False, toggle_class="--show-history")
    """Is the history panel visible?"""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with VerticalGroup():
            with HorizontalGroup(id="workspace"):
                yield Viewer(classes="panel")
                yield HistoryViewer(classes="panel").data_bind(Main.history)
            yield CommandLine()
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.history = load_location_history()
        self._navigation_history = load_navigation_history()
        config = load_configuration()
        self._command_line.dock_top = config.command_line_on_top
        self._command_line.history = load_command_history()
        self._history_visible = config.history_visible
        # If the navigation history isn't empty, let's visit the last location there.
        if self._navigation_history.current_item:
            self.post_message(
                OpenLocation(self._navigation_history.current_item, from_history=True)
            )

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
        if action == Backward.action_name():
            return self._navigation_history.can_go_backward or None
        if action == Forward.action_name():
            return self._navigation_history.can_go_forward or None
        if action == ToggleHistory.action_name():
            return len(self.history) > 0 or None
        return True

    def _maybe_remember_location(self, request: OpenLocation) -> None:
        """Remember a location in the history.

        Args:
            location: The location to remember.
        """
        self.history.add(request.location)
        self.mutate_reactive(Main.history)
        save_location_history(self.history)
        if not request.from_history:
            self._navigation_history.add(request.location)
            self.mutate_reactive(Main._navigation_history)
            save_naviagation_history(self._navigation_history)

    async def _handle_response(self, response: Response, request: OpenLocation) -> None:
        """Handle a response from a Gemini request.

        Args:
            response: The response to handle.
            request: The original request that generated the response.
        """
        assert isinstance(request.location, GeminiURI)
        uri = request.location
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
        self._maybe_remember_location(request)
        self.post_message(OpenText(await response.text(), uri))

    @work
    async def _load_from_capsule(self, request: OpenLocation) -> None:
        """Load a document from a Gemini URI.

        Args:
            uri: The Gemini URI to load the document from.
        """
        assert isinstance(request.location, GeminiURI)
        uri = request.location
        try:
            self._command_line.working = True
            async with await Client(
                verify_mode="tofu", trust_store_path=trust_file()
            ).request(uri) as response:
                await self._handle_response(response, request)
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
        finally:
            self._command_line.working = False

    @on(OpenText)
    def open_text(self, message: OpenText) -> None:
        """Open text in the viewer.

        Args:
            message: The message containing the text to open.
        """
        self._viewer.document = Viewer.Document(message.originally_from, message.text)
        self.refresh_bindings()

    @on(OpenLocation)
    def open_location(self, message: OpenLocation) -> None:
        """Open a location in the viewer.

        Args:
            message: The message the location open request.
        """
        if isinstance(message.location, GeminiURI):
            self._load_from_capsule(message)

    @on(OpenURI)
    def open_uri(self, message: OpenURI) -> None:
        """Open a URI in the viewer.

        Args:
            message: The message containing the URI to open.
        """

        # Does it look like a Gemini URI?
        try:
            self.post_message(OpenLocation(GeminiURI(message.uri)))
            return
        except URIError:
            pass

        # TODO: Handle gmi files in the filesystem.

        # Otherwise, try to open it in the system browser.
        open_in_browser(message.uri)

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

    def action_change_command_line_location_command(self) -> None:
        """Change the location of the command line."""
        self._command_line.dock_top = not self._command_line.dock_top
        with update_configuration() as config:
            config.command_line_on_top = self._command_line.dock_top

    def action_jump_to_command_line_command(self) -> None:
        """Jump to the command line."""
        assert self.AUTO_FOCUS is not None
        self.query_one(self.AUTO_FOCUS).focus()

    def action_jump_to_document_command(self) -> None:
        """Jump to the document."""
        if self._viewer.document:
            self._viewer.take_control()

    def action_backward_command(self) -> None:
        """Go backward in the navigation history."""
        if (
            self._navigation_history.backward()
            and self._navigation_history.current_item
        ):
            self.post_message(
                OpenLocation(self._navigation_history.current_item, from_history=True)
            )
            self.mutate_reactive(Main._navigation_history)

    def action_forward_command(self) -> None:
        """Go forward in the navigation history."""
        if self._navigation_history.forward() and self._navigation_history.current_item:
            self.post_message(
                OpenLocation(self._navigation_history.current_item, from_history=True)
            )
            self.mutate_reactive(Main._navigation_history)

    def action_toggle_history_command(self) -> None:
        """Toggle the visibility of the history panel."""
        self._history_visible = not self._history_visible
        with update_configuration() as config:
            config.history_visible = self._history_visible
        if self._history_visible:
            self._history_viewer.focus()
        else:
            self._viewer.take_control()


### main.py ends here
