"""Provides a dialog for setting the values of a certificate."""

##############################################################################
# Python imports.
from typing import Any

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, Collapsible, Input, Label, Rule

##############################################################################
# Textual enhanced imports.
from textual_enhanced.tools import add_key

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
type CertificateData = dict[str, Any]
"""Type of the data returned from the certificate dialog."""


##############################################################################
class Certificate(ModalScreen[CertificateData | None]):
    """A modal screen to get a certificate from the user."""

    CSS = """
    Certificate {
        align: center middle;

        &> VerticalGroup {
            width: 60%;
            height: auto;
            background: $panel;
            border: panel $border;
        }

        Collapsible {
            background: transparent;
            padding-right: 4;
            border-top: blank;
        }

        #buttons {
            height: auto;
            margin-top: 1;
            align-horizontal: right;
        }

        Button {
            margin-right: 1;
        }

        .leave-room {
            margin-top: 1;
        }

        Label {
            margin-left: 1;
        }

        /* Because https://github.com/Textualize/textual/issues/3945 */
        Label.leave-room {
            margin-top: 1;
            margin-left: 1;
        }
    }
    """

    BINDINGS = [("escape", "cancel"), ("f2", "create")]

    def __init__(self, location: GeminiURI, reason: str) -> None:
        """Initialise the object.

        Args:
            location: The location making the request.
            reason: The reason for the certificate request.
        """
        super().__init__()
        self._location = location
        """The location making the request."""
        self._reason = reason.strip()
        """The reason for the certificate request."""

    def compose(self) -> ComposeResult:
        """Compose the certificate dialog."""
        with VerticalGroup() as dialog:
            dialog.border_title = f"Certificate Request for {self._location}"
            if self._reason:
                yield Label(f"Reason: {self._reason}")
                yield Rule()
            yield Label("Common Name [dim](leave blank to use the host name)[/]:")
            yield Input(
                placeholder="Enter a descriptive name for the certificate",
                id="common_name",
            )
            with Collapsible(title="Advanced options"):
                yield Checkbox(
                    "Scope to domain/port [dim](ignores the path when scoping)[/]",
                    True,
                    id="scope-to-domain",
                    classes="leave-room",
                )
                yield Checkbox(
                    "Transient [dim](not saved to disk)[/]",
                    id="transient",
                    classes="leave-room",
                )
                yield Label(
                    "Valid for [dim](in days, <=0 is until 9999-12-31)[/]:",
                    classes="leave-room",
                )
                yield Input(
                    "0",
                    placeholder="Enter the number of days the certificate is valid for",
                    id="valid-for",
                    type="integer",
                )
                yield Label("Email address [dim](optional)[/]:", classes="leave-room")
                yield Input(
                    placeholder="Enter an email address for the certificate", id="email"
                )
                yield Label("User ID [dim](optional)[/]:", classes="leave-room")
                yield Input(
                    placeholder="Enter a user ID for the certificate", id="user_id"
                )
                yield Label("Domain [dim](optional)[/]:", classes="leave-room")
                yield Input(
                    placeholder="Enter a domain for the certificate", id="domain"
                )
                yield Label("Organisation [dim](optional)[/]:", classes="leave-room")
                yield Input(
                    placeholder="Enter an organization for the certificate",
                    id="organisation",
                )
                yield Label(
                    "Country [dim](optional, 2-letter code)[/]:", classes="leave-room"
                )
                yield Input(
                    placeholder="Enter a country code for the certificate",
                    id="country",
                    max_length=2,
                )
            with HorizontalGroup(id="buttons"):
                yield Button(add_key("Create", "F2"), id="create", variant="success")
                yield Button(add_key("Cancel", "Esc"), id="cancel", variant="error")

    def _maybe_add(self, data: CertificateData, key: str) -> None:
        """Maybe add a value to the certificate data.

        Args:
            data: The data to add to.
            key: The key to add.
        """
        if value := self.query_one(f"#{key}", Input).value.strip():
            data[key] = value

    def _scoped_location(self) -> GeminiURI:
        """Returns the location scoped as per the user's choice.

        Returns:
            The location to scope the certificate to.
        """
        return (
            self._location.with_path(None).with_query(None)
            if self.query_one("#scope-to-domain", Checkbox).value
            else self._location
        )

    @on(Button.Pressed, "#create")
    def action_create(self) -> None:
        """Create the certificate."""
        certificate_data: CertificateData = {
            "uri": self._scoped_location(),
            "transient": self.query_one("#transient", Checkbox).value,
        }
        self._maybe_add(certificate_data, "common_name")
        try:
            if (
                valid_days := int(self.query_one("#valid-for", Input).value.strip())
            ) > 0:
                certificate_data["valid_days"] = valid_days
        except ValueError:
            pass
        self._maybe_add(certificate_data, "email")
        self._maybe_add(certificate_data, "user_id")
        self._maybe_add(certificate_data, "domain")
        self._maybe_add(certificate_data, "organisation")
        self._maybe_add(certificate_data, "country")
        self.dismiss(certificate_data)

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """Cancel the edit of the raindrop data."""
        self.dismiss(None)


### certificate.py ends here
