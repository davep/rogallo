# Icons

Rogallo allows you to configure many of the "icons" that are used in the
application. Icons are characters that are used within the overall [user
interface](../ui/index.md), especially in the [viewer](../ui/viewer.md). If
you wish to change any of the defaults, you can edit them in the
`icons.yaml` file found in the [configuration directory](./index.md).

## Defaults

The default file will look something like this:

```yaml
client_certificate_used: ⚿
fingerspace_link: ☛
geminispace_link: ⪢
gopherspace_link: ○
list_item_bullet: •
nexspace_link: ☽
otherspace_link: ↗
spartanspace_link: ⪧
titanspace_link: ⩓
unverified: •
verified_ca: ⛉
verified_off: ✗
verified_tofu: ✓
```

## Icon meanings

The following are the icons used in the viewer for each type a link,
selected depending on the URI:

- `fingerspace_link` - [`finger://`](../protocols/finger.md)
- `geminispace_link` - [`gemini://`](../protocols/gemini.md)
- `gopherspace_link` - [`gopher://`](../protocols/gopher.md)
- `nexspace_link` - [`nex://`](../protocols/nex.md)
- `otherspace_link` - Any other type of URI
- `spartanspace_link` - [`spartan://`](../protocols/spartan.md)
- `titanspace_link` - [`titan://`](../protocols/titan.md)

List items within the viewer use the value defined by `list_item_bullet`.

In the viewer's title bar, if a client certificate was used in loading a
page, the value of `client_certificate_used` will be shown.

Also in the viewer's title bar, depending on how a server was verified, the
following will be shown:

- `unverified` - No verification done or necessary
- `verified_ca` - Verified via a certificate authority
- `verified_off` - Verification is turned off
- `verified_tofu` - Verified via TOFU

[//]: # (icons.md ends here)
