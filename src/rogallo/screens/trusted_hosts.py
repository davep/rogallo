"""Provides a screen for browsing and managing trusted hosts."""

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.getters import query_one
from textual.screen import ModalScreen
from textual.widgets import Button
from textual.widgets.option_list import Option

##############################################################################
# Textual enhanced imports.
from textual_enhanced.dialogs import Confirm
from textual_enhanced.tools import add_key
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Wasat imports.
from wasat import GeminiURI, TrustStore


##############################################################################
class KnownHost(Option):
    """An option representing a known host."""

    def __init__(self, host: str, port: int) -> None:
        """Initialise the option.

        Args:
            host: The host name.
            port: The port number.
        """
        super().__init__(f"{host}[dim italic]:{port}[/]")
        self._host = host
        """The host name."""
        self._port = port
        """The port number."""

    @property
    def host(self) -> str:
        """The host name."""
        return self._host

    @property
    def port(self) -> int:
        """The port number."""
        return self._port

    @property
    def uri(self) -> GeminiURI:
        """The URI for the known host."""
        return GeminiURI.with_default_scheme(self._host).with_port(self._port)


##############################################################################
class TrustedHostsBrowser(ModalScreen[None | GeminiURI]):
    """A modal screen to browse and manage trusted hosts."""

    CSS = """
    TrustedHostsBrowser {
        align: center middle;

        &> HorizontalGroup {
            width: 60%;
            height: auto;
            max-height: 80%;
            background: $panel;
            border: panel $border;
            EnhancedOptionList {
                height: 1fr;
                width: 1fr;
                margin: 1 1 0 1;
                &, &:focus {
                    border: none;
                }
            }
            #buttons {
                padding: 1 2;
                height: auto;
                width: auto;
                Button {
                    margin-bottom: 1;
                }
            }
        }
    }
    """

    BINDINGS = [
        ("f", "forget", "Forget"),
        ("escape", "close", "Close"),
    ]

    _host_list = query_one(EnhancedOptionList)
    """The list of trusted hosts."""

    def __init__(self, trust_store: TrustStore) -> None:
        """Initialise the screen.

        Args:
            client: The Gemini client.
        """
        super().__init__()
        self._trust_store = trust_store
        """The trust store to manage."""

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with HorizontalGroup() as dialog:
            dialog.border_title = "Trusted Hosts"
            yield EnhancedOptionList()
            with VerticalGroup(id="buttons"):
                yield Button(
                    add_key("Visit", "Enter", self), id="visit", variant="primary"
                )
                yield Button(add_key("Forget", "f", self), id="forget", variant="error")
                yield Button(
                    add_key("Close", "Esc", self), id="close", variant="primary"
                )

    async def on_mount(self) -> None:
        """Called when the screen is mounted."""
        with self._host_list.preserved_highlight:
            self._host_list.add_options(
                KnownHost(*host) for host in sorted(await self._trust_store.get_hosts())
            )

    @on(Button.Pressed, "#visit")
    @on(EnhancedOptionList.OptionSelected)
    def action_visit(self) -> None:
        """Visit the selected host."""
        if self._host_list.highlighted is not None:
            known_host = self._host_list.get_option_at_index(
                self._host_list.highlighted
            )
            assert isinstance(known_host, KnownHost)
            self.dismiss(known_host.uri)

    @on(Button.Pressed, "#forget")
    @work
    async def action_forget(self) -> None:
        """Forget the selected host."""
        if self._host_list.highlighted is not None:
            known_host = self._host_list.get_option_at_index(
                self._host_list.highlighted
            )
            assert isinstance(known_host, KnownHost)
            if await self.app.push_screen_wait(
                Confirm(
                    f"Forget {known_host.host}:{known_host.port}?",
                    "Are you sure you want to forget the selected host?",
                )
            ):
                await self._trust_store.forget(known_host.host, known_host.port)
                with self._host_list.preserved_highlight:
                    self._host_list.remove_option_at_index(self._host_list.highlighted)

    @on(Button.Pressed, "#close")
    def action_close(self) -> None:
        """Close the screen."""
        self.dismiss(None)


### trusted_hosts.py ends here
