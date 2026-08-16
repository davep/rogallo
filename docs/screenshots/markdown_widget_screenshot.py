"""Generate screenshots of Markdown support."""

from support.maker import make_app

app = make_app("example.md", convert_markdown_to_gemtext=False)

if __name__ == "__main__":
    app.run()

### markdown_screenshot.py ends here
