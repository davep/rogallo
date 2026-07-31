# Gemini

## Introduction

Rogallo's primary supported protocol is the [Gemini
Protocol](https://geminiprotocol.net/). Gemini URIs begin with `gemini://`
and, generally, Gemini servers (known as capsules) respond with content
written in [a hypertext format known as
gemtext](https://geminiprotocol.net/docs/gemtext-specification.gmi).

Rogallo has support for all of the text-based content that can be delivered
via gemtext, and will, if necessary, hand other types of data off to your
operating system so it can find a more appropriate client for it.

## Visiting a Gemini Capsule

When you very first start Rogallo, you will see an empty display and its
internal command line will be focused.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Empty Rogallo" lines=30 columns=90}
```

You can type [many different commands in here](./command-line.md), as well
as URIs. To visit a Gemini capsule you type in a `gemini://` URI. For
example, if you want to visit a locally-hosted capsule, you'd type
`gemini://localhost/`:

```{.textual path="docs/screenshots/empty_screenshot.py" title="Entering a URI" lines=30 columns=90 press="g,e,m,i,n,i,:,/,/,l,o,c,a,l,h,,o,s,t,/"}
```

Hit <kbd>Enter</kbd> and the site's content will be loaded.

```{.textual path="docs/screenshots/empty_screenshot.py" title="A loaded Gemini page" lines=30 columns=90 press="g,e,m,i,n,i,:,/,/,l,o,c,a,l,h,,o,s,t,/,enter"}
```

Because Rogallo is, first and foremost, a Gemini browser, you don't *have*
to type out `gemini://` every time. You can just enter the host and path and
Rogallo will attempt to treat this as a `gemini://` URI.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Entering a non-prefixed location" lines=30 columns=90 press="l,o,c,a,l,h,,o,s,t"}
```

```{.textual path="docs/screenshots/empty_screenshot.py" title="After entering the location" lines=30 columns=90 press="l,o,c,a,l,h,,o,s,t,enter"}
```

!!! note
    The resulting URI is still `gemini://localhost/`

[//]: # (gemini.md ends here)
