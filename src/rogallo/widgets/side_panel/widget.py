"""The main container widget for the side-panel."""

##############################################################################
# Python imports.
from typing import Literal, Self

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.getters import query_one
from textual.reactive import var
from textual.widgets import TabbedContent, TabPane, Tabs

##############################################################################
# Textual enhanced imports.
from textual_enhanced.binding import HelpfulBinding

##############################################################################
# Wasat imports.
from wasat import ClientCertificate, ClientCertificateStore

##############################################################################
# Local imports.
from ...commands import JumpToCommandLine
from ...data import (
    Bookmarks,
    LocationHistory,
    NavigationHistory,
    load_configuration,
    update_configuration,
)
from ...document import Document
from .bookmarks import BookmarksViewer
from .client_certificates import ClientCertificateManager
from .history import HistoryViewer


##############################################################################
class SidePanel(Container):
    """The main container widget for the side-panel."""

    DEFAULT_CSS = """
    SidePanel {
        height: 1fr;
        width: 35%;
        min-width: 42;
        dock: left;

        &.--dock-right {
            dock: right;
        }

        #tabs-list, Tabs {
            background: transparent;
        }
    }
    """

    DEFAULT_CLASSES = "panel"

    BINDINGS = [
        ("escape", "bounce_out"),
        ("enter, down, j", "dig_in"),
        HelpfulBinding(
            "ctrl+left, h, left",
            "switch('previous')",
            priority=True,
            tooltip="Move to the previous side panel tab",
        ),
        HelpfulBinding(
            "ctrl+right, l, right",
            "switch('next')",
            priority=True,
            tooltip="Move to the next side panel tab",
        ),
    ]

    HELP = """
    ## The Side Panel

    Here you can manage your bookmarks, your location history, and client
    certificates.

    ### Useful keys
    """

    dock_right: var[bool] = var(False, toggle_class="--dock-right")
    """Should the panel dock to the right?"""

    location_history: var[LocationHistory] = var(LocationHistory)
    """The history of locations visited."""
    navigation_history: var[NavigationHistory] = var(NavigationHistory)
    """The history of navigation through locations."""
    bookmarks: var[Bookmarks] = var(list)
    """The bookmarks for the application."""
    client_certificates: var[list[ClientCertificate]] = var(list)
    """The client certificates for the application."""
    current_document: var[Document] = var(Document)
    """The current document being viewed."""

    _tabs = query_one(TabbedContent)
    """The tabbed content widget."""

    def __init__(self, client_certificate_store: ClientCertificateStore) -> None:
        """Initialise the side-panel.

        Args:
            client_certificate_store: The client certificate store to use.
        """
        super().__init__()
        self._client_certificate_store = client_certificate_store
        """The client certificate store to use."""

    def compose(self) -> ComposeResult:
        """Compose the side-panel."""
        with TabbedContent():
            with TabPane("Bookmarks", id="bookmarks"):
                yield BookmarksViewer().data_bind(SidePanel.bookmarks)
            with TabPane("History", id="history"):
                yield HistoryViewer().data_bind(history=SidePanel.location_history)
            with TabPane("Client Certificates", id="client-certificates"):
                yield ClientCertificateManager(
                    self._client_certificate_store
                ).data_bind(
                    bookmarks=SidePanel.bookmarks,
                    client_certificates=SidePanel.client_certificates,
                    current_document=SidePanel.current_document,
                    location_history=SidePanel.location_history,
                    navigation_history=SidePanel.navigation_history,
                )

    def on_mount(self) -> None:
        """Called when the side-panel is mounted."""
        try:
            self._tabs.active = load_configuration().side_panel_chosen_tab
        except Tabs.TabError:
            pass

    @on(TabbedContent.TabActivated)
    def _remember_chosen_tab(self) -> None:
        """Remember the active tab in the side-panel.

        Args:
            event: The tab activated event.
        """
        with update_configuration() as config:
            config.side_panel_chosen_tab = self._tabs.active

    def focus(self, scroll_visible: bool = True) -> Self:
        """Focus the first tab in the side-panel."""
        if self._tabs.active_pane is not None:
            self._tabs.active_pane.children[0].focus(scroll_visible=scroll_visible)
        return self

    async def action_bounce_out(self) -> None:
        """Bounce focus out of the side panel."""
        if self.screen.focused == (tabs := self.query_one(Tabs)):
            await self.screen.run_action(JumpToCommandLine.action_name())
        else:
            tabs.focus()

    def action_dig_in(self) -> None:
        """Dig focus into the side panel."""
        if (active := self.query_one(TabbedContent).active_pane) is not None:
            for widget in active.query("*"):
                if widget.can_focus:
                    widget.focus()
                    return

    async def action_switch(self, switcher: Literal["next", "previous"]) -> None:
        """Switch the active tab in the side-panel.

        Args:
            switcher: The switcher to use. Can be `next` or `previous`.
        """
        dig_in = self.screen.focused != (tabs := self.query_one(Tabs))
        await tabs.run_action(f"{switcher}_tab")
        if dig_in:
            self.call_after_refresh(self.run_action, "dig_in")


### widget.py ends here
