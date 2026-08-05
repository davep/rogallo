# Rogallo

![Rogallo](https://raw.githubusercontent.com/davep/rogallo/refs/heads/main/.images/rogallo-social-banner.webp)

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/davep/rogallo/style-lint-and-test.yaml)](https://github.com/davep/rogallo/actions)
[![GitHub commits since latest release](https://img.shields.io/github/commits-since/davep/rogallo/latest)](https://github.com/davep/rogallo/commits/main/)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/davep/rogallo)](https://github.com/davep/rogallo/issues)
[![GitHub Release Date](https://img.shields.io/github/release-date/davep/rogallo)](https://github.com/davep/rogallo/releases)
[![PyPI - License](https://img.shields.io/pypi/l/rogallo)](https://github.com/davep/rogallo/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rogallo)](https://github.com/davep/rogallo/blob/main/pyproject.toml)
[![PyPI - Version](https://img.shields.io/pypi/v/rogallo)](https://pypi.org/project/rogallo/)

## Introduction

Rogallo is a terminal-based client for browsing
[Geminispace](https://geminiprotocol.net/),
[Gopherspace](https://en.wikipedia.org/wiki/Gopher_(protocol)), and
[Fingerspace](https://en.wikipedia.org/wiki/Finger_(protocol)). Its key
features include:

- Support for the `gemini`, `gopher`, and `finger` protocols
- Bookmarks management with search
- Location history tracking with search
- Backward and forward page navigation
- Copy-to-clipboard support for URIs or page content
- Configurable home page
- Full mouse navigation and interaction support
- Built-in source viewer
- Context-sensitive help screens
- Command palette for quick command discovery and execution
- Automatic handoff of unknown MIME types to the operating system
- Optional rendering (on by default) of ANSI escape sequences in pages
- Local [Gemtext](https://geminiprotocol.net/docs/gemtext-specification.gmi) file viewing
- Built-in theme selection, plus support for user-supplied custom UI themes
- Persistent configuration across sessions
- Fully responsive layout that adjusts dynamically to terminal resizing
- Cross-platform support for macOS, GNU/Linux, Windows, and other operating systems running modern Python

Key features for Gemini protocol support include:

- User input handling ([`1x` responses](https://geminiprotocol.net/docs/protocol-specification.gmi#input-expected)), including masked inputs for sensitive fields
    - Optional external text editor integration for composing inputs
- In-application generation of self-signed [client certificates](https://geminiprotocol.net/docs/protocol-specification.gmi#client-certificates), with persistent per-capsule management
- Redirection handling ([`3x` responses](https://geminiprotocol.net/docs/protocol-specification.gmi#redirection))
- Flexible capsule certificate verification for both CA-signed and self-signed certificates

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

## File locations

Rogallo stores files in an `rogallo` directory within both [`$XDG_DATA_HOME`
and
`$XDG_CONFIG_HOME`](https://specifications.freedesktop.org/basedir-spec/latest/).
If you wish to fully remove anything to do with Rogallo you will need to
remove those directories too.

Expanding for the common locations, the files normally created are:

- `~/.cache/rogallo/*` -- The document cache.
- `~/.config/rogallo/configuration.json` -- The configuration file.
- `~/.local/share/rogallo/*` -- The locally-held data.

## Getting help

If you need help, or have any ideas, please feel free to [raise an
issue](https://github.com/davep/rogallo/issues) or [start a
discussion](https://github.com/davep/rogallo/discussions).

## TODO

See [the TODO tag in
issues](https://github.com/davep/rogallo/issues?q=is%3Aissue+is%3Aopen+label%3ATODO)
to see what I'm planning.

[//]: # (README.md ends here)
