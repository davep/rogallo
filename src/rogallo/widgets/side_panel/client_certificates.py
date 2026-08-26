"""Provides a client certificate manager widget for the application."""

##############################################################################
# Python imports.
from itertools import chain

##############################################################################
# Textual imports.
from textual import on, work
from textual.reactive import var
from textual.suggester import SuggestFromList
from textual.widgets.option_list import Option

##############################################################################
# Textual enhanced imports.
from textual_enhanced.binding import HelpfulBinding
from textual_enhanced.dialogs import Confirm, ModalInput
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Wasat imports.
from wasat import ClientCertificate, ClientCertificateStore, GeminiURI, URIError

##############################################################################
# Local imports.
from ...data import Bookmarks, LocationHistory, NavigationHistory
from ...document import Document
from ...messages import ClientCertificatesModified
from ...safe_escape import escape
from ...screens.certificate_maker import ClientCertificateMaker
from ...screens.scope_picker import ScopePicker


##############################################################################
def _name(certificate: ClientCertificate) -> str:
    """Return the name of the certificate.

    Args:
        certificate: The certificate to get the name of.

    Returns:
        The name of the certificate.
    """
    return certificate.issuer_common_name or "Unnamed"


##############################################################################
class CertificateOption(Option):
    """An option for the client certificate manager."""

    def __init__(self, certificate: ClientCertificate, with_spacer: bool) -> None:
        """Initialise the certificate option.

        Args:
            certificate: The certificate to display.
            with_spacer: Whether to add a spacer after the option.
        """
        self._certificate = certificate
        """The certificate to display."""
        scopes = (
            "\n".join(f"[dim]{escape(scope)}[/]" for scope in certificate.scopes)
            if certificate.scopes
            else "[dim italic]Unused[/]"
        )
        super().__init__(
            f"{escape(_name(certificate))}\n"
            f"{scopes}\n"
            f"[dim][bold]Expires[/bold]: {certificate.not_after}[/]"
            f"{'\n' if with_spacer else ''}",
        )

    @property
    def certificate(self) -> ClientCertificate:
        """The certificate for this option."""
        return self._certificate


