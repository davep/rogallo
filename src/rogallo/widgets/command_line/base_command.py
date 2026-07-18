"""Provides the base command class."""

##############################################################################
# Textual imports.
from textual.widget import Widget


##############################################################################
class InputCommand:
    """Base class for input commands."""

    COMMAND = ""
    """The command for the help."""

    ALIASES = ""
    """Any aliases for the command for the help."""

    @classmethod
    def help_text(cls) -> tuple[str, ...]:
        """Get the help text for the command.

        Returns:
            The help text formatted as Markdown table rows.
        """
        return (f"| {cls.COMMAND} | {cls.ALIASES} | {cls.__doc__} |",)

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        del text, for_widget  # Unused
        return False

    @staticmethod
    def split_command(text: str) -> tuple[str, str]:
        """Split the command for further testing.

        Args:
            text: The text of the command.

        Returns:
            The command and its tail.
        """
        command, _, tail = text.strip().partition(" ")
        return command.strip(), tail.strip()

    @classmethod
    def suggestions(cls) -> tuple[str, ...]:
        """The suggested command matches for this command.

        Returns:
            A tuple of suggestions for the command.

        Notes:
            Any commands that look like value placeholders will be filtered
            out.
        """
        # Build up all the possible matches. These are built from the main
        # command and also the aliases. By convention the code will often
        # use `code` fences for commands, and the aliases will be a comma
        # list, so we clean that up as we go...
        return tuple(
            candidate.strip().removeprefix("`").removesuffix("`")
            for candidate in (cls.COMMAND, *cls.ALIASES.split(","))
            # Note that we filter out anything that looks like `<this>`.
            if not candidate.startswith("`<")
        )

    @classmethod
    def is_command(cls, command: str) -> bool:
        """Does the given command appear to be a match?

        Args:
            command: The command to test.

        Returns:
            `True` if the given command seems to be a match, `False` if not.
        """
        return command.strip().lower() in cls.suggestions()


### base_command.py ends here
