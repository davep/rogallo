"""Provides a modal screen for uploading text or a file.

This screen is intended to be used for Titan uploads.
"""

##############################################################################
# Python imports.
from mimetypes import guess_type, types_map
from pathlib import Path
from typing import NamedTuple

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.getters import query_one
from textual.screen import ModalScreen
from textual.suggester import SuggestFromList
from textual.widgets import Button, Input, Label, TabbedContent, TabPane, TextArea

##############################################################################
# Textual enhanced imports.
from textual_enhanced.tools import add_key

##############################################################################
# Textual FSPicker imports.
from textual_fspicker import FileOpen

##############################################################################
# Wasat imports.
from wasat import TitanURI

##############################################################################
# Local imports.
from ..editor import edit_externally, external_editor
from ..presentation import short_location


##############################################################################
class UploadData(NamedTuple):
    """The data for uploading."""

    data: str | Path
    """The data to upload."""
    mime_type: str | None = None
    """The MIME type of the data."""
    token: str | None = None
    """The token to use for the upload, if any."""


##############################################################################
class UserUpload(ModalScreen[UploadData | None]):
    """A modal screen to get input from the user."""

    CSS = """
    UserUpload {
        align: center middle;

        &> VerticalGroup {
            height: 60vh;
            width: 60vw;
            background: $panel;
            border: panel $border;

            TabbedContent {
                height: 1fr;
                margin: 1;
            }

            #token-input {
                align: left middle;
                width: 1fr;
                padding: 0 1 0 2;
                height: auto;
                border-top: solid $border;
                Input {
                    width: 1fr;
                }
                Label {
                   height: 3;
                   content-align: center middle;
                }
            }

            #buttons {
                align: right middle;
                width: 100%;
                height: auto;
                padding: 1 1 0 0;
                Button {
                    margin-right: 1;
                }
            }

            #file {
                Button, Label {
                    margin: 0 0 1 1;
                }
            }

            #character-count {
                width: 1fr;
                padding-left: 1;
                color: $text-muted;
            }

            #editor-help {
                width: 1fr;
                content-align: right middle;
                padding-right: 1;
            }

            .--empty {
                color: $text-muted;
            }

            .--title {
                color: $accent;
            }
        }
    }
    """

    BINDINGS = [
        ("f2", "upload"),
        ("f3", "edit_externally"),
        ("ctrl+t", "prepare_text"),
        ("ctrl+f", "prepare_file"),
        ("escape", "cancel"),
    ]

    _character_count = query_one("#character-count", Label)
    """The label displaying the character count."""
    _text_or_file = query_one(TabbedContent)
    """The tabbed content widget for text or file."""
    _selected_file_display = query_one("#selected-file", Label)
    """The label displaying the selected file."""
    _text = query_one(TextArea)
    """The user's input text."""
    _mime_type = query_one("#mime-type", Input)
    """The mime type input."""
    _token = query_one("#token", Input)
    """The token input."""

    def __init__(self, location: TitanURI, existing_content: str) -> None:
        """Initialise the screen.

        Args:
            location: The location to upload to.
        """
        super().__init__()
        self._location = location
        """The location to upload to."""
        self._existing_content = existing_content
        """The existing content at the location."""
        self._selected_file: Path | None = None
        """The selected file to upload."""

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with VerticalGroup() as dialog:
            dialog.border_title = f"Upload to {self._location}"
            with TabbedContent():
                with TabPane("Text [$accent]\\[^t][/]", id="text"):
                    yield TextArea(
                        self._existing_content,
                        highlight_cursor_line=False,
                        placeholder="Enter text to upload...",
                    )
                    with HorizontalGroup():
                        yield Label(id="character-count")
                        if external_editor():
                            yield Label(
                                "[dim][$accent]\\[f3][/] for $EDITOR[/]",
                                id="editor-help",
                            )
                with TabPane("File [$accent]\\[^f][/]", id="file"):
                    yield Button("Select file...", id="select-file")
                    yield Label("Selected file:", classes="--title")
                    yield Label("<none>", id="selected-file", classes="--empty")
                    yield Label("Mime type:", classes="--title")
                    yield Input(
                        placeholder="Enter MIME type (e.g. text/plain)",
                        id="mime-type",
                        suggester=SuggestFromList(sorted(types_map.values())),
                    )
            with HorizontalGroup(id="token-input"):
                yield Label("Token:", classes="--title")
                yield Input(placeholder="Enter token (optional)", id="token")
            with HorizontalGroup(id="buttons"):
                yield Button(add_key("Upload", "f2", self), id="upload")
                yield Button(add_key("Cancel", "Esc", self), id="cancel")

    def on_mount(self) -> None:
        """Focus the text area on mount."""
        self._refresh_character_count()
        if self._existing_content:
            self._text.focus()

    def action_prepare_file(self) -> None:
        """Switch to the file tab."""
        self._text_or_file.active = "file"
        self.query_one("Tabs").focus()
        self.call_after_refresh(self.focus_next)

    def action_prepare_text(self) -> None:
        """Switch to the text tab."""
        self._text_or_file.active = "text"
        self.query_one("Tabs").focus()
        self.call_after_refresh(self.focus_next)

    @on(TextArea.Changed)
    def _refresh_character_count(self) -> None:
        """Update the text size count."""
        self._character_count.update(
            f"Characters: {len(self._text.text)}" if self._text.text else ""
        )

    @on(Button.Pressed, "#select-file")
    async def _select_file(self) -> None:
        """Select a file to upload."""
        start_at = Path(".")
        if self._selected_file is not None and self._selected_file.parent.is_dir():
            start_at = self._selected_file.parent
        if selected_file := await self.app.push_screen_wait(
            FileOpen(
                start_at,
                title="Select a file to upload",
                open_button="Select",
                cancel_button=add_key("Cancel", "Esc", self),
            )
        ):
            self._selected_file = selected_file
            self._selected_file_display.update(short_location(selected_file))
            self._selected_file_display.remove_class("--empty")
            mime_type, _ = guess_type(self._selected_file)
            self._mime_type.value = mime_type or "application/octet-stream"

    @on(Button.Pressed, "#upload")
    def action_upload(self) -> None:
        """Upload the data."""
        if self._text_or_file.active == "text":
            self.dismiss(
                UploadData(
                    data=self._text.text,
                    mime_type="text/plain",
                    token=self._token.value.strip() or None,
                )
            )
        elif self._text_or_file.active == "file" and self._selected_file is not None:
            self.dismiss(
                UploadData(
                    data=self._selected_file,
                    mime_type=self._mime_type.value.strip()
                    or "application/octet-stream",
                    token=self._token.value.strip() or None,
                )
            )

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """Cancel the upload."""
        self.dismiss(None)

    def action_edit_externally(self) -> None:
        """Edit the input in an external editor."""
        if self._text_or_file.active == "text":
            self._text.text = edit_externally(self.app, self._text.text)


### user_upload.py ends here
