from argparse import Namespace
from pathlib import Path

from rogallo.rogallo import Rogallo

app = Rogallo(
    Namespace(
        command="open",
        location=str(Path(__file__).parent.parent / "examples/features.gmi"),
        theme="textual-mono",
    )
)

if __name__ == "__main__":
    app.run()
