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

- Support for the `gemini` protocol
- Support for the `gopher` protocol
- Support for the `finger` protocol
- A bookmark facility (with search)
- A location history facility (with search)
- A backward/forward navigation facility
- Copy-to-clipboard support for URIs or page contents
- Support for setting a home page
- Designed to work on macOS, GNU/Linux and Windows (and likely on other operating systems that support modern Python)
- Mouse support
- A view source facility
- Has in-application help screens
- Has an easy-to-use command palette
- Hands unknown MIME types off to the operating system
- Optional support (on by default) for ANSI escape sequences in pages
- Support for viewing local [Gemtext](https://geminiprotocol.net/docs/gemtext-specification.gmi) files
- Choice of themes
- Persistent user configuration across sessions
- Fully responsive layout that adjusts dynamically to terminal resizing
- Support for user-supplied custom UI themes

Key features for the Gemini protocol support include:

- Support for user input ([`1x` responses](https://geminiprotocol.net/docs/protocol-specification.gmi#input-expected)), including masked inputs for sensitive fields
    - Optionally use your own choice of text editor to compose the input
- Support for in-application generation of self-signed [client certificates](https://geminiprotocol.net/docs/protocol-specification.gmi#client-certificates), with persistent per-capsule management
- Support for redirections ([`3x` responses](https://geminiprotocol.net/docs/protocol-specification.gmi#redirection))
- A flexible capsule certificate verification approach, handling both CA-signed and self-signed certificates

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
