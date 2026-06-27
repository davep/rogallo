"""Provides the main screen."""

##############################################################################
# Python imports.
from argparse import Namespace
from pathlib import Path
from webbrowser import open as open_in_browser

##############################################################################
# Pyperclip imports.
from pyperclip import PyperclipException
from pyperclip import copy as copy_to_clipboard

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.getters import query_one
from textual.reactive import var
from textual.widgets import Footer, Header, Label

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import ChangeTheme, Command, Help, Quit
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Wasat imports.
from wasat import Client, ConnectionError, GeminiURI, Response, SecurityError, URIError
from wasat.uri import GEMINI_PREFIX

##############################################################################
# Local imports.
from .. import __version__
from ..commands import (
    Backward,
    ChangeCommandLineLocation,
    Forward,
    JumpToCommandLine,
    JumpToDocument,
    Reload,
    ToggleHistory,
)
from ..data import (
    CommandLineHistory,
    LocationHistory,
    LocationVisit,
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
from ..messages import CopyToClipboard, OpenLocation, OpenText, OpenURI
from ..preflight import (
    is_likely_local_text_file,
    is_likely_schemeless_capsule,
    path_from_uri,
)
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

        #history {
            width: 30%;
            display: none;
            Label {
                padding: 0 1;
                text-align: right;
                background: $panel;
                width: 1fr;
            }
        }

        &.--show-history #history {
            display: block;
        }
    }

    Tooltip {
        max-width: 90vw !important;
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
        Reload,
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

    _location_history: var[LocationHistory] = var(LocationHistory)
    """The location history."""
    _navigation_history: var[NavigationHistory] = var(NavigationHistory)
    """The navigation history."""
    _command_history: var[CommandLineHistory] = var(CommandLineHistory)
    """The command line history."""

    _history_visible: var[bool] = var(False, toggle_class="--show-history")
    """Is the history panel visible?"""

    def __init__(self, arguments: Namespace) -> None:
        """Initialize the main screen.

        Args:
            arguments: The command line arguments.
        """
        super().__init__()
        self._arguments = arguments
        """The command line arguments."""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with VerticalGroup():
            with HorizontalGroup(id="workspace"):
                yield Viewer(classes="panel")
                with VerticalGroup(classes="panel", id="history"):
                    yield Label("History")
                    yield HistoryViewer().data_bind(history=Main._location_history)
            yield CommandLine().data_bind(history=Main._command_history)
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self._location_history = load_location_history()
        self._navigation_history = load_navigation_history()
        config = load_configuration()
        self._command_line.dock_top = config.command_line_on_top
        self._command_line.history = load_command_history()
        self._history_visible = config.history_visible
        if self._arguments.command == "open" and (
            location := getattr(self._arguments, "location", None)
        ):
            self.post_message(OpenURI(location))
        elif self._location_history.current_item:
            self.post_message(
                OpenLocation(
                    self._location_history.current_item.location, from_history=True
                )
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
            return len(self._location_history) > 0 or None
        if action == Reload.action_name():
            return bool(self._viewer.document)
        return True

    async def _handle_response(self, response: Response, request: OpenLocation) -> None:
        """Handle a response from a Gemini request.

        Args:
            response: The response to handle.
            request: The original request that generated the response.
        """
        assert isinstance(request.location, GeminiURI)
        uri = response.uri or response.requested_uri or request.location
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
        self.post_message(OpenText(await response.text(), request, uri))

    def _maybe_remember_location(self, request: OpenText) -> None:
        """Remember a location in the history.

        Args:
            request: The request to open text for. This is used to determine
                the location to remember.
        """
        self._location_history.add(LocationVisit(request.originally_from))
        self.mutate_reactive(Main._location_history)
        save_location_history(self._location_history)
        if (
            not request.original_request.from_history
            and self._navigation_history.current_item != request.originally_from
        ):
            self._navigation_history.add(request.originally_from)
            self.mutate_reactive(Main._navigation_history)
            save_naviagation_history(self._navigation_history)

    @on(OpenText)
    def open_text(self, message: OpenText) -> None:
        """Open text in the viewer.

        Args:
            message: The message containing the text to open.
        """
        self._maybe_remember_location(message)
        self._viewer.document = Viewer.Document(message.originally_from, message.text)
        self.refresh_bindings()

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

    @work(thread=True)
    def _load_from_filesystem(self, request: OpenLocation) -> None:
        """Load a document from the filesystem.

        Args:
            request: The request to load the document from.
        """
        assert isinstance(request.location, Path)
        try:
            self.post_message(
                OpenText(
                    request.location.read_text(encoding="utf-8"),
                    request,
                    request.location,
                )
            )
        except OSError as error:
            self.notify(
                f"Error loading {request.location}:\n\n{error}",
                severity="error",
                title="Filesystem Error",
            )
        except UnicodeDecodeError as error:
            self.notify(
                f"Error loading {request.location}:\n\n{error}\n\nLikely not a text file.",
                severity="error",
                title="Decode Error",
            )

    @on(OpenLocation)
    def open_location(self, message: OpenLocation) -> None:
        """Open a location in the viewer.

        Args:
            message: The message the location open request.
        """
        if isinstance(message.location, GeminiURI):
            self._load_from_capsule(message)
        else:
            self._load_from_filesystem(message)

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

        # Perhaps it's a local text file?
        if is_likely_local_text_file(message.uri):
            self.post_message(OpenLocation(path_from_uri(message.uri)))
            return

        # It's not an obvious Gemini URI, and it's not a file in the local
        # filesystem. Before we pass it off to the system browser, let's see
        # it could look like a Gemini URI if we add the scheme.
        if is_likely_schemeless_capsule(message.uri):
            self.post_message(OpenLocation(GeminiURI(f"{GEMINI_PREFIX}{message.uri}")))
            return

        # Otherwise, try to open it in the system browser.
        open_in_browser(message.uri)

    @on(CommandLine.CommandExecuted)
    def _save_command_line_history(self, message: CommandLine.CommandExecuted) -> None:
        """Save the command line history when a command is executed.

        Args:
            message: The message containing the command that was executed.
        """
        save_command_history(message.command_line.history)

    @on(CopyToClipboard)
    def _copy_text_to_clipboard(self, message: CopyToClipboard) -> None:
        """Copy text to the clipboard.

        Args:
            message: The message containing the text to copy.
        """
        # First off, use Textual's own copy to clipboard facility. Generally
        # this will work in most terminals, and if it does it'll likely work
        # best, getting the text through remote connections to the user's
        # own environment.
        self.app.copy_to_clipboard(message.text)
        # However, as a backup, use pyerclip too. If the above did fail due
        # to the terminal not supporting the operation, this might.
        try:
            copy_to_clipboard(message.text)
        except PyperclipException:
            pass
        self.notify(
            f"Copied {message.description} to clipboard"
            if message.description
            else "Copied"
        )

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
        if self._history_visible:
            self._history_visible = not self._history_viewer.has_focus
        else:
            self._history_visible = True
        with update_configuration() as config:
            config.history_visible = self._history_visible
        if self._history_visible:
            self._history_viewer.focus()
        else:
            self._viewer.take_control()

    def action_reload_command(self) -> None:
        """Reload the current document."""
        if self._viewer.document.location:
            self.post_message(
                OpenLocation(self._viewer.document.location, from_history=True)
            )


### main.py ends here
