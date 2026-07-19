"""Generate screenshots of ANSI support."""

from support.maker import make_app

app = make_app("mandelbrot")

if __name__ == "__main__":
    app.run()

### ansi_screenshot.py ends here
