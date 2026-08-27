"""Provides the title widget for the viewer."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.events import Click
from textual.getters import query_one
from textual.reactive import var
from textual.widgets import Label

##############################################################################
# Wasat imports.
from wasat import VerificationMethod

##############################################################################
# Local imports.
from ...commands import AboutClientCertificate, AboutThisPage
from ...data import load_configuration
from ...types import RogalloLocation


##############################################################################
class ViewerTitle(Horizontal):
    """A widget for displaying the title of the viewer."""

    DEFAULT_CSS = """
    ViewerTitle {
        background: $panel;
        color: $foreground;
        height: 1;
        padding: 0 1;

        #verification-method, #lock-icon {
            width: 2;
            padding-right: 1;
        }

        #verification-method, #lock-icon {
            pointer: pointer;
        }

        .--verified-ca, #lock-icon {
            color: $text-success;
        }
        .--verified-tofu {
            color: $text-warning;
        }
        .--verified-off, .--verified-none {
            color: $text-error;
        }

        #location {
            width: 1fr;
            content-align: right middle;
        }
    }
    """

    location: var[RogalloLocation | None] = var(None, always_update=True)
    """The location to display."""
    verification_method: var[VerificationMethod | None] = var(None)
    """The verification method used for the connection."""
    needed_certificate: var[bool] = var(False)
    """Whether the location needed a certificate."""

    _verification_method_icon = query_one("#verification-method", Label)
    """The label for the verification method."""
    _lock_icon = query_one("#lock-icon", Label)
    """The label for the lock icon."""
    _location_label = query_one("#location", Label)
    """The label for the location."""

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield Label(id="verification-method")
        yield Label(id="lock-icon")
        yield Label(id="location")

    def _watch_location(self) -> None:
        """React to the location changing."""
        if (
            len(
                display := ""
                if self.location is None
                else str(self.location)[-self._location_label.size.width :]
            )
            >= self._location_label.size.width
        ):
            display = f"…{display[1:]}"
        self._location_label.update(display)

    def _watch_needed_certificate(self) -> None:
        """React to the needed_certificate changing."""
        self._lock_icon.update(
            load_configuration().client_certificate_used_icon
            if self.needed_certificate
            else " "
        )

    def _watch_verification_method(self) -> None:
        """React to the verification_method changing."""
        self._verification_method_icon.set_classes(
            f"--verified-{str(self.verification_method).lower()}"
        )
        match self.verification_method:
            case "ca":
                self._verification_method_icon.update(
                    load_configuration().verified_ca_icon
                )
            case "tofu":
                self._verification_method_icon.update(
                    load_configuration().verified_tofu_icon
                )
            case "off":
                self._verification_method_icon.update(
                    load_configuration().verified_off_icon
                )
            case _:
                self._verification_method_icon.update(
                    load_configuration().verified_none_icon
                )

    def on_resize(self) -> None:
        """Handle the widget being resized."""
        self.location = self.location

    async def on_click(self, event: Click) -> None:
        """Handle the widget being clicked."""
        if event.widget is self._verification_method_icon:
            await self.screen.run_action(AboutThisPage.action_name())
        elif event.widget is self._lock_icon:
            await self.screen.run_action(AboutClientCertificate.action_name())


### title.py ends here
