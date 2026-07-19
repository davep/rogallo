"""Provides the main screen."""

##############################################################################
# Python imports.
from argparse import Namespace
from functools import partial
from mimetypes import guess_type
from pathlib import Path
from urllib.parse import urlparse
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
from textual_enhanced.tools import add_key

##############################################################################
# Textual file system picker imports.
from textual_fspicker import FileOpen, Filters

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
    GoToParent,
    GoToRoot,
    JumpToCommandLine,
    JumpToDocument,
    JumpToSidebar,
    OpenFile,
    Reload,
    SearchBookmarks,
    SearchHistory,
    SetHome,
    SetHomeToCurrentLocation,
    StripeLinks,
    ToggleANSIEscapeSequenceHandling,
    ToggleBookmarksManager,
    ToggleEmojiRemoval,
    ToggleHistoryManager,
    ToggleLinkNumbers,
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
    load_trusted_mime_types,
    load_trusted_schemes,
    save_bookmarks,
    save_command_history,
    save_location_history,
    save_naviagation_history,
    save_trusted_mime_types,
    save_trusted_schemes,
    trust_file,
    update_configuration,
)
from ..document import Document
from ..input_content import InputContent
from ..messages import (
    CopyToClipboard,
    OpenDocument,
    OpenLocation,
    OpenUnsupportedMIMEType,
    OpenUnsupportedURI,
    OpenURI,
)
from ..preflight import (
    is_likely_local_text_file,
    is_likely_schemeless_capsule,
    path_from_uri,
)
from ..providers import BookmarkSearchCommands, HistorySearchCommands, MainCommands
from ..widgets import BookmarksViewer, CommandLine, HistoryViewer, Viewer
from .certificate import Certificate
from .confirm_unsupported import ConfirmUnsupportedURI
from .user_input import UserInput


