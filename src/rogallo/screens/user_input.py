"""Provides a modal screen for getting user input."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.content import Content
from textual.screen import ModalScreen
from textual.widgets import TextArea

##############################################################################
# Wasat imports.
from wasat import GeminiURI


##############################################################################
class UserInput(ModalScreen[str | None]):
    """A modal screen to get input from the user."""

    CSS = """
    UserInput {
        align: center middle;

        TextArea, TextArea:focus {
            border: round $border;
            width: 60%;
            padding: 1;
            height: auto;
            max-height: 60%;
        }

        &.--sensitive TextArea {
            color: $text 10%;
        }
    }
    """

    BINDINGS = [
        ("escape", "escape"),
        ("f2", "submit"),
    ]

    def __init__(self, location: GeminiURI, prompt: str, sensitive: bool) -> None:
        """Initialise the object.

        Args:
            request_from: The request that prompted this input.
            prompt: The prompt to display to the user.
            sensitive: Whether the input is sensitive.
        """
        super().__init__(classes=("--sensitive" if sensitive else ""))
        self._location = location
        """The location making the request."""
        self._prompt = prompt.strip()
        """The prompt to display to the user."""
        self._sensitive = sensitive
        """Whether the input is sensitive."""

    def compose(self) -> ComposeResult:
        """Compose the input dialog."""
        yield (
            user_input := TextArea(
                highlight_cursor_line=False, placeholder="Enter your input here..."
            )
        )
        user_input.border_title = Content(
            self._prompt
            or (
                f"{'Sensitive input' if self._sensitive else 'Input'} for {self._location}"
                if self._location
                else "Input"
            )
        )
        user_input.border_subtitle = "Press F2 to submit"

    def action_submit(self) -> None:
        """Accept the input."""
        self.dismiss(self.query_one(TextArea).text.strip())

    def action_escape(self) -> None:
        """Escape out without getting the input."""
        self.dismiss(None)


### user_input.py ends here
