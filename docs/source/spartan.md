# Spartan

## Introduction

Rogallo has support for visiting Spartan servers. Much like when Much like
when [visiting a Gemini server](./gemini.md), you can type in the URI of the
location you wish to visit. Spartan URIs begin with `spartan://`.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Entering a Spartan URI" lines=30 columns=90 press="s,p,a,r,t,a,n,:,/,/,l,o,c,a,l,h,o,s,t,/"}
```

```{.textual path="docs/screenshots/empty_screenshot.py" title="After pressing Enter" lines=30 columns=90 press="s,p,a,r,t,a,n,:,/,/,l,o,c,a,l,h,o,s,t,:,3,0,0,0,enter"}
```

## `spartan://` URIs

Rogallo will handle any valid `spartan://` URI, either as a link to be
followed from content returned by a Spartan, [Gemini](./gemini.md) or
[Gopher](./gopher.md) server, or as entered in the [command
line](./command-line.md).

## Input support

A key feature of Spartan is the ability to upload data to the server. In
support of this the protocol extends Gemtext with a new line type of `=:`.
These lines are a link that, when followed, should have data attached. In
Rogallo this will trigger an input box and, if you confirm the input, it
will be sent to the Spartan URI.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Following an input link" lines=30 columns=90 press="s,p,a,r,t,a,n,:,/,/,l,o,c,a,l,h,o,s,t,:,3,0,0,0,enter,3,enter"}
```

[//]: # (spartan.md ends here)
