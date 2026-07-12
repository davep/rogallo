import os
from argparse import Namespace
from pathlib import Path

from rogallo.rogallo import Rogallo

docs_dir = Path(__file__).parent.parent

os.environ["XDG_CONFIG_HOME"] = str(docs_dir / "build" / "config")
os.environ["XDG_DATA_HOME"] = str(docs_dir / "build" / "data")

app = Rogallo(
    Namespace(
        command="open",
        location=str(docs_dir / "examples/features.gmi"),
        theme="textual-mono",
    )
)

if __name__ == "__main__":
    app.run()
