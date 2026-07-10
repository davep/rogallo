"""Provides the main entry point for the application."""

##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace
from inspect import cleandoc
from operator import attrgetter

##############################################################################
# Local imports.
from . import __doc__, __version__
from .data.locations import cache_dir, config_dir, data_dir
from .rogallo import Rogallo


##############################################################################
def get_args() -> Namespace:
    """Get the command line arguments.

    Returns:
        The arguments.
    """

    # Build the parser.
    parser = ArgumentParser(
        prog="rogallo",
        description=__doc__,
        epilog=f"v{__version__}",
    )

    # Add --version
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information",
        action="version",
        version=f"%(prog)s v{__version__}",
    )

    # Add --theme
    parser.add_argument(
        "-t",
        "--theme",
        help="Set the theme for the application (see `themes` command for available themes)",
    )

    # Allow for commands on the command line.
    sub_parser = parser.add_subparsers(
        dest="command", help="Available commands", required=False
    )

    # Add the 'directories' command.
    sub_parser.add_parser(
        "directories",
        aliases=["dirs", "d"],
        help="Show the directories created and used by Rogallo",
    )

    # Add the 'license' command.
    sub_parser.add_parser(
        "license",
        aliases=["licence"],
        help="Show license information",
    )

    # Add the 'bindings' command.
    sub_parser.add_parser(
        "bindings",
        help="List commands that can have their bindings changed",
    )

    # Add the 'themes' command.
    sub_parser.add_parser(
        "themes", help="List the available themes that can be used with --theme"
    )

    # Add the 'open' command.
    sub_parser.add_parser(
        "open",
        help="Open a location",
    ).add_argument(
        "location",
        help="The location to open",
    )

    # Finally, parse the command line.
    return parser.parse_args()


##############################################################################
def show_bindable_commands() -> None:
    """Show the commands that can have bindings applied."""
    from rich.console import Console

    from .safe_escape import escape
    from .screens import Main

    console = Console(highlight=False)
    for command in sorted(Main.COMMAND_MESSAGES, key=attrgetter("__name__")):
        if command().has_binding:
            console.print(
                f"[bold]{escape(command.__name__)}[/] [dim italic]- {escape(command.tooltip())}[/]"
            )
            console.print(
                f"    [dim italic]Default: {escape(command.binding().key)}[/]"
            )


##############################################################################
def show_themes() -> None:
    """Show the available themes."""
    for theme in sorted(Rogallo(Namespace(theme=None)).available_themes):
        if theme != "textual-ansi":
            print(theme)


##############################################################################
def main() -> None:
    """Main entry point for the rogallo application."""
    match (args := get_args()).command:
        case "d" | "dirs" | "directories":
            print(cache_dir())
            print(config_dir())
            print(data_dir())
        case "license" | "licence":
            print(cleandoc(Rogallo.HELP_LICENSE))
        case "bindings":
            show_bindable_commands()
        case "themes":
            show_themes()
        case _:
            Rogallo(args).run()


##############################################################################
if __name__ == "__main__":
    main()

### __main__.py ends here
