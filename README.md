Multibrowse: Multi-Monitor Kiosk Mode
=====================================

Simple python script to open several full-screen browser windows onto multiple monitor setups.

Browser is currently set to Google Chrome, but can be adapted to use any browser.

Supported platforms: Windows(7/8/10)/Linux/MacOS(x86/arm64)

Installation
------------

Installing with a package manager is recommended.

### Chocolatey

```
choco install multibrowse
```

### Manual Installation

Binaries can be found on the [releases page](https://github.com/foxxyz/multibrowse/releases). To build yourself, see below.

### Additional Requirements (Linux)

On linux, `xrandr` is used to find display configuration and must be available on `PATH`.

To install:
  * Install with Apt: `apt install lxrandr`
  * Install with Pacman: `pacman -S xorg-xrandr`

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


Development
-----------

### Requirements

 * Rust

### Running

`cargo run`

Building
--------

`cargo build --release`

License
-------

MIT
