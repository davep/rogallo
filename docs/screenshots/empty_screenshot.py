"""Generate screenshots of an empty UI."""

from support.maker import make_app

app = make_app("", with_fake_history=False)

if __name__ == "__main__":
    app.run()

### empty_screenshot.py ends here
