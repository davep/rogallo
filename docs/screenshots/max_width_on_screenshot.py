"""Generate screenshots showing max document width on."""

from support.maker import make_app

app = make_app("much_text", maximum_document_width=80)

if __name__ == "__main__":
    app.run()

### max_width_on_screenshot.py ends here
