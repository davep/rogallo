import os
from argparse import Namespace
from pathlib import Path

from rogallo.data import update_configuration
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

app = Rogallo(
    Namespace(
        command="open",
        location=str(docs_dir / "examples/features.gmi"),
        theme="textual-mono",
    )
)

if __name__ == "__main__":
    app.run()
