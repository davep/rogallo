"""Provides the main screen."""

##############################################################################
# Python imports.
from argparse import Namespace
from collections.abc import Awaitable
from functools import partial
from subprocess import CalledProcessError, run
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
from textual.widgets import Footer
from textual.worker import get_current_worker

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import ChangeTheme, Command, Help, Quit
from textual_enhanced.dialogs import Confirm, ModalInput
from textual_enhanced.screen import EnhancedScreen
from textual_enhanced.tools import add_key

##############################################################################
# Textual file system picker imports.
from textual_fspicker import FileOpen, FileSave, Filters

##############################################################################
# Wasat imports.
from wasat import ClientCertificate, GeminiURI

##############################################################################
# Local imports.
from ... import __version__
from ...cache import ContentCache
from ...clients import Clients
from ...commands import (
    AboutThisPage,
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
    HandOffToOperatingSystem,
    JumpToCommandLine,
    JumpToDocument,
    JumpToSidebar,
    OpenFile,
    PipeDocument,
    Reload,
    SaveSource,
    SearchBookmarks,
    SearchHistory,
    SetHome,
    SetHomeToCurrentLocation,
    StripeLinks,
    ToggleANSIEscapeSequenceHandling,
    ToggleCosyLinkNumbers,
    ToggleEmojiRemoval,
    ToggleLinkNumbers,
    ToggleSidebar,
    ToggleView,
    ViewChangeLog,
)
from ...data import (
    Bookmark,
    Bookmarks,
    CommandLineHistory,
    LocationHistory,
    LocationVisit,
    NavigationHistory,
    NavigationPosition,
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
    update_configuration,
)
from ...input_content import InputContent
from ...messages import (
    BookmarksModified,
    ClientCertificatesModified,
    HistoryModified,
    OpenFromFileSystem,
    OpenLocation,
    OpenURI,
)
from ...preflight import has_navigable_path
from ...providers import BookmarkSearchCommands, HistorySearchCommands, MainCommands
from ...types import GEMINI_EXTENSIONS, SpartanURINeedingData
from ...widgets import (
    CommandLine,
    SidePanel,
    Toolbar,
    Viewer,
)
from ..about_page import AboutPage
from .handlers import handle_filesystem_request
from .local_messages import (
    CopyToClipboard,
    OpenDocument,
    OpenUnsupportedMIMEType,
    OpenUnsupportedURI,
)
from .request_builder import build_request
from .unsupported import maybe_open_unsupported_mime_type, maybe_open_unsupported_uri
from .uri_resolver import uri_resolver


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

        SidePanel {
            display: none;
        }
        &.--side-panel SidePanel {
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
        AboutThisPage,
        AddLocationToBookmarks,
        ChangeCommandLineLocation,
        ChangeTheme,
        ClearCache,
        CopyDocumentToClipboard,
        CopyLocationToClipboard,
        GoHome,
        GoToParent,
        GoToRoot,
        HandOffToOperatingSystem,
        JumpToCommandLine,
        JumpToDocument,
        JumpToSidebar,
        OpenFile,
        PipeDocument,
        Reload,
        SaveSource,
        SetHome,
        SetHomeToCurrentLocation,
        StripeLinks,
        ToggleANSIEscapeSequenceHandling,
        ToggleCosyLinkNumbers,
        ToggleEmojiRemoval,
        ToggleLinkNumbers,
        ToggleSidebar,
        ToggleView,
        ViewChangeLog,
    ]

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)
    COMMANDS = {MainCommands}
    AUTO_FOCUS = "CommandLine Input"

    _viewer = query_one(Viewer)
    """The viewer widget."""
    _command_line = query_one(CommandLine)
    """The command line widget."""
    _sidepanel = query_one(SidePanel)
    """The side panel widget."""

    _location_history: var[LocationHistory] = var(LocationHistory)
    """The location history."""
    _navigation_history: var[NavigationHistory] = var(NavigationHistory)
    """The navigation history."""
    _command_history: var[CommandLineHistory] = var(CommandLineHistory)
    """The command line history."""
    _bookmarks: var[Bookmarks] = var(list)
    """The bookmarks."""
    _client_certificates: var[list[ClientCertificate]] = var(list)
    """The client certificates."""
    _sidepanel_visible: var[bool] = var(False, toggle_class="--side-panel")
    """Whether the side panel is visible."""

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
        self._clients = Clients.create()
        """The clients for the supported protocols."""

    def _watch__sidepanel_visible(self) -> None:
        """Watch for changes to the side panel visibility."""
        with update_configuration() as config:
            config.sidepanel_visible = self._sidepanel_visible

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        with VerticalGroup():
            if load_configuration().toolbar_visible:
                yield Toolbar(
                    buttons=load_configuration().toolbar_contents,
                    commands=Main.COMMAND_MESSAGES,
                    version=__version__,
                    can_focus=load_configuration().toolbar_can_get_focus,
                    show_tooltips=load_configuration().toolbar_tooltips,
                )
            with Workspace():
                yield Viewer().data_bind(location_history=Main._location_history)
                yield SidePanel(self._clients.gemini.client_cert_store).data_bind(
                    bookmarks=Main._bookmarks,
                    client_certificates=Main._client_certificates,
                    location_history=Main._location_history,
                    navigation_history=Main._navigation_history,
                )
            yield CommandLine().data_bind(
                history=Main._command_history,
                location_history=Main._location_history,
                navigation_history=Main._navigation_history,
                bookmarks=Main._bookmarks,
            )
        if load_configuration().footer_visible:
            yield Footer()

    def _navigation_changed(self) -> None:
        """Handle changes to the navigation history."""
        self.mutate_reactive(Main._navigation_history)
        save_naviagation_history(self._navigation_history.clone().truncate())

    async def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self._command_history = load_command_history()
        self._location_history = load_location_history()
        self._navigation_history = load_navigation_history()
        self._bookmarks = load_bookmarks()
        self._client_certificates = (
            await self._clients.gemini.client_cert_store.list_certificates()
        )
        config = load_configuration()
        self._sidepanel_visible = config.sidepanel_visible
        self._sidepanel.dock_right = config.sidepanel_on_right
        self._command_line.dock_top = config.command_line_on_top
        if self._clients.gemini.trust_store:
            self._command_line.known_hosts = [
                GeminiURI.with_default_scheme(f"{host}:{port}")
                for host, port in await self._clients.gemini.trust_store.get_hosts()
            ]
            HistorySearchCommands.known_hosts = self._command_line.known_hosts
        self._viewer.stripe_links = config.stripe_links
        self._viewer.with_link_numbers = config.with_link_jumps
        self._viewer.handle_ansi_escape_sequences = config.handle_ansi_escape_sequences
        self._viewer.strip_emoji = config.strip_emoji
        self._viewer.cosy_link_numbers = config.cosy_link_jumps
        if self._arguments.command == "open" and (
            location := getattr(self._arguments, "location", None)
        ):
            self.post_message(OpenURI(location))
        elif self._navigation_history.current_item:
            self.post_message(
                OpenLocation(
                    self._navigation_history.current_item.location,
                    from_history=True,
                )
            )
        # Wait a few moments to do housekeeping, because by then the user is
        # probably reading something. For... reasons I guess.
        self.set_timer(5, self._housekeeping, name="housekeeping")

    async def on_unmount(self) -> None:
        """Called when the screen is unmounted."""
        await self._clients.close()

    @work(thread=True)
    def _housekeeping(self) -> None:
        """Perform housekeeping tasks."""
        self._cache.expire(lambda: get_current_worker().is_cancelled)

    def _set_last_input(self, input_content: InputContent | None) -> None:
        """Set the last user input.

        Args:
            input_content: The last user input.
        """
        self._last_user_input = input_content

    def _get_last_input(self) -> InputContent | None:
        """Get the last user input.

        Returns:
            The last user input.
        """
        return self._last_user_input

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
        if action in (
            JumpToDocument.action_name(),
            AboutThisPage.action_name(),
            SaveSource.action_name(),
        ):
            return bool(self._viewer.document)
        if action == JumpToCommandLine.action_name():
            return not self._command_line.has_control
        if action == Backward.action_name():
            return self._navigation_history.can_go_backward or None
        if action == Forward.action_name():
            return self._navigation_history.can_go_forward or None
        if action == SearchHistory.action_name():
            return (
                len(self._location_history) > 0
                or len(self._navigation_history) > 0
                or len(HistorySearchCommands.known_hosts) > 0
                or None
            )
        if action == SearchBookmarks.action_name():
            return len(self._bookmarks) > 0 or None
        if action in (
            CopyLocationToClipboard.action_name(),
            HandOffToOperatingSystem.action_name(),
            Reload.action_name(),
            SetHomeToCurrentLocation.action_name(),
        ):
            return bool(self._viewer.document.location)
        if action in (
            CopyDocumentToClipboard.action_name(),
            PipeDocument.action_name(),
        ):
            return bool(self._viewer.document)
        if action == ToggleView.action_name():
            return bool(self._viewer.document) and self._viewer.can_view_source
        if action == GoHome.action_name():
            return bool(load_configuration().home_page.strip())
        if action == AddLocationToBookmarks.action_name():
            return bool(self._viewer.document.location) and (
                self._viewer.document.location not in self._bookmarks
            )
        if action == GoToParent.action_name():
            return (
                has_navigable_path(self._viewer.document.location)
                and self._viewer.document.location.parent
                != self._viewer.document.location
            )
        if action == GoToRoot.action_name():
            return (
                has_navigable_path(self._viewer.document.location)
                and self._viewer.document.location.root
                != self._viewer.document.location
            )
        return True

    def _remember_last_visit(self, request: OpenDocument) -> None:
        """Remember the last visit to a location.

        Args:
            request: The request to remember the visit for.
        """
        if (location := request.document.location) is None:
            return
        if isinstance(location, SpartanURINeedingData):
            # Spartan URIs that need data are not remembered in history
            # because they're not useful locations without the data.
            return
        self._location_history.add(LocationVisit(location))
        self.mutate_reactive(Main._location_history)
        save_location_history(self._location_history)

    @on(Viewer.DocumentLoaded)
    def _document_loaded(self) -> None:
        """Handle a document being loaded in the viewer.

        Args:
            message: The message containing the document that was loaded.
        """
        self.refresh_bindings()
        self._viewer.take_control()
        if self._navigation_history.current_item:
            self._viewer.jump = self._navigation_history.current_item.focused_link

    @on(OpenDocument)
    def open_document(self, message: OpenDocument) -> None:
        """Open a document in the viewer.

        Args:
            message: The message containing the document to open.
        """
        if (
            message.document.location
            and not message.document.avoid_history
            and not message.from_history
        ):
            # Add this new document to the end of the navigation history.
            # This ensures that we know where "here" is right now. Also
            # force a save to storage so if we resume we're back on this
            # page. Note that only the location is saved, there's no focused
            # link to care about yet.
            self._navigation_history.add(NavigationPosition(message.document.location))
            self._navigation_changed()
        self._remember_last_visit(message)
        self._viewer.document = message.document

    @work(exclusive=True)
    async def _make_request(self, handler: Awaitable[None]) -> None:
        """Make a request to a server.

        Args:
            handler: The handler to use for the request.
        """
        with self._command_line.busy_spinner():
            await handler

    @work(thread=True)
    def _load_from_filesystem(self, request: OpenLocation) -> None:
        """Load a document from the filesystem.

        Args:
            request: The request to load the document from.
        """
        handle_filesystem_request(request, self)

    @on(OpenLocation)
    def open_location(self, message: OpenLocation) -> None:
        """Open a location in the viewer.

        Args:
            message: The message the location open request.
        """
        if (
            request := build_request(
                cache=self._cache,
                clients=self._clients,
                current_document=self._viewer.document,
                message=message,
                owner=self,
                set_last_input=self._set_last_input,
                get_last_input=self._get_last_input,
            )
        ) is not None:
            self._make_request(request)
        else:
            self._load_from_filesystem(message)

    @on(OpenURI)
    def open_uri(self, message: OpenURI) -> None:
        """Open a URI in the viewer.

        Args:
            message: The message containing the URI to open.
        """
        if (
            position := self._viewer.navigation_position
        ) and not self._viewer.document.avoid_history:
            # We're about to head somewhere else, which suggests that we've
            # navigated via a link. So here we seek to replace the current
            # head of the history with a fresh version that also records the
            # focused link. It is possible we're navigating away because
            # someone entered a fresh URI, etc, which means we'll be saving
            # a link ID that wasn't used. This is fine, there's no downside
            # to that.
            self._navigation_history.add_or_replace(position)
            self._navigation_changed()
        self.post_message(uri_resolver(message))

    @on(OpenUnsupportedURI)
    @work
    async def _open_unsupported_uri(self, message: OpenUnsupportedURI) -> None:
        """Maybe open an unsupported URI in the system's web browser.

        Args:
            message: The message containing the unsupported URI.
        """
        await maybe_open_unsupported_uri(message, self)

    @on(OpenUnsupportedMIMEType)
    @work
    async def _open_unsupported_mime_type(
        self, message: OpenUnsupportedMIMEType
    ) -> None:
        """Open an unsupported MIME typed location in the system's web browser.

        Args:
            message: The message containing the unsupported MIME type.
        """
        await maybe_open_unsupported_mime_type(message, self)

    @on(OpenFromFileSystem)
    @work
    async def _open_from_filesystem(self, message: OpenFromFileSystem) -> None:
        """Open a file."""
        if chosen_file := await self.app.push_screen_wait(
            FileOpen(
                message.start_from,
                title="Open a file to view",
                filters=Filters(
                    ("Gemtext", lambda path: path.suffix.lower() in GEMINI_EXTENSIONS),
                    ("All files", lambda _: True),
                ),
                cancel_button=partial(add_key, key="Esc", context=self),
            )
        ):
            self.post_message(OpenLocation(chosen_file))

    @on(CommandLine.CommandExecuted)
    def _save_command_line_history(self, message: CommandLine.CommandExecuted) -> None:
        """Save the command line history when a command is executed.

        Args:
            message: The message containing the command that was executed.
        """
        self.mutate_reactive(Main._command_history)
        save_command_history(message.command_line.history)

    @on(HistoryModified)
    def _save_location_history(self) -> None:
        """Save the location history when it is modified.

        Args:
            message: The message containing the modified history.
        """
        self.mutate_reactive(Main._location_history)
        save_location_history(self._location_history)

    @on(BookmarksModified)
    def _save_bookmarks(self) -> None:
        """Save the bookmarks when they are modified.

        Args:
            message: The message containing the modified bookmarks.
        """
        self.mutate_reactive(Main._bookmarks)
        save_bookmarks(self._bookmarks)

    @on(ClientCertificatesModified)
    async def _refresh_known_client_certificates(self) -> None:
        """Refresh the known client certificates when they are modified."""
        self._client_certificates = (
            await self._clients.gemini.client_cert_store.list_certificates()
        )

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
        if self.screen.focused and (self._sidepanel in self.screen.focused.ancestors):
            self._sidepanel_visible = False
            return
        if not self._sidepanel_visible:
            self._sidepanel_visible = True
        self._sidepanel.focus()

    def action_toggle_sidebar_command(self) -> None:
        """Toggle the sidebar."""
        self._sidepanel_visible = not self._sidepanel_visible

    def action_backward_command(self) -> None:
        """Go backward in the navigation history."""
        if (
            self._navigation_history.backward()
            and self._navigation_history.current_item
        ):
            self.post_message(
                OpenLocation(
                    self._navigation_history.current_item.location,
                    from_history=True,
                )
            )
            self._navigation_changed()

    def action_forward_command(self) -> None:
        """Go forward in the navigation history."""
        if self._navigation_history.forward() and self._navigation_history.current_item:
            self.post_message(
                OpenLocation(
                    self._navigation_history.current_item.location,
                    from_history=True,
                )
            )
            self._navigation_changed()

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
        if self._viewer.can_view_source:
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

    def action_toggle_cosy_link_numbers_command(self) -> None:
        """Toggle cosy link numbers."""
        self._viewer.cosy_link_numbers = not self._viewer.cosy_link_numbers
        with update_configuration() as config:
            config.cosy_link_jumps = self._viewer.cosy_link_numbers

    def action_go_to_parent_command(self) -> None:
        """Go to the parent of the current document's location."""
        if (
            has_navigable_path(location := self._viewer.document.location)
            and location.parent != location
        ):
            self.post_message(OpenLocation(location.parent))

    def action_go_to_root_command(self) -> None:
        """Go to the root of the current document's location."""
        if (
            has_navigable_path(location := self._viewer.document.location)
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

    def action_open_file_command(self) -> None:
        """Open a file."""
        self.post_message(OpenFromFileSystem())

    def action_about_this_page_command(self) -> None:
        """Show information about the current page."""
        if self._viewer.document.location:
            self.app.push_screen(AboutPage(self._viewer.document))

    @work
    async def action_pipe_document_command(self) -> None:
        """Pipe the current document to a command."""
        if self._viewer.document and (
            command := await self.app.push_screen_wait(
                ModalInput(
                    "Shell command/pipeline to pipe the document through",
                    title="Pipe the document through a command",
                )
            )
        ):
            try:
                with self.app.suspend():
                    run(
                        command,
                        input=self._viewer.document.content,
                        text=True,
                        shell=True,
                        encoding="utf-8",
                    )
            except CalledProcessError as error:
                self.notify(
                    f"Command failed with exit code {error.returncode}",
                    severity="error",
                )
            except BrokenPipeError:
                self.notify(
                    "Process closed pipe before input was fully written",
                    severity="warning",
                )

    def action_view_change_log_command(self) -> None:
        """View the change log."""
        self.post_message(OpenURI("gemini://tilde.team/~davep/rogallo/changelog.gmi"))

    def action_hand_off_to_operating_system_command(self) -> None:
        """Hand off the current document's location to the operating system."""
        if self._viewer.document.location:
            open_in_browser(str(self._viewer.document.location))

    @work
    async def action_save_source_command(self) -> None:
        """Save the current document's source to a file."""
        if self._viewer.document and (
            target := await self.app.push_screen_wait(
                FileSave(
                    default_file=self._viewer.document.suggested_filename,
                    title="Save source to file",
                    cancel_button=partial(add_key, key="Esc", context=self),
                )
            )
        ):
            try:
                target.write_text(self._viewer.document.content, encoding="utf-8")
                self.notify(f"Saved to {target}", title="Save Source")
            except OSError as error:
                self.notify(
                    f"Unable to save to {target}:\n\n{error}",
                    severity="error",
                    title="Save Source Error",
                )


### main.py ends here
