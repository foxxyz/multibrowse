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
python multibrowse.py http://ivo.la - http://bbc.com
