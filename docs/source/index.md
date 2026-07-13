# Introduction

```{.textual path="docs/screenshots/main_screenshot.py" title="Rogallo" lines=35 columns=90}
```

Rogallo is a terminal-based client for browsing
[Geminispace](https://geminiprotocol.net/). Its key features include:

- A bookmark facility (with search)
- A location history facility (with search)
- A backward/forward navigation facility
- Support for setting a home page
- Support for user input ([`1x` responses](https://geminiprotocol.net/docs/protocol-specification.gmi#input-expected)), including masked inputs for sensitive fields
- Support for in-application generation of self-signed [client certificates](https://geminiprotocol.net/docs/protocol-specification.gmi#client-certificates), with persistent per-capsule management
- Support for redirections ([`3x` responses](https://geminiprotocol.net/docs/protocol-specification.gmi#redirection))
- Copy-to-clipboard support for URIs or page contents
- Designed to work on macOS, GNU/Linux and Windows (and likely on other operating systems that support modern Python)
- Mouse support
- A view source facility
- A trust-on-first-use (TOFU) trust facility
- Has in-application help screens
- Has an easy-to-use command palette
- Hands unknown MIME types off to the operating system
- Optional support (on by default) for ANSI escape sequences in pages
- Support for viewing local [Gemtext](https://geminiprotocol.net/docs/gemtext-specification.gmi) files
- Choice of themes
- Persistent user configuration across sessions
- Fully responsive layout that adjusts dynamically to terminal resizing

!!! note

    Rogallo is primarily designed to browse content on Gemini capsules.
    However, in this documentation, you will mainly see it browsing files in
    the local filesystem. This is because the screenshots are generated when
    the documentation is generated, and so visiting `gemini://...` locations
    would be slow and brittle.

## Installing

### pipx

The application can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
pipx install rogallo
```

### uv

The application can be installed using [`uv`](https://docs.astral.sh/uv/getting-started/installation/):

```sh
uv tool install rogallo
```

If you don't have `uv` installed you can use [uvx.sh](https://uvx.sh) to
perform the installation. For GNU/Linux or macOS or similar:

```sh
curl -LsSf uvx.sh/rogallo/install.sh | sh
```

or on Windows:

```sh
powershell -ExecutionPolicy ByPass -c "irm https://uvx.sh/rogallo/install.ps1 | iex"
```

Once installed run the `rogallo` command.

## Running Rogallo

Once you've installed Rogallo using one of the [above methods](#installing),
you can run the application using the `rogallo` command. A number of command
line commands and switches available:

```sh
rogallo --help
```
```bash exec="on" result="text"
rogallo --help
```

### `bindings`

Prints the application commands whose keyboard bindings can be modified,
giving the defaults too.

```sh
rogallo bindings
```
```bash exec="on" result="text"
rogallo bindings
```

### `directories`

```sh
rogallo directories
```

This prints each of the directories where Rogallo stores cache,
configuration and data files. The output will look something like this:

```
/Users/davep/.cache/rogallo
/Users/davep/.config/rogallo
/Users/davep/.local/share/rogallo
```

The exact values will, of course, depend on [your own
environment](https://specifications.freedesktop.org/basedir/latest/).

### `licence`

Prints Rogallo's licence.

```sh
rogallo licence
```
```bash exec="on" result="text"
rogallo licence
```

### `open`

The open command can be used to open either a Gemtext file in the local
filesystem, or a connection to content on a Gemini capsule (normally a URI
starting with `gemini://`).

```sh
rogallo open --help
```
```bash exec="on" result="text"
rogallo open --help
```

### `themes`

Shows a list of all of the themes that are available.

```sh
rogallo themes
```
```bash exec="on" result="text"
rogallo themes
```

Use the `--theme` switch to set a theme from the command line.

### `-t`, `--theme`

Sets Rogallo's theme; this overrides and changes any previous theme choice
made [via the user interface](configuration.md#theme).

### `-v`, `--version`

Prints the version number of Rogallo.

```sh
rogallo --version
```
```bash exec="on" result="text"
rogallo --version
```

## Getting help

A great way to get to know Rogallo is to read the help screen. Once in the
application you can see this by pressing <kbd>F1</kbd>.

```{.textual path="docs/screenshots/main_screenshot.py" title="The Rogallo help sceeen" press="f1" lines=50 columns=120}
```

The help will adapt to which part of the screen has focus, providing extra
detail where appropriate.

### The command palette

Another way of discovering commands and keys in Rogallo is to use the
command palette (by default you can call it with
<kbd>ctrl</kbd>+<kbd>p</kbd>).

```{.textual path="docs/screenshots/main_screenshot.py" title="The Rogallo command palette" press="ctrl+p" lines=50 columns=120}
```

## Questions and feedback

If you have any questions about Rogallo, or you have ideas for how it might
be improved, do please feel free to [visit the discussion
area](https://github.com/davep/rogallo/discussions) and [ask your
question](https://github.com/davep/rogallo/discussions/categories/q-a) or
[suggest an
improvement](https://github.com/davep/rogallo/discussions/categories/ideas).

When doing so, please do search past discussions and also [issues current
and previous](https://github.com/davep/rogallo/issues) to make sure I've not
already dealt with this, or don't have your proposed change already flagged
as something to do.

[//]: # (index.md ends here)
