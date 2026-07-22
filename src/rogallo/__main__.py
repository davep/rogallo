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

    # Add --theme
    parser.add_argument(
        "-t",
        "--theme",
        help="Set the theme for the application (see `themes` command for available themes)",
    )

    # Add --version
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information",
        action="version",
        version=f"%(prog)s v{__version__}",
    )

    # Allow for commands on the command line.
    sub_parser = parser.add_subparsers(
        dest="command", help="Available commands", required=False
    )

    # Add the 'bindings' command.
    sub_parser.add_parser(
        "bindings",
        help="List commands that can have their bindings changed",
    )

    # Add the 'diagnostics' command.
    sub_parser.add_parser(
        "diagnostics",
        aliases=["diag"],
        help="Show diagnostic information about the application",
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

    # Add the 'open' command.
    sub_parser.add_parser(
        "open",
        help="Open a location",
    ).add_argument(
        "location",
        help="The location to open",
    )

    # Add the 'themes' command.
    sub_parser.add_parser(
        "themes", help="List the available themes that can be used with --theme"
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
def show_dignoastics() -> None:
    """Show diagnostic information about the application environment."""
    from os import environ
    from platform import (
        python_compiler,
        python_implementation,
        python_version,
        release,
        system,
        version,
    )
    from sys import executable as python_executable

    from bagofstuff import __version__ as bagofstuff_version
    from cryptography import __version__ as cryptography_version
    from gemtext import __version__ as gemtext_version
    from textual import __version__ as textual_version
    from textual_enhanced import __version__ as textual_enhanced_version
    from textual_fspicker import __version__ as textual_fspicker_version
    from wasat import __version__ as wasat_version

    print("# Libraries")
    print(f"bagofstuff: {bagofstuff_version}")
    print(f"cryptography: {cryptography_version}")
    print(f"gemtext: {gemtext_version}")
    print(f"rogallo: {__version__}")
    print(f"textual: {textual_version}")
    print(f"textual_enhanced: {textual_enhanced_version}")
    print(f"textual_fspicker: {textual_fspicker_version}")
    print(f"wasat: {wasat_version}")
    print()
    print("# Python")
    print(f"Compiler: {python_compiler()}")
    print(f"Executable: {python_executable}")
    print(f"Implementation: {python_implementation()}")
    print(f"Version: {python_version()}")
    print()
    print("# System")
    print(f"Name: {system()}")
    print(f"Release: {release()}")
    print(f"Version: {version()}")
    print()
    print("# Terminal")
    if not (terminal := (environ.get("TERM_PROGRAM") or environ.get("TERMINAL_NAME"))):
        terminal = "*unknown*"
        for tell, name in {
            "ALACRITTY_WINDOW_ID": "Alacritty",
            "GNOME_TERMINAL_SCREEN": "GNOME Terminal",
            "INSIDE_EMACS": "GNU Emacs",
            "JEDITERM_SOURCE_ARGS": "PyCharm",
            "KITTY_PID": "Kitty",
            "KONSOLE_VERSION": "Konsole",
            "TERMINATOR_UUID": "Terminator",
            "WT_SESSION": "Windows Terminal",
            "XTERM_VERSION": "XTerm",
        }.items():
            if tell in environ:
                terminal = f"{name} ({environ[tell]})"
                break
    print(f"Detected: {terminal}")


##############################################################################
def main() -> None:
    """Main entry point for the rogallo application."""
    match (args := get_args()).command:
        case "d" | "dirs" | "directories":
            print(cache_dir())
            print(config_dir())
            print(data_dir())
        case "diag" | "diagnostics":
            show_dignoastics()
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
