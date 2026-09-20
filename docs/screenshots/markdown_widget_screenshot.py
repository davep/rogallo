"""Generate screenshots of Markdown support."""

from support.maker import GeneralConfiguration, make_app

app = make_app(
    "example.md", general=GeneralConfiguration(convert_markdown_to_gemtext=False)
)

if __name__ == "__main__":
    app.run()

### markdown_screenshot.py ends here
