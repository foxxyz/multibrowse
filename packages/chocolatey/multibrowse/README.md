Multibrowse: Multi-Monitor Kiosk Mode
=====================================

Multibrowse is a CLI launcher for Google Chrome that makes it trivial to open full-screen browser windows onto multiple monitors.

Package Parameters
------------------

* `/installLocation` - Install to a different destination folder. Default: `$Env:ChocolateyToolsLocation\multibrowse`
Example: `choco install multibrowse --params '"/installLocation:C:\\opt"'`

Usage
-----

Open `http://ivo.la` on display 1 and `http://bbc.com` on display 2

```
multibrowse http://ivo.la http://bbc.com
```

Open `http://ivo.la` on display 1 and `http://bbc.com` on display 3

```
multibrowse http://ivo.la - http://bbc.com
```

To exit windows opened in fullscreen, use:
 * Mac: ⌘-Q
 * Windows/Linux: Alt-F4

### Display Order

Displays are ordered according to their x/y position from left to right, then top to bottom. Top-left display is always display #1.

### Additional Options

Additional CLI options passed to the `multibrowse` binary will be delegated to the browser instance. Check out the [wiki page](https://github.com/foxxyz/multibrowse/wiki) for common options.