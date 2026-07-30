"""Provides a dialog for showing information about the current page."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Vertical, VerticalGroup
from textual.screen import ModalScreen
from textual.widgets import Button, Label

##############################################################################
# Local imports.
from ..document import Document


##############################################################################
class Data(HorizontalGroup):
    """A widget to show a label and a value."""

    DEFAULT_CSS = """
    Data {
        height: 1;
        width: auto;
        #label {
            text-style: bold;
            color: $text-accent;
            padding-right: 1;
        }
    }
    """

    def __init__(self, label: str, value: str | bool) -> None:
        """Initialise the widget."""
        super().__init__()
        self._data_label = label
        """The label of the data."""
        self._data_value = (
            value if isinstance(value, str) else ("Yes" if value else "No")
        )
        """The value of the data."""

    def compose(self) -> ComposeResult:
        """Compose the widget."""
        yield Label(f"{self._data_label}:", id="label")
        yield Label(self._data_value, id="value", markup=False)


##############################################################################
class AboutPage(ModalScreen[None]):
    """A modal screen to show information about the current page."""

    CSS = """
    AboutPage {
        align: center middle;

        &> VerticalGroup {
            height: auto;
            width: auto;
            max-width: 90%;
            max-height: 90%;
            background: $panel;
            border: panel $border;
        }

        #content {
            width: auto;
            height: auto;
            padding: 1 2;
            background: $surface;
        }

        #heading {
            text-style: bold underline;
            text-align: center;
            padding-top: 1;
            width: 100%;
        }

        #buttons {
            align: center middle;
            width: 100%;
            height: auto;
            padding-top: 1;
        }
    }
    """

    BINDINGS = [("escape", "close")]

    def __init__(self, document: Document) -> None:
        """Initialise the screen.

        Args:
            document: The document to show information about.
        """
        super().__init__()
        self._document = document
        """The document to show information about."""

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with VerticalGroup() as dialog:
            dialog.border_title = f"About {self._document.location}"
            with Vertical(id="content"):
                if self._document.original_location != self._document.location:
                    yield Data(
                        "Original location", str(self._document.original_location)
                    )
                yield Data("Size", f"{len(self._document.content)} bytes")
                yield Data("From cache", "Yes" if self._document.from_cache else "No")
                yield Data(
                    "Needed client certificate",
                    self._document.needed_certificate,
                )
                yield Data(
                    "Verification method", str(self._document.verification_method)
                )
                if self._document.server_certificate is not None:
                    yield Label("Server certificate", id="heading")
                    yield Data("Issuer", self._document.server_certificate.issuer)
                    yield Data("Subject", self._document.server_certificate.subject)
                    for (
                        name
                    ) in self._document.server_certificate.subject_alternative_names:
                        yield Data("Subject alternative", name)
                    yield Data(
                        "Fingerprint", self._document.server_certificate.fingerprint
                    )
                    yield Data(
                        "Valid from", str(self._document.server_certificate.not_before)
                    )
                    yield Data(
                        "Valid until", str(self._document.server_certificate.not_after)
                    )
                    yield Data(
                        "Is expired",
                        self._document.server_certificate.is_expired,
                    )
                    yield Data(
                        "Is self-signed",
                        self._document.server_certificate.is_self_signed,
                    )
            with HorizontalGroup(id="buttons"):
                yield Button("Close", id="close", variant="primary")

    @on(Button.Pressed, "#close")
    def action_close(self) -> None:
        """Close the screen."""
        self.dismiss()


### about_page.py ends here