##############################################################################
class ClientCertificateManager(EnhancedOptionList):
    """A widget that manages client certificates for the application."""

    DEFAULT_CSS = """
    ClientCertificateManager {
        height: 1fr;
        border: none;
        text-wrap: nowrap;
        text-overflow: ellipsis;
        &:focus {
            border: none;
            background: $panel;
        }
    }
    """

    HELP = """
    ## Client certificates

    These are your client certificates. Here you can view, add, and remove
    them.
    """

    BINDINGS = [
        HelpfulBinding(
            "n",
            "new",
            "New",
            tooltip="Add a new certificate",
        ),
        HelpfulBinding(
            "d", "delete", "Delete", tooltip="Delete the selected certificate"
        ),
        HelpfulBinding(
            "a",
            "add_association",
            "Associate",
            tooltip="Add an association to the selected certificate",
        ),
        HelpfulBinding(
            "r",
            "remove_association",
            "Disassociate",
            tooltip="Remove an association from the selected certificate",
        ),
    ]

    location_history: var[LocationHistory] = var(LocationHistory)
    """The history of locations visited."""
    navigation_history: var[NavigationHistory] = var(NavigationHistory)
    """The history of navigation through locations."""
    bookmarks: var[Bookmarks] = var(list)
    """The bookmarks for the application."""
    client_certificates: var[list[ClientCertificate]] = var(list)
    """The client certificates for the application."""
    current_document: var[Document] = var(Document)

    def __init__(self, store: ClientCertificateStore) -> None:
        """Initialize the client certificate manager widget."""
        super().__init__()
        self._store = store
        """The client certificate store."""

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if not self.is_mounted:
            return True
        if action == "remove_association":
            return (
                self.highlighted is not None
                and isinstance(
                    option := self.options[self.highlighted], CertificateOption
                )
                and len(option.certificate.scopes) > 0
                or None
            )
        return True

    @on(EnhancedOptionList.OptionHighlighted)
    def _highlighted_certificate(self) -> None:
        """Refresh bindings as we move through the list."""
        self.refresh_bindings()

    async def _watch_client_certificates(self) -> None:
        """Load the client certificates into the widget."""
        with self.preserved_highlight:
            certificates = sorted(
                self.client_certificates,
                key=lambda certificate: _name(certificate).casefold(),
            )
            with_spacer = bool(certificates)
            self.clear_options().add_options(
                CertificateOption(certificate, with_spacer)
                for certificate in certificates
            )

    @work
    async def action_new(self) -> None:
        """Add a new certificate."""
        if data := await self.app.push_screen_wait(ClientCertificateMaker()):
            certificate = await self._store.create_certificate(**data)
            self.post_message(ClientCertificatesModified())
            self.notify(escape(_name(certificate)), title="Added")

    @work
    async def action_delete(self) -> None:
        """Delete the selected certificate."""
        if (
            self.highlighted is not None
            and isinstance(option := self.options[self.highlighted], CertificateOption)
            and await self.app.push_screen_wait(
                Confirm(
                    "Delete certificate?",
                    f"Are you sure you want to delete '{_name(option.certificate)}'?",
                )
            )
        ):
            await self._store.delete_certificate(option.certificate)
            self.post_message(ClientCertificatesModified())
            self.notify(escape(_name(option.certificate)), title="Deleted")

    async def _history_suggester(self) -> SuggestFromList:
        """A suggester for the history of input.

        If there us no history yet then a list of commands and aliases will
        be used.
        """
        return SuggestFromList(
            [
                *sorted(
                    # Suggest the set of all known locations...
                    set(
                        chain(
                            (str(visit.location) for visit in self.location_history),
                            (str(visit) for visit in self.navigation_history),
                            (str(bookmark.location) for bookmark in self.bookmarks),
                        )
                    )
                    # ...minus those that are already associated with a certificate.
                    - {
                        str(GeminiURI.with_default_scheme(scope))
                        for certificate in await self._store.list_certificates()
                        for scope in certificate.scopes
                    }
                ),
            ]
        )

    def _infer_default_association(self) -> str:
        """Infer a default association for the selected certificate.

        Returns:
            The default association, or an empty string if none can be inferred.
        """
        if (
            isinstance(self.current_document.location, GeminiURI)
            and not self.current_document.needed_certificate
        ):
            return str(self.current_document.location.with_path(None))
        return ""

    @work
    async def action_add_association(self) -> None:
        """Add an association to the selected certificate."""
        if (
            self.highlighted is not None
            and isinstance(option := self.options[self.highlighted], CertificateOption)
            and (
                location := await self.app.push_screen_wait(
                    ModalInput(
                        "Enter the location to associate with this certificate (e.g. gemini://example.com):",
                        initial=self._infer_default_association(),
                        title="Add Association",
                        suggester=await self._history_suggester(),
                    )
                )
            )
        ):
            try:
                await self._store.associate_scope(
                    option.certificate, GeminiURI.with_default_scheme(location)
                )
                self.post_message(ClientCertificatesModified())
                self.notify(f"Association added for {location}", title="Added")
            except (RuntimeError, URIError, ValueError) as error:
                self.notify(
                    f"Unable to add association for {location}:\n\n{error}",
                    severity="error",
                    title="Error",
                )

    @work
    async def action_remove_association(self) -> None:
        """Remove an association from the selected certificate."""
        # GTFO if there's no scope to remove.
        if (
            self.highlighted is None
            or not isinstance(
                option := self.options[self.highlighted], CertificateOption
            )
            or len(option.certificate.scopes) == 0
        ):
            return

        # If there's only one scope, use that. If there are multiple scopes,
        # ask the user to pick one. If there are no scopes, do nothing.
        location = (
            option.certificate.scopes[0]
            if len(option.certificate.scopes) == 1
            else (
                (
                    await self.app.push_screen_wait(
                        ScopePicker(
                            option.certificate,
                            "Remove scope",
                        )
                    )
                )
                if len(option.certificate.scopes) > 1
                else option.certificate.scopes[0]
            )
        )

        # Give up if we didn't get a scope.
        if location is None:
            return

        # Confirm they really want to remove the association.
        if await self.app.push_screen_wait(
            Confirm(
                "Remove association?",
                f"Are you sure you want to remove the association for '{escape(location)}'?",
            )
        ):
            try:
                await self._store.disassociate_scope(location)
                self.post_message(ClientCertificatesModified())
                self.notify(f"Association removed for {location}", title="Removed")
            except RuntimeError as error:
                self.notify(
                    f"Unable to remove association for {location}:\n\n{error}",
                    severity="error",
                    title="Error",
                )


### client_certificates.py ends here