##############################################################################
class Workspace(HorizontalGroup):
    """A workspace for the main screen."""

    DEFAULT_CSS = """
    Workspace {
        height: 1fr;
    }
    """

    DEFAULT_CLASSES = "dead-space"

    BINDINGS = [("escape", "screen.jump_to_command_line_command")]


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

        .dead-space {
            hatch: right $surface;
        }

        * {
            scrollbar-background: $surface;
            scrollbar-background-hover: $surface;
            scrollbar-background-active: $surface;
        }

        *:focus, *:focus-within {
            scrollbar-background: $panel 80%;
            scrollbar-background-hover: $panel 80%;
            scrollbar-background-active: $panel 80%;
        }

        .panel {
            border-left: solid $panel;
            background: $surface;
            &:focus, &:focus-within {
                border-left: solid $border;
                background: $panel 80%;
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
        SearchHistory,
        SearchBookmarks,
        Backward,
        Forward,
        Quit,
        # Everything else.
        AddLocationToBookmarks,
        ChangeCommandLineLocation,
        ChangeTheme,
        ClearCache,
        CopyDocumentToClipboard,
        CopyLocationToClipboard,
        GoHome,
        GoToParent,
        GoToRoot,
        JumpToCommandLine,
        JumpToDocument,
        JumpToSidebar,
        OpenFile,
        Reload,
        SetHome,
        SetHomeToCurrentLocation,
        StripeLinks,
        ToggleANSIEscapeSequenceHandling,
        ToggleBookmarksManager,
        ToggleEmojiRemoval,
        ToggleHistoryManager,
        ToggleLinkNumbers,
        ToggleView,
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
        self._trusted_schemes = load_trusted_schemes()
        """The trusted schemes."""
        self._trusted_mime_types = load_trusted_mime_types()
        """The trusted MIME types."""
        self._last_user_input: InputContent | None = None
        """The last user input."""
        self._client = Client(
            verify_mode="tofu",
            trust_store_path=trust_file(),
            client_cert_store_path=client_certificates_directory(),
            connect_timeout=load_configuration().connection_timeout,
            read_timeout=load_configuration().read_timeout,
            max_redirects=load_configuration().maximum_redirects,
        )
        """The Gemini client."""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with VerticalGroup():
            with Workspace():
                yield Viewer().data_bind(location_history=Main._location_history)
                with VerticalGroup(id="history"):
                    yield Label("History")
                    yield HistoryViewer().data_bind(history=Main._location_history)
                with VerticalGroup(id="bookmarks"):
                    yield Label("Bookmarks")
                    yield BookmarksViewer().data_bind(bookmarks=Main._bookmarks)
            yield CommandLine().data_bind(
                history=Main._command_history,
                location_history=Main._location_history,
                navigation_history=Main._navigation_history,
                bookmarks=Main._bookmarks,
            )
        yield Footer()

    async def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self._command_history = load_command_history()
        self._location_history = load_location_history()
        self._navigation_history = load_navigation_history()
        self._bookmarks = load_bookmarks()
        config = load_configuration()
        self._command_line.dock_top = config.command_line_on_top
        if self._client.trust_store:
            self._command_line.known_hosts = [
                GeminiURI.with_default_scheme(f"{host}:{port}")
                for host, port in await self._client.trust_store.get_hosts()
            ]
            HistorySearchCommands.known_hosts = self._command_line.known_hosts
        self._history_visible = config.history_visible
        self._bookmarks_visible = config.bookmarks_visble
        self._viewer.stripe_links = config.stripe_links
        self._viewer.with_link_numbers = config.with_link_jumps
        self._viewer.handle_ansi_escape_sequences = config.handle_ansi_escape_sequences
        self._viewer.strip_emoji = config.strip_emoji
        if self._arguments.command == "open" and (
            location := getattr(self._arguments, "location", None)
        ):
            self.post_message(OpenURI(location))
        elif self._location_history.current_item:
            self.post_message(
                OpenLocation(
                    self._location_history.current_item.location,
                    do_not_record_in_history=True,
                )
            )

    async def on_unmount(self) -> None:
        """Called when the screen is unmounted."""
        await self._client.close()

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
        if action == ToggleHistoryManager.action_name():
            return len(self._location_history) > 0 or None
        if action == SearchHistory.action_name():
            return (
                len(self._location_history) > 0
                or len(self._navigation_history) > 0
                or len(HistorySearchCommands.known_hosts) > 0
                or None
            )
        if action in (
            ToggleBookmarksManager.action_name(),
            SearchBookmarks.action_name(),
        ):
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
        if action == GoToParent.action_name():
            return (
                bool(self._viewer.document.location)
                and isinstance(self._viewer.document.location, GeminiURI)
                and self._viewer.document.location.parent
                != self._viewer.document.location
            )
        if action == GoToRoot.action_name():
            return (
                bool(self._viewer.document.location)
                and isinstance(self._viewer.document.location, GeminiURI)
                and self._viewer.document.location.root
                != self._viewer.document.location
            )
        return True

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
        initial_input = ""
        if self._last_user_input and self._last_user_input == InputContent(
            location=location, prompt=prompt, sensitive=sensitive
        ):
            initial_input = self._last_user_input.content
        if user_input := await self.app.push_screen_wait(
            UserInput(
                location, prompt=prompt, sensitive=sensitive, default=initial_input
            )
        ):
            try:
                self.post_message(
                    OpenLocation(
                        location=location.with_query(user_input),
                        allow_cached=False,
                        associated_input=InputContent(
                            location=location,
                            prompt=prompt,
                            sensitive=sensitive,
                            content=user_input,
                        ),
                    )
                )
            except URIError as error:
                self.notify(
                    f"Unable to create query for {location}:\n\n{error}",
                    severity="error",
                    title="Input Error",
                )

    async def _handle_client_certificate_request(
        self, location: GeminiURI, request_reason: str
    ) -> None:
        """Handle a request for a client certificate from a Gemini request.

        Args:
            location: The location making the request.
            request_reason: The reason for the client certificate request.
        """
        if (
            certificate_data := await self.app.push_screen_wait(
                Certificate(location, request_reason)
            )
        ) is None:
            self.notify("Client certificate request cancelled.", severity="warning")
            return
        try:
            await self._client.client_cert_store.create_credentials(**certificate_data)
        except (ValueError, OSError, RuntimeError) as error:
            self.notify(
                f"Unable to create client certificate for {location}:\n\n{error}",
                severity="error",
                title="Client Certificate Error",
            )
            return
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
                uri,
                response.meta.strip(),
                response.status is StatusCode.SENSITIVE_INPUT,
            )
            return

        # Handle a request for a client certificate.
        if response.status.is_client_certificate_required:
            await self._handle_client_certificate_request(uri, response.meta.strip())
            return

        # Handle any other non-successful response.
        if not response.status.is_success:
            self._last_user_input = request.associated_input
            self.notify(
                f"Error loading {uri}:\n\n{response.status.value} {response.status.name}\n{response.meta}",
                severity="error",
                title="Request Error",
            )
            return

        # Clear out any saved input.
        self._last_user_input = None

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
                            needed_certificate=response.client_cert_used,
                        )
                    ),
                    original_request=request,
                )
            )
        else:
            self.post_message(OpenUnsupportedMIMEType(uri, response.mime_type))

    def _maybe_remember_location(self, request: OpenDocument) -> None:
        """Remember a location in the history.

        Args:
            request: The request to open text for. This is used to determine
                the location to remember.
        """
        if (location := request.document.location) is None:
            return
        self._location_history.add(LocationVisit(location))
        self.mutate_reactive(Main._location_history)
        save_location_history(self._location_history)
        if (
            not request.original_request.do_not_record_in_history
            and self._navigation_history.current_item
            != request.document.original_location
        ):
            self._navigation_history.add(location)
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
            self._last_user_input = request.associated_input
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
        mime_type = guess_type(request.location)[0] or "application/octet-stream"
        if not self._is_displayable(mime_type):
            self.post_message(OpenUnsupportedMIMEType(request.location, mime_type))
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
            self.post_message(
                OpenLocation(GeminiURI(message.uri), allow_cached=message.allow_cached)
            )
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
            self.post_message(
                OpenLocation(
                    GeminiURI.with_default_scheme(message.uri),
                    allow_cached=message.allow_cached,
                )
            )
            return

        # Otherwise, try to open it in the system browser.
        self.post_message(OpenUnsupportedURI(message.uri))

    @on(OpenUnsupportedURI)
    @work
    async def _open_unsupported_uri(self, message: OpenUnsupportedURI) -> None:
        """Maybe open an unsupported URI in the system's web browser.

        Args:
            message: The message containing the unsupported URI.
        """

        # Because we want to gatekeep which schemes get passed on, let's
        # grab the scheme.
        try:
            scheme = urlparse(message.uri).scheme.lower()
        except ValueError:
            return

        # If there's no scheme, let's GTFO.
        if not scheme:
            self.notify(
                f"Unable to open {message.uri}: no scheme found", severity="error"
            )
            return

        # If the scheme isn't trusted, let's see what the user wants to do about it.
        if not (open_uri := scheme in self._trusted_schemes):
            match await self.app.push_screen_wait(
                ConfirmUnsupportedURI(
                    message.uri,
                    f"The scheme '{scheme}' is not supported by Rogallo. "
                    "Do you want to open the URI in your external browser?",
                )
            ):
                case "once":
                    open_uri = True
                case "always":
                    open_uri = True
                    self._trusted_schemes.add(scheme)
                    save_trusted_schemes(self._trusted_schemes)

        # At this point, if the user has consented to opening the URI based
        # on the scheme, let's do it.
        if open_uri:
            open_in_browser(message.uri)

    @on(OpenUnsupportedMIMEType)
    @work
    async def _open_unsupported_mime_type(
        self, message: OpenUnsupportedMIMEType
    ) -> None:
        """Open an unsupported MIME typed location in the system's web browser.

        Args:
            message: The message containing the unsupported MIME type.
        """

        # If the MIME type isn't trusted, let's see what the user wants to
        # do about it.
        if not (open_uri := message.mime_type in self._trusted_mime_types):
            match await self.app.push_screen_wait(
                ConfirmUnsupportedURI(
                    str(message.location),
                    f"The MIME type '{message.mime_type}' is not supported by Rogallo. "
                    "Do you want to open the location in your external browser?",
                )
            ):
                case "once":
                    open_uri = True
                case "always":
                    open_uri = True
                    self._trusted_mime_types.add(message.mime_type)
                    save_trusted_mime_types(self._trusted_mime_types)

        # At this point, if the user has consented to opening the location
        # based on the MIME type, let's do it.
        if open_uri:
            open_in_browser(
                str(message.location)
                if isinstance(message.location, GeminiURI)
                else message.location.resolve().as_uri()
            )

    @on(CommandLine.CommandExecuted)
    def _save_command_line_history(self, message: CommandLine.CommandExecuted) -> None:
        """Save the command line history when a command is executed.

        Args:
            message: The message containing the command that was executed.
        """
        self.mutate_reactive(Main._command_history)
        save_command_history(message.command_line.history)

    @on(HistoryViewer.HistoryModified)
    def _save_location_history(self) -> None:
        """Save the location history when it is modified.

        Args:
            message: The message containing the modified history.
        """
        self.mutate_reactive(Main._location_history)
        save_location_history(self._location_history)

    @on(BookmarksViewer.BookmarksModified)
    def _save_bookmarks(self) -> None:
        """Save the bookmarks when they are modified.

        Args:
            message: The message containing the modified bookmarks.
        """
        self.mutate_reactive(Main._bookmarks)
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

    @on(ChangeTheme)
    async def _change_theme(self) -> None:
        """Handle the change theme action."""
        await self.run_action("change_theme_command")

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
                OpenLocation(
                    self._navigation_history.current_item, do_not_record_in_history=True
                )
            )
            self.mutate_reactive(Main._navigation_history)

    def action_forward_command(self) -> None:
        """Go forward in the navigation history."""
        if self._navigation_history.forward() and self._navigation_history.current_item:
            self.post_message(
                OpenLocation(
                    self._navigation_history.current_item, do_not_record_in_history=True
                )
            )
            self.mutate_reactive(Main._navigation_history)

    def action_toggle_history_manager_command(self) -> None:
        """Toggle the visibility of the history manager panel."""
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

    def action_toggle_bookmarks_manager_command(self) -> None:
        """Toggle the visibility of the bookmarks manager panel."""
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
                    do_not_record_in_history=True,
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

    def action_stripe_links_command(self) -> None:
        """Toggle link striping."""
        self._viewer.stripe_links = not self._viewer.stripe_links
        with update_configuration() as config:
            config.stripe_links = self._viewer.stripe_links

    def action_toggle_link_numbers_command(self) -> None:
        """Toggle link numbers."""
        self._viewer.with_link_numbers = not self._viewer.with_link_numbers
        with update_configuration() as config:
            config.with_link_jumps = self._viewer.with_link_numbers

    def action_go_to_parent_command(self) -> None:
        """Go to the parent of the current document's location."""
        if (
            isinstance(location := self._viewer.document.location, GeminiURI)
            and location.parent != location
        ):
            self.post_message(OpenLocation(location.parent))

    def action_go_to_root_command(self) -> None:
        """Go to the root of the current document's location."""
        if (
            isinstance(location := self._viewer.document.location, GeminiURI)
            and location.root != location
        ):
            self.post_message(OpenLocation(location.root))

    def action_toggle_emoji_removal_command(self) -> None:
        """Toggle emoji removal."""
        self._viewer.strip_emoji = not self._viewer.strip_emoji
        with update_configuration() as config:
            config.strip_emoji = self._viewer.strip_emoji

    def action_toggle_ansi_escape_sequence_handling_command(self) -> None:
        """Toggle ANSI escape sequence handling."""
        self._viewer.handle_ansi_escape_sequences = (
            not self._viewer.handle_ansi_escape_sequences
        )
        with update_configuration() as config:
            config.handle_ansi_escape_sequences = (
                self._viewer.handle_ansi_escape_sequences
            )

    @work
    async def action_open_file_command(self) -> None:
        """Open a file."""
        if chosen_file := await self.app.push_screen_wait(
            FileOpen(
                filters=Filters(
                    ("Gemtext", lambda path: path.suffix.lower() == ".gmi"),
                    ("All files", lambda _: True),
                ),
                cancel_button=partial(add_key, key="Esc", context=self),
            )
        ):
            self.post_message(OpenLocation(chosen_file))


### main.py ends here
