"""Provides the main entry point for the application."""

##############################################################################
# Local imports.
from .rogallo import Rogallo


##############################################################################
def main() -> None:
    """Main entry point for the rogallo application."""
    Rogallo().run()


##############################################################################
if __name__ == "__main__":
    main()

### __main__.py ends here
