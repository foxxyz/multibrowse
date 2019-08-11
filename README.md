Multibrowse: Multi-Monitor Kiosk Mode
=====================================

Simple python script to open several full-screen browser windows onto multiple monitor setups.

Browser is currently set to Google Chrome, but can be adapted to use any browser.

Supported platforms: Windows(7/8/10)/Linux/MacOS

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

Installation
------------

Binaries can be found on the [releases page](https://github.com/foxxyz/multibrowse/releases). To build yourself, see below.

Development Requirements
------------------------

 * Python 3

### Linux

 * `xrandr`
  * Install with Apt: `apt-get install lxrandr`
  * Install with Pacman: `pacman -S xorg-xrandr`

### MacOS

 * PyObjC
  * Install with pip: `pip install pyobjc`


Building
--------

Multibrowse can be built into a single contained .exe file using [pyinstaller](http://www.pyinstaller.org/). Pyinstaller can be installed using `pip install pyinstaller`.

The following command produces a single self-contained exe file in `/dist`:

```
pyinstaller --onefile multibrowse.py
```

License
-------

MIT