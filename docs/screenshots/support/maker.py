"""Provides code for building a screenshot-ready Rogallo instance."""

import os
from argparse import Namespace
from pathlib import Path

from wasat import GeminiURI

from rogallo.data import Bookmark, save_bookmarks, update_configuration
from rogallo.rogallo import Rogallo

##############################################################################
# Work our the root of the documentation directory and the build directory.
docs_dir = Path(__file__).parent.parent.parent
docs_build_dir = docs_dir / "build"

##############################################################################
# Set the XDG_ to point at an isolated build environment for the
# screenshots. I don't want to mess with an actual installation of Rogallo.
os.environ["XDG_CONFIG_HOME"] = str(docs_build_dir / "config")
os.environ["XDG_DATA_HOME"] = str(docs_build_dir / "data")

##############################################################################
# Start out with the same configuration for every screenshot.
with update_configuration() as config:
    config.bookmarks_visble = False
    config.command_line_on_top = False
    config.disable_animations = True
    config.history_visible = False
    config.home_page = str(docs_dir / "examples/features.gmi")
    config.theme = "textual-mono"
    config.with_cache = False

##############################################################################
# Create some bookmarks for the screenshots.
save_bookmarks(
    [
        Bookmark("The Gemini Protocol", GeminiURI("gemini://geminiprotocol.net/")),
        Bookmark("davep", GeminiURI("gemini://davep.gemcities.com/")),
        Bookmark("Station", GeminiURI("gemini://station.martinrue.com/")),
        Bookmark("AstroBotany", GeminiURI("gemini://astrobotany.mozz.us/")),
    ]
)


##############################################################################
# Create the Rogallo app with the specified command line arguments.
def make_app(viewing: str = "features"):
    return Rogallo(
        Namespace(
            command="open",
            location=str(docs_dir / f"examples/{viewing}.gmi"),
            theme=None,
        )
    )


### maker.py ends here
