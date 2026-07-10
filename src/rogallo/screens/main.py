"""Provides the main screen."""

##############################################################################
# Python imports.
from argparse import Namespace
from mimetypes import guess_type
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
from textual.suggester import SuggestFromList
from textual.widgets import Footer, Header, Label

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import ChangeTheme, Command, Help, Quit
from textual_enhanced.dialogs import Confirm, ModalInput
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Wasat imports.
from wasat import (
    Client,
    ConnectionError,
    GeminiURI,
    Response,
    SecurityError,
    StatusCode,
    URIError,
)
from wasat.uri import GEMINI_PREFIX

##############################################################################
# Local imports.
from .. import __version__
from ..cache import ContentCache
from ..commands import (
    AddLocationToBookmarks,
    Backward,
    ChangeCommandLineLocation,
    ClearCache,
    CopyDocumentToClipboard,
    CopyLocationToClipboard,
    Forward,
    GoHome,
    JumpToCommandLine,
    JumpToDocument,
    JumpToSidebar,
    Reload,
    SearchBookmarks,
    SearchHistory,
    SetHome,
    SetHomeToCurrentLocation,
    ToggleBookmarks,
    ToggleHistory,
    ToggleView,
)
from ..data import (
    Bookmark,
    Bookmarks,
    CommandLineHistory,
    LocationHistory,
    LocationVisit,
    NavigationHistory,
    client_certificates_directory,
    load_bookmarks,
    load_command_history,
    load_configuration,
    load_location_history,
    load_navigation_history,
    save_bookmarks,
    save_command_history,
    save_location_history,
    save_naviagation_history,
    trust_file,
    update_configuration,
)
from ..document import Document
from ..messages import CopyToClipboard, OpenDocument, OpenLocation, OpenURI
from ..preflight import (
    is_likely_local_text_file,
    is_likely_schemeless_capsule,
    path_from_uri,
)
from ..providers import BookmarkSearchCommands, HistorySearchCommands, MainCommands
from ..types import GeminiLocation
from ..widgets import BookmarksViewer, CommandLine, HistoryViewer, Viewer
from .user_input import UserInput


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

        #history, #bookmarks {
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
        &.--show-bookmarks #bookmarks {
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
        ToggleBookmarks,
        Backward,
        Forward,
        Quit,
        # Everything else.
        AddLocationToBookmarks,
        ChangeTheme,
        ChangeCommandLineLocation,
        JumpToCommandLine,
        JumpToDocument,
        JumpToSidebar,
        Reload,
        CopyDocumentToClipboard,
        CopyLocationToClipboard,
        ToggleView,
        GoHome,
        SetHome,
        SetHomeToCurrentLocation,
        SearchHistory,
        SearchBookmarks,
        ClearCache,
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
    _bookmarks_viewer = query_one(BookmarksViewer)
    """The bookmarks viewer widget."""

    _location_history: var[LocationHistory] = var(LocationHistory)
    """The location history."""
    _navigation_history: var[NavigationHistory] = var(NavigationHistory)
    """The navigation history."""
    _command_history: var[CommandLineHistory] = var(CommandLineHistory)
    """The command line history."""
    _bookmarks: var[Bookmarks] = var(list)
    """The bookmarks."""

    _history_visible: var[bool] = var(False, toggle_class="--show-history")
    """Is the history panel visible?"""
    _bookmarks_visible: var[bool] = var(False, toggle_class="--show-bookmarks")
    """Is the bookmarks panel visible?"""

    def __init__(self, arguments: Namespace) -> None:
        """Initialize the main screen.

        Args:
            arguments: The command line arguments.
        """
        super().__init__()
        self._arguments = arguments
        """The command line arguments."""
        self._cache = ContentCache()
        """The disk cache manager."""
        self._client = Client(
            verify_mode="tofu",
            trust_store_path=trust_file(),
            client_cert_store_path=client_certificates_directory(),
        )
        """The Gemini client."""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with VerticalGroup():
            with HorizontalGroup(id="workspace"):
                yield Viewer(classes="panel")
                with VerticalGroup(classes="panel", id="history"):
                    yield Label("History")
                    yield HistoryViewer().data_bind(history=Main._location_history)
                with VerticalGroup(classes="panel", id="bookmarks"):
                    yield Label("Bookmarks")
                    yield BookmarksViewer().data_bind(bookmarks=Main._bookmarks)
            yield CommandLine().data_bind(
                history=Main._command_history,
                location_history=Main._location_history,
                navigation_history=Main._navigation_history,
                bookmarks=Main._bookmarks,
            )
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self._location_history = load_location_history()
        self._navigation_history = load_navigation_history()
        self._bookmarks = load_bookmarks()
        config = load_configuration()
        self._command_line.dock_top = config.command_line_on_top
        self._command_line.history = load_command_history()
        self._history_visible = config.history_visible
        self._bookmarks_visible = config.bookmarks_visble
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
        if action in (ToggleHistory.action_name(), SearchHistory.action_name()):
            return len(self._location_history) > 0 or None
        if action == ToggleBookmarks.action_name():
            return len(self._bookmarks) > 0 or None
        if action in (
            Reload.action_name(),
            CopyLocationToClipboard.action_name(),
            SetHomeToCurrentLocation.action_name(),
        ):
            return bool(self._viewer.document.location)
        if action == CopyDocumentToClipboard.action_name():
            return bool(self._viewer.document)
        if action == ToggleView.action_name():
            return bool(self._viewer.document) and self._viewer.document.is_gemtext
        if action == GoHome.action_name():
            return bool(load_configuration().home_page.strip())
        if action == AddLocationToBookmarks.action_name():
            return bool(self._viewer.document.location) and (
                self._viewer.document.location not in self._bookmarks
            )
        return True

    def _open_externally(self, location: GeminiLocation, mime_type: str | None) -> None:
        """Open a location in the system's web browser.

        Args:
            location: The location to open.
            mime_type: The MIME type of the content at the location.
        """
        self.notify(
            f"Unable to display {location} because it is {mime_type}. "
            "Opening in the system's web browser instead.",
            title="Unsupported MIME type",
        )
        open_in_browser(
            str(location)
            if isinstance(location, GeminiURI)
            else location.resolve().as_uri()
        )

    def _is_displayable(self, mime_type: str | None) -> bool:
        """Check if a MIME type is displayable.

        Args:
            mime_type: The MIME type to check.

        Returns:
            `True` if the MIME type is displayable, `False` otherwise.
        """
        if isinstance(mime_type, str):
            mime_type, _, _ = mime_type.partition(";")
        return mime_type in load_configuration().displayable_content_types

    async def _handle_input_request(
        self, location: GeminiURI, prompt: str, sensitive: bool
    ) -> None:
        """Handle a request for input from a Gemini request.

        Args:
            location: The location making the request.
            sensitive: Whether the input is sensitive.
        """
        if user_input := await self.app.push_screen_wait(
            UserInput(location, prompt=prompt, sensitive=sensitive)
        ):
            try:
                self.post_message(OpenLocation(location.with_query(user_input)))
            except URIError as error:
                self.notify(
                    f"Unable to create query for {location}:\n\n{error}",
                    severity="error",
                    title="Input Error",
                )

    async def _handle_client_certificate_request(self, location: GeminiURI) -> None:
        """Handle a request for a client certificate from a Gemini request.

        Args:
            location: The location making the request.
        """
        if (
            common_name := await self.app.push_screen_wait(
                ModalInput("Enter a descriptive name for the client certificate")
            )
        ) is None:
            self.notify("Client certificate request cancelled.", severity="warning")
            return
        await self._client.client_cert_store.create_credentials(
            uri=location,
            transient=False,
            common_name=common_name.strip(),
            valid_days=None,
        )
        self.post_message(OpenLocation(location, allow_cached=False))

    async def _handle_response(self, response: Response, request: OpenLocation) -> None:
        """Handle a response from a Gemini request.

        Args:
            response: The response to handle.
            request: The original request that generated the response.
        """
        assert isinstance(request.location, GeminiURI)
        uri = response.uri or response.requested_uri or request.location

        # Handle a request for user input.
        if response.status.is_input:
            await self._handle_input_request(
                request.location,
                response.meta.strip(),
                response.status is StatusCode.SENSITIVE_INPUT,
            )
            return

        # Handle a request for a client certificate.
        if response.status.is_client_certificate_required:
            if not await self._client.client_cert_store.get_credentials(uri):
                await self._handle_client_certificate_request(uri)
            return

        # Handle any other non-successful response.
        if not response.status.is_success:
            self.notify(
                f"Error loading {uri}:\n\n{response.status.value} {response.status.name}\n{response.meta}",
                severity="error",
                title="Request Error",
            )
            return

        # Handle a successful response.
        if self._is_displayable(response.mime_type):
            self.post_message(
                OpenDocument(
                    document=self._cache.add_document(
                        Document(
                            location=uri,
                            original_location=request.location,
                            content=await response.text(),
                            mime_type=response.mime_type,
                        )
                    ),
                    original_request=request,
                )
            )
        else:
            self._open_externally(uri, response.mime_type)

    def _maybe_remember_location(self, request: OpenDocument) -> None:
        """Remember a location in the history.

        Args:
            request: The request to open text for. This is used to determine
                the location to remember.
        """
        if request.document.original_location is None:
            return
        self._location_history.add(LocationVisit(request.document.original_location))
        self.mutate_reactive(Main._location_history)
        save_location_history(self._location_history)
        if (
            not request.original_request.from_history
            and self._navigation_history.current_item
            != request.document.original_location
        ):
            self._navigation_history.add(request.document.original_location)
            self.mutate_reactive(Main._navigation_history)
            save_naviagation_history(self._navigation_history)

    @on(OpenDocument)
    def open_document(self, message: OpenDocument) -> None:
        """Open a document in the viewer.

        Args:
            message: The message containing the document to open.
        """
        self._maybe_remember_location(message)
        self._viewer.document = message.document
        self.refresh_bindings()
        self._viewer.take_control()

    @work
    async def _load_from_capsule(self, request: OpenLocation) -> None:
        """Load a document from a Gemini URI.

        Args:
            uri: The Gemini URI to load the document from.
        """
        uri = request.location
        assert isinstance(uri, GeminiURI)

        # If a cached copy of the document exists and the request allows it,
        # use that instead of making a network request.
        if request.allow_cached and (cached_document := self._cache.get_document(uri)):
            self.post_message(
                OpenDocument(
                    document=cached_document,
                    original_request=request,
                )
            )
            return

        # Otherwise, make a request to the capsule and handle the response.
        try:
            self._command_line.working = True
            async with await self._client.request(uri) as response:
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
        mime_type = guess_type(request.location)[0]
        if not self._is_displayable(mime_type):
            self._open_externally(request.location, mime_type)
            return
        try:
            self.post_message(
                OpenDocument(
                    document=Document(
                        location=request.location,
                        original_location=request.location,
                        content=request.location.read_text(encoding="utf-8"),
                        mime_type=mime_type,
                    ),
                    original_request=request,
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

    @on(HistoryViewer.HistoryModified)
    def _save_location_history(self) -> None:
        """Save the location history when it is modified.

        Args:
            message: The message containing the modified history.
        """
        save_location_history(self._location_history)

    @on(BookmarksViewer.BookmarksModified)
    def _save_bookmarks(self) -> None:
        """Save the bookmarks when they are modified.

        Args:
            message: The message containing the modified bookmarks.
        """
        save_bookmarks(self._bookmarks)

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

    def action_jump_to_sidebar_command(self) -> None:
        """Jump to the sidebar."""
        if self._history_visible:
            self._history_viewer.focus()
        elif self._bookmarks_visible:
            self._bookmarks_viewer.focus()
        else:
            self._history_visible = True
            self._history_viewer.focus()

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
        if self._history_visible:
            self._history_viewer.focus()
        else:
            self._viewer.take_control()
        if self._history_visible and self._bookmarks_visible:
            self._bookmarks_visible = False

    def action_toggle_bookmarks_command(self) -> None:
        """Toggle the visibility of the bookmarks panel."""
        if self._bookmarks_visible:
            self._bookmarks_visible = not self._bookmarks_viewer.has_focus
        else:
            self._bookmarks_visible = True
        if self._bookmarks_visible:
            self._bookmarks_viewer.focus()
        else:
            self._viewer.take_control()
        if self._bookmarks_visible and self._history_visible:
            self._history_visible = False

    def _watch__history_visible(self) -> None:
        """Watch for changes to the history visibility."""
        with update_configuration() as config:
            config.history_visible = self._history_visible

    def _watch__bookmarks_visible(self) -> None:
        """Watch for changes to the bookmarks visibility."""
        with update_configuration() as config:
            config.bookmarks_visble = self._bookmarks_visible

    def action_reload_command(self) -> None:
        """Reload the current document."""
        if self._viewer.document.location:
            self.post_message(
                OpenLocation(
                    self._viewer.document.location,
                    from_history=True,
                    allow_cached=False,
                )
            )

    def action_copy_location_to_clipboard_command(self) -> None:
        """Copy the current document's URI to the clipboard."""
        if self._viewer.document.location:
            self.post_message(
                CopyToClipboard(
                    str(self._viewer.document.location),
                    description="current location",
                )
            )

    def action_copy_document_to_clipboard_command(self) -> None:
        """Copy the current document's content to the clipboard."""
        if self._viewer.document:
            self.post_message(
                CopyToClipboard(
                    self._viewer.document.content, description="current document"
                )
            )

    def action_toggle_view_command(self) -> None:
        """Toggle the view between rendered and source."""
        if self._viewer.document.is_gemtext:
            self._viewer.view_source = not self._viewer.view_source

    def action_go_home_command(self) -> None:
        """Go to the home page."""
        if home_page := load_configuration().home_page.strip():
            self.post_message(OpenURI(home_page))

    @work
    async def action_set_home_command(self) -> None:
        """Set the home page."""
        if user_input := await self.app.push_screen_wait(
            ModalInput(
                "New home page",
                load_configuration().home_page.strip(),
                suggester=SuggestFromList(
                    sorted(str(visit.location) for visit in self._location_history)
                ),
            ),
        ):
            with update_configuration() as config:
                config.home_page = user_input.strip()
            self.notify(f"Set to {user_input}", title="Home Page Set")

    def action_set_home_to_current_location_command(self) -> None:
        """Set the home page to the current document's location."""
        if self._viewer.document.location:
            with update_configuration() as config:
                config.home_page = str(self._viewer.document.location)
            self.notify(
                f"Set to {self._viewer.document.location}",
                title="Home Page Set",
            )

    @work
    async def action_add_location_to_bookmarks_command(self) -> None:
        """Add the current document's location to the bookmarks."""
        if self._viewer.document.location and (
            title := await self.app.push_screen_wait(
                ModalInput(
                    "Bookmark title",
                    "",
                    sub_title=f"Bookmark for {self._viewer.document.location}",
                )
            )
        ):
            self._bookmarks.append(Bookmark(title, self._viewer.document.location))
            self.mutate_reactive(Main._bookmarks)
            save_bookmarks(self._bookmarks)
            self.notify(
                f"Added {self._viewer.document.location} to bookmarks",
                title="Bookmark Added",
            )

    def action_search_history_command(self) -> None:
        """Search the history."""
        HistorySearchCommands.navigation_history = self._navigation_history
        HistorySearchCommands.location_history = self._location_history
        self.show_palette(HistorySearchCommands)

    def action_search_bookmarks_command(self) -> None:
        """Search the bookmarks."""
        BookmarkSearchCommands.bookmarks = self._bookmarks
        self.show_palette(BookmarkSearchCommands)

    @work
    async def action_clear_cache_command(self) -> None:
        """Clear the cache."""
        if await self.app.push_screen_wait(
            Confirm(
                "Clear cache",
                "Are you sure you want to clear all cached content?",
            )
        ):
            self._cache.clear()
            self.notify("All cached content has been cleared.", title="Cache")


### main.py ends here
