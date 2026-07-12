# Introduction

```{.textual path="docs/screenshots/main_screenshot.py" title="Rogallo" lines=40 columns=120}
```

Rogallo is a terminal-based client for browsing
[Geminispace](https://geminiprotocol.net/). It's key features include:

- A bookmark facility (with search)
- A location history facility (with search)
- A backward/forward navigation facility
- Support for setting a home page
- Support for user input (`1x` responses), including masked inputs for sensitive fields
- Support for in-application generation of self-signed client certificates, with persistent per-capsule management
- Support for redirections (`3x` responses)
- Copy-to-clipboard support for URLs, page text, or raw source
- Designed to work on macOS, GNU/Linux and Windows (and likely on other operating systems that support modern Python)
- Mouse support
- A view source facility
- A trust-on-first-use (TOFU) trust facility
- Has in-application help screens
- Has an easy-to-use command palette
- Hands unknown MIME types off to the operating system
- Optional support (on by default) for ANSI escape sequences in pages
- Support for viewing local Gemtext files
- Choice of themes
- Persistent user configuration across sessions
- Fully responsive layout that adjusts dynamically to terminal resizing

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

## Getting help

If you need help, or have any ideas, please feel free to [raise an
issue](https://github.com/davep/rogallo/issues) or [start a
discussion](https://github.com/davep/rogallo/discussions).

[//]: # (index.md ends here)
