Multibrowse: Multi-Monitor Kiosk Mode
=====================================

Simple python script to open several full-screen browser windows onto multiple monitor setups.

Browser is currently set to Google Chrome, but can be adapted to use any browser.

Supported platforms: Windows/Linux (OSX coming soon!)

Requirements
------------

 * Python 3

Usage
-----

Open `http://ivo.la` on monitor 1 and `http://bbc.com` on monitor 2

```
python multibrowse.py http://ivo.la http://bbc.com
```

Open `http://ivo.la` on monitor 1 and `http://bbc.com` on monitor 3

```
python multibrowse.py http://ivo.la - http
://bbc.com

Deployment
----------

Multibrowse includes a setup.py file to build a fully self-contained .exe for Windows machines. To build, install py2exe:

```
pip install py2exe
```

And run the building process:

```
python setup.py py2exe
```

This should generate a `dist` folder containing `multibrowse.exe`. This executable has no dependencies and can be used as-is.
