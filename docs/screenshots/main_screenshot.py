import os
from argparse import Namespace
from pathlib import Path

from wasat import GeminiURI

from rogallo.data import Bookmark, save_bookmarks, update_configuration
from rogallo.rogallo import Rogallo

docs_dir = Path(__file__).parent.parent

os.environ["XDG_CONFIG_HOME"] = str(docs_dir / "build" / "config")
os.environ["XDG_DATA_HOME"] = str(docs_dir / "build" / "data")

with update_configuration() as config:
    config.bookmarks_visble = False
    config.command_line_on_top = False
    config.disable_animations = True
    config.history_visible = False
    config.home_page = str(docs_dir / "examples/features.gmi")
    config.with_cache = False

save_bookmarks(
    [
        Bookmark("The Gemini Protocol", GeminiURI("gemini://geminiprotocol.net/")),
        Bookmark("davep", GeminiURI("gemini://davep.gemcities.com/")),
        Bookmark("Station", GeminiURI("gemini://station.martinrue.com/")),
        Bookmark("AstroBotany", GeminiURI("gemini://astrobotany.mozz.us/")),
    ]
)

app = Rogallo(
    Namespace(
        command="open",
        location=str(docs_dir / "examples/features.gmi"),
        theme="textual-mono",
    )
)

if __name__ == "__main__":
    app.run()
