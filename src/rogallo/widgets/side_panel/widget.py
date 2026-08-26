"""The main container widget for the side-panel."""

##############################################################################
# Python imports.
from typing import Self

##############################################################################
# Textual imports.
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
from ...data import Bookmarks, LocationHistory, NavigationHistory
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

        #tabs-list {
            background: $panel;
        }
    }
    """

    DEFAULT_CLASSES = "panel"

    BINDINGS = [
        ("escape", "bounce_out"),
        ("down", "dig_in"),
        HelpfulBinding(
            "ctrl+left",
            "switch('previous_tab')",
            tooltip="Move to the previous side panel tab",
        ),
        HelpfulBinding(
            "ctrl+right",
            "switch('next_tab')",
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
            with TabPane("Bookmarks"):
                yield BookmarksViewer().data_bind(SidePanel.bookmarks)
            with TabPane("History"):
                yield HistoryViewer().data_bind(history=SidePanel.location_history)
            with TabPane("Client Certificates"):
                yield ClientCertificateManager(
                    self._client_certificate_store
                ).data_bind(
                    bookmarks=SidePanel.bookmarks,
                    client_certificates=SidePanel.client_certificates,
                    location_history=SidePanel.location_history,
                    navigation_history=SidePanel.navigation_history,
                )

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

    async def action_switch(self, switcher: str) -> None:
        await self.query_one(Tabs).run_action(switcher)
        self.call_after_refresh(self.run_action, "dig_in")


### widget.py ends here
